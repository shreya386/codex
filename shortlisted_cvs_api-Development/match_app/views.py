import re
from rest_framework.response import Response
from .utils import get_cosine_similarity
import numpy as np
import pandas as pd
from django.db import connection
from .models import JobDetail, WorkerAttachment
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from openpyxl import *
from django.db import connection
import time


def is_user_with_role_present(user_id):
    query = """
    SELECT id
    FROM iconic_worker_test_v1.user_roles
    WHERE user_id = %s AND (role_name = 'INTERNALRECRUITER' OR role_name = 'EXTERNALRECRUITER')
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [user_id])
        result = cursor.fetchone()

    return result is not None


def get_worker_ids_for_user(user_id):
    if is_user_with_role_present(user_id):
        print("^^^^^^^^^^^User with role present")
        query = """
        SELECT worker_id
        FROM iconic_worker_test_v1.recruiter_worker
        WHERE recruiter_id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [user_id])
            rows = cursor.fetchall()

        worker_ids = [row[0] for row in rows]
        return worker_ids
    else:
        return []


@csrf_exempt
@api_view(["GET", "POST"])
def get_similar_cvs(request):
    if request.method == "POST":
        length_data = 0
        response_data = []
        job_id = request.POST.get("job_id")
        input_job_title = request.POST.get("input_job_title")
        input_location = request.POST.get("input_location")
        input_keywords = request.POST.get("input_keywords")
        input_certifications = request.POST.get("input_certifications")
        input_user_id = request.POST.get("input_user_id")
        print("input_user_id", input_user_id)

        if input_keywords:
            input_keywords_split = [
                k_keyword.strip() for k_keyword in input_keywords.split(",")
            ]
        if input_location:
            input_location_split = [
                i_keyword.strip() for i_keyword in input_location.split(",")
            ]
        if input_certifications:
            input_certifications_split = [
                j_keyword.strip() for j_keyword in input_certifications.split(",")
            ]
        if input_job_title:
            input_job_title_split = [
                l_keyword.strip() for l_keyword in input_job_title.split(",")
            ]

        if job_id:
            job_values = JobDetail.objects.filter(id=job_id).values(
                "id",
                "description",
                "jd_skills_extracted",
                "state",
                "title",
                "location",
                "state",
            )

            jd_info = []
            for job_item in job_values:
                jd_desc = []
                jd_skills_data = []
                title_lst = []
                id_lst = []
                lc_lst = []
                st_lst = []
                id_lst.append(job_item["id"])
                jd_desc.append(job_item["description"])
                jd_skills_data.append(job_item["jd_skills_extracted"])
                title_lst.append(job_item["title"])
                lc_lst.append(job_item["location"])
                st_lst.append(job_item["state"])
            jd_info = pd.DataFrame(
                {
                    "id": id_lst,
                    "Description": jd_desc,
                    "jd_skills_extracted": jd_skills_data,
                    "Job_Title": title_lst,
                    "Location": lc_lst,
                    "State": st_lst,
                }
            )

        if input_user_id:
            print("Entered into input_user_id")
            worker_ids = get_worker_ids_for_user(input_user_id)
            print("worker_ids", len(worker_ids))
            if worker_ids:
                print("Worker ID present")
                cvs_data = WorkerAttachment.objects.filter(
                    user_id__in=worker_ids, document_type="RESUME"
                ).values(
                    "user_id",
                    "path",
                    "file_name",
                    "skills_extracted",
                    "location",
                )

                cv_info = pd.DataFrame(
                    list(cvs_data),
                    columns=[
                        "user_id",
                        "path",
                        "file_name",
                        "skills_extracted",
                        "location",
                    ],
                )

            else:
                print("Entered into overall of user_id")
                cvs_data = WorkerAttachment.objects.filter(
                    document_type="RESUME"
                ).values_list(
                    "user_id",
                    "path",
                    "file_name",
                    "skills_extracted",
                    "location",
                )

                cv_info = pd.DataFrame(
                    list(cvs_data),
                    columns=[
                        "user_id",
                        "path",
                        "file_name",
                        "skills_extracted",
                        "location",
                    ],
                )

        else:
            print("Entered into overall")

            cvs_data = WorkerAttachment.objects.filter(
                document_type="RESUME"
            ).values_list(
                "user_id",
                "path",
                "file_name",
                "skills_extracted",
                "location",
            )

            cv_info = pd.DataFrame(
                list(cvs_data),
                columns=[
                    "user_id",
                    "path",
                    "file_name",
                    "skills_extracted",
                    "location",
                ],
            )

        cv_info = cv_info.apply(lambda x: x.str.strip()).replace("", np.nan)
        cv_info.dropna(subset=["skills_extracted"], inplace=True)
        cv_info.reset_index(drop=True, inplace=True)
        cv_info["matched_location"] = np.nan
        cv_info["Skills Keywords Matched"] = np.nan
        cv_info["Certifications Matched"] = np.nan
        cv_info["Job_Title_Matched"] = np.nan
        cv_info["matched_State"] = np.nan
        filtered_cv_info = pd.DataFrame()
        similarity_scores = []

        if job_id and (
            input_certifications is None
            and input_job_title is None
            and input_location is None
            and input_keywords is None
        ):
            for index, jd_row in jd_info.iterrows():
                location_match = [
                    skill.strip() for skill in jd_row["Location"].split(",")
                ]
                state_match = [skill.strip() for skill in jd_row["State"].split(",")]

                jd_skills = [
                    skill.strip() for skill in jd_row["jd_skills_extracted"].split(",")
                ]

                for jd_skills_keywords in jd_skills:
                    jd_skill_match = cv_info["skills_extracted"].str.contains(
                        jd_skills_keywords, flags=re.IGNORECASE
                    )

                    if jd_skill_match.any():
                        cv_info.loc[
                            jd_skill_match, "Skills Keywords Matched"
                        ] = cv_info.loc[
                            jd_skill_match, "Skills Keywords Matched"
                        ].apply(
                            lambda x: ", ".join(
                                list(set(x.split(", ")) | {jd_skills_keywords})
                            )
                            if isinstance(x, str)
                            else jd_skills_keywords
                        )

                for jd_location in location_match:
                    pattern = r"\b{}\b".format(re.escape(jd_location))
                    jd_location_match = cv_info["location"].str.contains(
                        pattern, flags=re.IGNORECASE, na=False
                    )
                    if jd_location_match.any():
                        cv_info.loc[
                            jd_location_match, "matched_location"
                        ] = cv_info.loc[jd_location_match, "matched_location"].apply(
                            lambda x: ", ".join(
                                list(set(x.split(", ")) | {jd_location})
                            )
                            if isinstance(x, str)
                            else jd_location
                        )

                for jd_state in state_match:
                    pattern = r"\b{}\b".format(re.escape(jd_state))
                    jd_state_match = cv_info["location"].str.contains(
                        pattern, flags=re.IGNORECASE, na=False
                    )
                    if jd_state_match.any():
                        cv_info.loc[jd_state_match, "matched_State"] = cv_info.loc[
                            jd_state_match, "matched_State"
                        ].apply(
                            lambda x: ", ".join(list(set(x.split(", ")) | {jd_state}))
                            if isinstance(x, str)
                            else jd_state
                        )

        elif (
            job_id
            and input_keywords
            and input_location
            and input_certifications
            and input_job_title
        ):
            print("^^^^^^^Entered into Second condition")
            if input_keywords:
                for keywords in input_keywords_split:
                    input_skill_match = cv_info["skills_extracted"].str.contains(
                        keywords, flags=re.IGNORECASE
                    )
                    if input_skill_match.any():
                        # filtered_rows = filtered_cv_info[input_skill_match]
                        cv_info.loc[
                            input_skill_match, "Skills Keywords Matched"
                        ] = cv_info.loc[
                            input_skill_match, "Skills Keywords Matched"
                        ].apply(
                            lambda x: ", ".join(list(set(x.split(", ")) | {keywords}))
                            if isinstance(x, str)
                            else keywords
                        )

            if input_location:
                # 2) Input_Locations
                for location_key in input_location_split:
                    pattern = r"\b{}\b".format(re.escape(location_key))
                    location_match = cv_info["location"].str.contains(
                        pattern, flags=re.IGNORECASE, na=False
                    )
                    if location_match.any():
                        cv_info.loc[location_match, "matched_location"] = cv_info.loc[
                            location_match, "matched_location"
                        ].apply(
                            lambda x: ", ".join(
                                list(set(x.split(", ")) | {location_key})
                            )
                            if isinstance(x, str)
                            else location_key
                        )

            if input_certifications:
                # 3) Input_Certifications
                for certification_key in input_certifications_split:
                    certifications_pattern = r"\b{}\b".format(
                        re.escape(certification_key)
                    )
                    certificaton_match = cv_info["skills_extracted"].str.contains(
                        certifications_pattern, flags=re.IGNORECASE, na=False
                    )
                    if certificaton_match.any():
                        cv_info.loc[
                            certificaton_match, "Certifications Matched"
                        ] = cv_info.loc[
                            certificaton_match, "Certifications Matched"
                        ].apply(
                            lambda x: ", ".join(
                                list(set(x.split(", ")) | {certification_key})
                            )
                            if isinstance(x, str)
                            else certification_key
                        )

            if input_job_title:
                # 4) Input_Job_Title
                for title_key in input_job_title_split:
                    title_pattern = r"\b{}\b".format(re.escape(title_key))
                    title_match = cv_info["skills_extracted"].str.contains(
                        title_pattern, flags=re.IGNORECASE, na=False
                    )
                    if title_match.any():
                        cv_info.loc[title_match, "Job_Title_Matched"] = cv_info.loc[
                            title_match, "Job_Title_Matched"
                        ].apply(
                            lambda x: ", ".join(list(set(x.split(", ")) | {title_key}))
                            if isinstance(x, str)
                            else title_key
                        )

        elif (
            input_keywords or input_certifications or input_job_title or input_location
        ) and job_id is None:
            if input_keywords:
                for keywords in input_keywords_split:
                    input_skill_match = cv_info["skills_extracted"].str.contains(
                        keywords, flags=re.IGNORECASE
                    )
                    if input_skill_match.any():
                        # filtered_rows = filtered_cv_info[input_skill_match]
                        cv_info.loc[
                            input_skill_match, "Skills Keywords Matched"
                        ] = cv_info.loc[
                            input_skill_match, "Skills Keywords Matched"
                        ].apply(
                            lambda x: ", ".join(list(set(x.split(", ")) | {keywords}))
                            if isinstance(x, str)
                            else keywords
                        )

            if input_location:
                for location_key in input_location_split:
                    print("Location key", location_key)
                    pattern = r"\b{}\b".format(re.escape(location_key))
                    print("Location pattern", pattern)
                    location_match = cv_info["location"].str.contains(
                        pattern, flags=re.IGNORECASE, na=False
                    )
                    if location_match.any():
                        cv_info.loc[location_match, "matched_location"] = cv_info.loc[
                            location_match, "matched_location"
                        ].apply(
                            lambda x: ", ".join(
                                list(set(x.split(", ")) | {location_key})
                            )
                            if isinstance(x, str)
                            else location_key
                        )

            if input_certifications:
                # 3) Input_Certifications
                for certification_key in input_certifications_split:
                    certifications_pattern = r"\b{}\b".format(
                        re.escape(certification_key)
                    )
                    certificaton_match = cv_info["skills_extracted"].str.contains(
                        certifications_pattern, flags=re.IGNORECASE, na=False
                    )
                    if certificaton_match.any():
                        cv_info.loc[
                            certificaton_match, "Certifications Matched"
                        ] = cv_info.loc[
                            certificaton_match, "Certifications Matched"
                        ].apply(
                            lambda x: ", ".join(
                                list(set(x.split(", ")) | {certification_key})
                            )
                            if isinstance(x, str)
                            else certification_key
                        )

            if input_job_title:
                # 4) Input_Job_Title
                for title_key in input_job_title_split:
                    title_pattern = r"\b{}\b".format(re.escape(title_key))
                    title_match = cv_info["skills_extracted"].str.contains(
                        title_pattern, flags=re.IGNORECASE, na=False
                    )
                    if title_match.any():
                        cv_info.loc[title_match, "Job_Title_Matched"] = cv_info.loc[
                            title_match, "Job_Title_Matched"
                        ].apply(
                            lambda x: ", ".join(list(set(x.split(", ")) | {title_key}))
                            if isinstance(x, str)
                            else title_key
                        )

        elif (
            job_id
            and input_keywords is None
            and (
                input_location is not None
                or input_certifications is not None
                or input_job_title is not None
            )
        ):
            if input_location:
                for location_key in input_location_split:
                    pattern = r"\b{}\b".format(re.escape(location_key))
                    location_match = cv_info["location"].str.contains(
                        pattern, flags=re.IGNORECASE, na=False
                    )
                    if location_match.any():
                        cv_info.loc[location_match, "matched_location"] = cv_info.loc[
                            location_match, "matched_location"
                        ].apply(
                            lambda x: ", ".join(
                                list(set(x.split(", ")) | {location_key})
                            )
                            if isinstance(x, str)
                            else location_key
                        )

            if input_certifications:
                # 3) Input_Certifications
                for certification_key in input_certifications_split:
                    certifications_pattern = r"\b{}\b".format(
                        re.escape(certification_key)
                    )
                    certificaton_match = cv_info["skills_extracted"].str.contains(
                        certifications_pattern, flags=re.IGNORECASE, na=False
                    )
                    if certificaton_match.any():
                        cv_info.loc[
                            certificaton_match, "Certifications Matched"
                        ] = cv_info.loc[
                            certificaton_match, "Certifications Matched"
                        ].apply(
                            lambda x: ", ".join(
                                list(set(x.split(", ")) | {certification_key})
                            )
                            if isinstance(x, str)
                            else certification_key
                        )

            if input_job_title:
                # 4) Input_Job_Title
                for title_key in input_job_title_split:
                    title_pattern = r"\b{}\b".format(re.escape(title_key))
                    title_match = cv_info["skills_extracted"].str.contains(
                        title_pattern, flags=re.IGNORECASE, na=False
                    )
                    if title_match.any():
                        cv_info.loc[title_match, "Job_Title_Matched"] = cv_info.loc[
                            title_match, "Job_Title_Matched"
                        ].apply(
                            lambda x: ", ".join(list(set(x.split(", ")) | {title_key}))
                            if isinstance(x, str)
                            else title_key
                        )

            if input_keywords is None:
                print("^^^^^^^^^^^Entered into third condition", jd_info)
                for index, jd_row in jd_info.iterrows():
                    jd_skills = [
                        skill.strip()
                        for skill in jd_row["jd_skills_extracted"].split(",")
                    ]
                    for jd_skills_keywords in jd_skills:
                        jd_skill_match = cv_info["skills_extracted"].str.contains(
                            jd_skills_keywords, flags=re.IGNORECASE
                        )

                        if jd_skill_match.any():
                            cv_info.loc[
                                jd_skill_match, "Skills Keywords Matched"
                            ] = cv_info.loc[
                                jd_skill_match, "Skills Keywords Matched"
                            ].apply(
                                lambda x: ", ".join(
                                    list(set(x.split(", ")) | {jd_skills_keywords})
                                )
                                if isinstance(x, str)
                                else jd_skills_keywords
                            )

        elif job_id and (
            (input_keywords is not None)
            or (input_location is not None)
            or (input_certifications is not None)
            or (input_job_title is not None)
        ):
            print("^^^^^^^^^^^Entered into fifth condition")
            if input_keywords is not None:
                for keywords in input_keywords_split:
                    input_skill_match = cv_info["skills_extracted"].str.contains(
                        keywords, flags=re.IGNORECASE
                    )
                    if input_skill_match.any():
                        # filtered_rows = filtered_cv_info[input_skill_match]
                        cv_info.loc[
                            input_skill_match, "Skills Keywords Matched"
                        ] = cv_info.loc[
                            input_skill_match, "Skills Keywords Matched"
                        ].apply(
                            lambda x: ", ".join(list(set(x.split(", ")) | {keywords}))
                            if isinstance(x, str)
                            else keywords
                        )

            if input_location:
                # 2) Input_Locations
                for location_key in input_location_split:
                    pattern = r"\b{}\b".format(re.escape(location_key))
                    location_match = cv_info["location"].str.contains(
                        pattern, flags=re.IGNORECASE, na=False
                    )
                    if location_match.any():
                        cv_info.loc[location_match, "matched_location"] = cv_info.loc[
                            location_match, "matched_location"
                        ].apply(
                            lambda x: ", ".join(
                                list(set(x.split(", ")) | {location_key})
                            )
                            if isinstance(x, str)
                            else location_key
                        )

            if input_certifications:
                # 3) Input_Certifications
                for certification_key in input_certifications_split:
                    certifications_pattern = r"\b{}\b".format(
                        re.escape(certification_key)
                    )
                    certificaton_match = cv_info["skills_extracted"].str.contains(
                        certifications_pattern, flags=re.IGNORECASE, na=False
                    )
                    if certificaton_match.any():
                        cv_info.loc[
                            certificaton_match, "Certifications Matched"
                        ] = cv_info.loc[
                            certificaton_match, "Certifications Matched"
                        ].apply(
                            lambda x: ", ".join(
                                list(set(x.split(", ")) | {certification_key})
                            )
                            if isinstance(x, str)
                            else certification_key
                        )

            if input_job_title:
                # 4) Input_Job_Title
                for title_key in input_job_title_split:
                    title_pattern = r"\b{}\b".format(re.escape(title_key))
                    title_match = cv_info["skills_extracted"].str.contains(
                        title_pattern, flags=re.IGNORECASE, na=False
                    )
                    if title_match.any():
                        cv_info.loc[title_match, "Job_Title_Matched"] = cv_info.loc[
                            title_match, "Job_Title_Matched"
                        ].apply(
                            lambda x: ", ".join(list(set(x.split(", ")) | {title_key}))
                            if isinstance(x, str)
                            else title_key
                        )

        if cv_info["matched_location"].notna().any():
            filtered_cv_info = pd.concat(
                [filtered_cv_info, cv_info[cv_info["matched_location"].notna()]]
            )

        if cv_info["Certifications Matched"].notna().any():
            filtered_cv_info = pd.concat(
                [
                    filtered_cv_info,
                    cv_info[cv_info["Certifications Matched"].notna()],
                ]
            )

        if cv_info["Job_Title_Matched"].notna().any():
            filtered_cv_info = pd.concat(
                [
                    filtered_cv_info,
                    cv_info[cv_info["Job_Title_Matched"].notna()],
                ]
            )
        if cv_info["matched_State"].notna().any():
            filtered_cv_info = pd.concat(
                [filtered_cv_info, cv_info[cv_info["matched_State"].notna()]]
            )
        if cv_info["Skills Keywords Matched"].notna().any():
            filtered_cv_info = pd.concat(
                [
                    filtered_cv_info,
                    cv_info[cv_info["Skills Keywords Matched"].notna()],
                ]
            )
        if input_keywords:
            print("----Int h input")
            for index, fv_row in filtered_cv_info.iterrows():
                filtered_skills = [
                    skill.strip() for skill in fv_row["skills_extracted"].split(",")
                ]
                scores = get_cosine_similarity(input_keywords_split, filtered_skills)
                # print("all scores: ", scores)
                max_scores = np.max(scores, axis=1)
                max_score = np.max(max_scores)
                rounded_scores = round(max_score, 2)
                similarity_scores.append(rounded_scores)
            filtered_cv_info["cosine_similarity"] = similarity_scores

        elif job_id:
            print("----Direct JOB ID-----")
            for index, fv_row in filtered_cv_info.iterrows():
                filtered_skills = [
                    skill.strip() for skill in fv_row["skills_extracted"].split(",")
                ]
                for index, jd_row in jd_info.iterrows():
                    jd_skills = [
                        skill.strip()
                        for skill in jd_row["jd_skills_extracted"].split(",")
                    ]
                    scores = get_cosine_similarity(jd_skills, filtered_skills)
                    # print("all scores: ", scores)
                    max_scores = np.max(scores, axis=1)
                    max_score = np.max(max_scores)
                    rounded_scores = round(max_score, 2)
                    similarity_scores.append(rounded_scores)
            filtered_cv_info["cosine_similarity"] = similarity_scores

        duplicate = filtered_cv_info.duplicated()
        print("the length of duplicates: ", duplicate.value_counts())
        filtered_cv_info.drop_duplicates(keep="first", inplace=True)
        # filtered_cv_info.to_excel("Resultant_df/filtered_csv_info.xlsx")
        sort_columns = []

        if (
            "matched_location" in filtered_cv_info.columns
            and filtered_cv_info["matched_location"].notnull().any()
        ):
            sort_columns.append("matched_location")

        if (
            "Skills Keywords Matched" in filtered_cv_info.columns
            and filtered_cv_info["Skills Keywords Matched"].notnull().any()
        ):
            sort_columns.append("Skills Keywords Matched")

        if (
            "Certifications Matched" in filtered_cv_info.columns
            and filtered_cv_info["Certifications Matched"].notnull().any()
        ):
            sort_columns.append("Certifications Matched")

        if (
            "Job_Title_Matched" in filtered_cv_info.columns
            and filtered_cv_info["Job_Title_Matched"].notnull().any()
        ):
            sort_columns.append("Job_Title_Matched")

        if (
            "matched_State" in filtered_cv_info.columns
            and filtered_cv_info["matched_State"].notnull().any()
        ):
            sort_columns.append("matched_State")

        filtered_cv_info.sort_values(by=sort_columns, ascending=False)
        filtered_cv_info = filtered_cv_info[:500]
        # Create a copy of the DataFrame
        sorted_df = filtered_cv_info.copy()
        if sorted_df.empty:
            length_data = 0
            response_data = "No Similarity found"
        else:
            # Calculate the number of columns with values for each row
            sorted_df["num_filled_columns"] = (
                sorted_df[
                    [
                        "matched_location",
                        "Skills Keywords Matched",
                        "Certifications Matched",
                        "Job_Title_Matched",
                    ]
                ]
                .notnull()
                .sum(axis=1)
            )

            # Sort the DataFrame based on the number of filled columns in descending order, and then by the specified columns
            sorted_df = sorted_df.sort_values(
                by=[
                    "num_filled_columns",
                    "matched_location",
                    "Skills Keywords Matched",
                    "Certifications Matched",
                    "Job_Title_Matched",
                ],
                ascending=[False, False, False, False, False],
            )

            # Drop the 'num_filled_columns' column
            sorted_df = sorted_df.drop("num_filled_columns", axis=1)

            for column in sorted_df.columns:
                # Step 2: Check if all values in the column are null
                if sorted_df[column].isnull().all():
                    # Step 3: Drop the column from the sorted_data DataFrame
                    sorted_df = sorted_df.drop(column, axis=1)
                    sorted_df = sorted_df.reset_index(drop=True)

            if "cosine_similarity" in sorted_df.columns:
                data = list(
                    zip(
                        sorted_df["user_id"].to_list(),
                        sorted_df["file_name"].to_list(),
                        sorted_df["cosine_similarity"].to_list(),
                    )
                )

                response_data = [
                    {
                        "user_id": user_id,
                        "cv_file_path": file_name,
                        "skills_compatibility_score": cosine_similarity,
                    }
                    for user_id, file_name, cosine_similarity in data
                    if cosine_similarity is not None
                ]
            else:
                data = list(
                    zip(
                        sorted_df["user_id"].to_list(),
                        sorted_df["file_name"].to_list(),
                    )
                )

                response_data = [
                    {
                        "user_id": user_id,
                        "cv_file_path": file_name,
                        "skills_compatibility_score": 0,
                    }
                    for user_id, file_name in data
                ]

        length_data = len(filtered_cv_info)
        # filtered_cv_info.to_excel("Resultant_df/filtered_csv_info.xlsx")

        return Response(
            {
                "status_code": "200",
                "cv_count": length_data,
                "message": "Sucessfully Processed CV",
                "similar_cvs": response_data,
            }
        )
    else:
        # Handle the GET request (if required)
        return Response(
            {
                "status_code": "400",
                "message": "Invalid request method",
            },
            status=400,
        )

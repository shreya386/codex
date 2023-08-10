# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_mysql.models import Bit1BooleanField


class JobDetail(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    annual_salary_from = models.FloatField()
    annual_salary_to = models.FloatField()
    city = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    jd_skills_extracted = models.TextField(blank=True, null=True)
    employment_type = models.CharField(max_length=255, blank=True, null=True)
    estimated_start_date = models.DateTimeField(blank=True, null=True)
    hourly_rate_from = models.FloatField()
    hourly_rate_to = models.FloatField()
    is401kretirement = Bit1BooleanField(blank=True, null=True)
    is_health_benifit = Bit1BooleanField(
        blank=True, null=True
    )  # This field type is a guess.
    is_pay_for_milage = Bit1BooleanField(
        blank=True, null=True
    )  # This field type is a guess.
    is_per_diem = Bit1BooleanField(blank=True, null=True)  # This field type is a guess.
    is_relocation_benifit = Bit1BooleanField(
        blank=True, null=True
    )  # This field type is a guess.
    is_yearly_bonus = Bit1BooleanField(
        blank=True, null=True
    )  # This field type is a guess.
    job_cancelled_date = models.DateTimeField(blank=True, null=True)
    job_completed_date = models.DateTimeField(blank=True, null=True)
    job_posted_date = models.DateTimeField(blank=True, null=True)
    job_type = models.CharField(max_length=255, blank=True, null=True)
    last_saved_step = models.IntegerField()
    latitude = models.FloatField()
    location = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.FloatField()
    milage_rate = models.FloatField()
    minimum_mile = models.FloatField()
    no_of_opening_job = models.IntegerField()
    per_diem_rate = models.FloatField()
    region = models.CharField(max_length=255, blank=True, null=True)
    special_qualification = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    worker_margin = models.FloatField()
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    assigned_to = models.ForeignKey(
        "UserMaster", models.DO_NOTHING, db_column="assigned_to", blank=True, null=True
    )
    experience = models.ForeignKey(
        "ExperienceLevelMaster", models.DO_NOTHING, blank=True, null=True
    )
    job_title = models.ForeignKey(
        "JobTitleMaster",
        models.DO_NOTHING,
        db_column="job_title",
        blank=True,
        null=True,
    )
    supervisor = models.ForeignKey(
        "UserMaster",
        models.DO_NOTHING,
        db_column="supervisor",
        related_name="jobdetail_supervisor_set",
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        "UserMaster", models.DO_NOTHING, related_name="jobdetail_user_set"
    )

    class Meta:
        managed = False
        db_table = "job_detail"


class WorkerAttachment(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    user = models.ForeignKey("UserMaster", models.DO_NOTHING)
    file_name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    skills_extracted = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    document_type = models.CharField(max_length=50)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "worker_attachment"


class UserMaster(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.TextField()  # This field type is a guess.
    is_deleted = models.TextField()  # This field type is a guess.
    is_verified = models.TextField()  # This field type is a guess.
    last_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)
    sub_admin_contact_number = models.CharField(max_length=255, blank=True, null=True)
    verification_token = models.CharField(max_length=255, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "user_master"


class ExperienceLevelMaster(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    expression = models.CharField(max_length=255, blank=True, null=True)
    from_year = models.IntegerField()
    is_enable = models.TextField(blank=True, null=True)  # This field type is a guess.
    level = models.CharField(max_length=255, blank=True, null=True)
    to_year = models.IntegerField()

    class Meta:
        managed = False
        db_table = "experience_level_master"


class JobTitleMaster(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_enable = models.TextField(blank=True, null=True)  # This field type is a guess.
    title = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "job_title_master"

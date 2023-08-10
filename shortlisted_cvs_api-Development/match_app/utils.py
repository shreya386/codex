from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Define function to calculate similarity between two texts using Spacy
def get_cosine_similarity(str1_list, str2_list):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(str1_list + str2_list).toarray()
    similarity_scores = cosine_similarity(
        vectors[: len(str1_list)], vectors[len(str1_list) :]
    )
    return similarity_scores

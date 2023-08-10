from django.urls import path

from . import views

urlpatterns = [
    # path("", views.description, name="description"),
    path("", views.get_similar_cvs, name="results"),
]

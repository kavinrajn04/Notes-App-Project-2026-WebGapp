from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.landing_page),
    path("api/notes/", views.notes_list, name="notes_list"),
]

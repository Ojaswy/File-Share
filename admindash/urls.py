from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("text", views.text, name="text"),
    path("deletetext", views.deletetext, name="deletetext"),
]

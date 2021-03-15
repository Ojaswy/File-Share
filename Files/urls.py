from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("f/<str:filename>/", views.File, name="File"),
    path("dashboard", views.dashboard, name="Dashboard"),
    path("login", views.auth, name="Login"),
    path("logout", views.logout, name="Logout"),
]

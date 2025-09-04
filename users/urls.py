from django.urls import path
from .views import register, login, profile
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    # path("register/", register),
    path("login/", views.login, name="login"),
    # path("login/", login),
    path("profile/", views.profile, name="profile"),
    # path("profile/", me),
]
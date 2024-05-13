from .views import login, signup, logout_user
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("login", login, name="login"),
    path("signup", signup, name="signup"),
    path("logout", logout_user, name="logout"),
]

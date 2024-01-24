from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from . import views

app_name = "ngusers"
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.user_login, name="login"),
    path("register/", views.verify_email, name="register"),
    path("set_password/<str:email>", views.set_password, name="set_password"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("update_picture/", views.update_picture, name="update_picture"),
]

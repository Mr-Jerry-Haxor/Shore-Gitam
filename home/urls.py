from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("login/", views.login, name='login'),
    path("signup/", views.signup, name='signup'),
    path("festpass/", views.festpass, name='festpass'),
]
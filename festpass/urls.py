from django.urls import path
from . import views


urlpatterns = [
    path("", views.passhome, name="passhome"),
    path("shoreidcard", views.shoreidcard, name="shoreidcard"),
]

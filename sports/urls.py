from django.urls import path
from . import views

app_name = "sports"
urlpatterns = [
    path("", views.matches, name="matches"),
    path("points/", views.points, name="points"),
]

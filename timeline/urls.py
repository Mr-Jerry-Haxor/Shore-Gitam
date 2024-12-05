from django.urls import path
from . import views

app_name = "timeline"
urlpatterns = [
    path("", views.index, name="index"),
    path("Day/<str:day_no>", views.timeline, name="timeline"),
]

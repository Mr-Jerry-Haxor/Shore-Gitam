from django.urls import path
from . import views

app_name = "hospitality"

urlpatterns = [
    path("", views.home, name="home"),
    path("food_qr/", views.food, name="food_qr"),
    path("user_history/", views.user_history, name="user_history"),
    path("scan/", views.scan, name="scan"),
    path("adduser/", views.add_hospitality_user, name="add_user"),
    path("checkInOut/", views.checkInOutHome, name="checkInOutHome"),
    path("checkInOutForm/<str:email>", views.checkInOutForm, name="checkInOutForm"),
    path("checkInOutHistory/", views.checkInOutHistory, name="checkInOutHistory"),
    path("admin_history/<str:date>", views.admin_history, name="admin_history"),
    path("upload_NOC/", views.noc_and_travel_tickets, name="hospitalitynoc"),

    path("add_student/", views.add_student, name="add_student"),
]

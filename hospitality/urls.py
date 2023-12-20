from django.urls import path
from . import views

app_name = "hospitality"

urlpatterns = [
    path("", views.home, name="home"),
    path("food_qr/", views.food, name="food_qr"),
    path("user_history/", views.user_history, name="user_history"),
    path("scan/", views.scan, name="scan"),
    path("checkInOut/", views.checkInOutHome, name="checkInOutHome"),
    path("checkInOutForm/<str:email>", views.checkInOutForm, name="checkInOutForm"),
    path("checkInOutHistory/", views.checkInOutHistory, name="checkInOutHistory"),
    path("admin_history/<str:date>", views.admin_history, name="admin_history"),
]

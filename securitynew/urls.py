from django.urls import path
from . import views

app_name = "securitynew"
urlpatterns = [
    path("", views.home, name="home"),
    path("scan_qr", views.scan_qr, name="scan_qr"),
    path("view_user/<str:passhash>", views.view_user, name="view_user"),
    path("accept_user/<str:passhash>", views.accept_user, name="accept_user"),
]
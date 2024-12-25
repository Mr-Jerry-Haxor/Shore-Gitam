from django.urls import path
from . import views

urlpatterns = [
    path("bgmi", views.bgmi_player, name="bgmireg"),
    path("volunteer", views.volunteer_registration, name="volunteer"),
    path("noc_and_tickets", views.noc, name="noc_and_tickets"),

    path("send_emails/", views.send_volunteer_emails),
]

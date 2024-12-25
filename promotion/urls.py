from django.urls import path
from . import views

urlpatterns = [
    path("bgmi", views.bgmi_player, name="bgmireg"),
    path("volunteer", views.volunteer_registration, name="volunteer"),
    path("noc_and_tickets", views.noc, name="noc_and_tickets"),
    path("volunteer_dashboard", views.volunteer_dashboard, name="volunteer_dashboard"),
    path("volunteer_accept/<str:email>", views.volunteer_accept, name="volunteer_accept"),
    # path("volunteer_reject/<str:email>", views.volunteer_reject, name="volunteer_reject"),
]

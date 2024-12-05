from django.urls import path
from . import views

app_name = "grievance"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("raise/", views.raise_ticket, name="raise_ticket"),
    path("update/<str:ticket_hash>", views.update_ticket, name="update_ticket"),
]

from django.urls import path
from . import views

app_name = "teams"
urlpatterns = [
    path("", views.team, name="team"),
    path("apply/", views.apply, name="apply"),
    path("view/", views.view_application, name="view_application"),
    path("verify/", views.verify_application, name="verify_application"),
    path(
        "verify_application/<str:domain_id>/<str:email>",
        views.verify_individual_application,
        name="verify_individual_application",
    ),
    path(
        "disprove_application/<str:domain_id>/<str:email>",
        views.disprove_individual_application,
        name="disprove_individual_application",
    ),
]

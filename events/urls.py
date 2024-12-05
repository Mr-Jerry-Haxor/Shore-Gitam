from django.urls import path
from . import views

app_name = "events"
urlpatterns = [
    path("", views.event_home, name="eventshome"),  # URL Working, guidelines not added
    path("sports/", views.sports_home, name="sports_home"),  # URL Working
    path("culturals/", views.culturals_home, name="culturals_home"),  # URL Working
    path(
        "select_college/<str:sport_name>", views.selectCollege, name="selectCollege"
    ),  # URL Working
    path("register/<str:sport_name>", views.register, name="register"),  # URL Working
    path("addCollege/", views.addCollege, name="addCollege"),
    path("addEvent/", views.addEvent, name="addEvent"),
    path("success/<str:team_hash>", views.success, name="success"),
    path(
        "registered_sports/<str:sport_name>",
        views.registered_sports,
        name="registered_sports",
    ),
    path(
        "registered_culturals/<str:sport_name>",
        views.registered_culturals,
        name="registered_culturals",
    ),
    path("view_team/<str:team_hash>", views.view_team, name="view_team"),
    path(
        "sports/registered_teams", views.events_admin_sports, name="events_admin_sports"
    ),
    path(
        "culturals/registered_teams",
        views.events_admin_culturals,
        name="events_admin_culturals",
    ),
    # hackathon urls
    path("hackathon/", views.hackathon_home, name="hackathon_home"),  # URL Working
    path(
        "hackathon/selectCollege/<str:hackathon_name>",
        views.select_hackathon_college,
        name="hackathon_selectCollege",
    ),  # URL Working
    path(
        "hackathon/register/<str:hackathon_name>",
        views.register_hackathon,
        name="hackathon_register",
    ),  # URL Working
    path(
        "hackathon/success/<str:team_hash>",
        views.hackathon_success,
        name="hackathon_success",
    ),  # URL Working
    path("hackathon/registered_teams", views.hackathon_admin, name="hackathon_admin"),
    path(
        "hackathon/view_team/<str:team_hash>",
        views.view_hackathon_team,
        name="view_hackathon_team",
    ),
]

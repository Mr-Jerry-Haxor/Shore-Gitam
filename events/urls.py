from django.urls import path
from . import views

app_name = "events"
urlpatterns = [
    path("", views.event_home, name="eventshome"),
    path("sports/", views.sports_home, name="sports_home"),
    path("culturals/", views.culturals_home, name="culturals_home"),
    path("select_college/<str:sport_name>", views.selectCollege, name="selectCollege"),
    path("register/<str:sport_name>", views.register, name="register"),
    path("addCollege/", views.addCollege, name="addCollege"),
    path("addEvent/", views.addEvent, name="addEvent"),
    path("success/<str:team_hash>", views.success, name="success"),
    path("registered_sports/", views.registered_sports, name="registered_sports"),
    path("registered_culturals/", views.registered_culturals, name="registered_culturals"),
    path("view_team/<str:team_hash>", views.view_team, name="view_team"),
]

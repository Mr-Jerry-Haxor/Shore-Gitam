from django.urls import path
from . import views

app_name = "prelims"
urlpatterns = [
    path("", views.prelims_closed, name="prelims_closed"),

    path("home/", views.culturals_home, name="home"),
    path("register/<str:event_name>/", views.prelims_closed, name="register"),
    # path("register/<str:event_name>/", views.register, name="register"),
    
    # path(
    #     "registered_events/", views.registered_events, name="prelims_registered_events"
    # ),
    # path("view_teams/<str:event_name>/", views.view_teams, name="prelims_view_teams"),
    # path("view_team/<str:team_hash>", views.view_team, name="prelims_view_team"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "prelimsadmin/", views.prelims_admin_dashboard, name="prelims_admin_dashboard"
    ),
    path("uploadfile/<str:team_hash>/", views.upload_file, name="upload_file"),
]

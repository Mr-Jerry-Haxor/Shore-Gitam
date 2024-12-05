from django.urls import path
from . import views

app_name = "production_admin"
urlpatterns = [
    path("", views.index, name="index"),
    path("pull_and_restart/", views.pull_and_restart, name="pull_and_restart"),
    path(
        "migrate_database/<str:app_name>/",
        views.migrate_database,
        name="migrate_database",
    ),
    path("run-command/", views.run_command, name="run_command"),
    path("add-campus/", views.add_campus_to_teams_prelims),
    # path("change-usernames/", views.change_username, name="change_username"),
    # path("send_festpasspurchase_emails/", views.send_festpasspurchase_emails, name="send_festpasspurchase_emails"),
    # path("remove_prebooking/", views.remove_prebooking, name="remove_prebooking"),
]

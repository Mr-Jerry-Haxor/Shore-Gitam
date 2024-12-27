from django.urls import path
from .views import *


urlpatterns = [
    path("tasks/<str:domain_name>", coretasks, name="coretasks"),
    path("", home, name="corehome"),
    path("createtask/<str:domain_name>/", createtask, name="createtask"),
    path("edittask/<str:domain_name>/<int:taskid>", edit_task, name="edittask"),
    path("submit_task/<int:task_id>", submit_task, name="submit_task"),
    path(
        "remove_submission/<int:task_id>", remove_submission, name="remove_submission"
    ),

    
    path("domain_heads/", give_access_to_domain_head, name="domain_heads"),
    path("add_domain_leads/", add_domain_leads, name="add_domain_leads"),
]

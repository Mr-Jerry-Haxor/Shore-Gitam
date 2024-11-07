from django.urls import path
from .views import *


urlpatterns = [
    path("tasks/<str:domain_name>", coretasks, name="coretasks"),
    path("", home, name="corehome"),
    path("createtask/<str:domain_name>/", createtask, name="createtask"),
    path("edittask/<str:domain_name>/<int:taskid>", edit_task, name="edittask"),
]

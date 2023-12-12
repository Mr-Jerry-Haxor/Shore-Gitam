from django.urls import path 
from .views import *


urlpatterns = [
    path('tasks/<str:domain_name>' , coretasks , name='coretasks'),
    path('',home  , name='home'),
    path('createtask/<str:domain_name>/', createtask , name="createtask"),
]



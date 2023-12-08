from django.urls import path 
from .views import *


urlpatterns = [
    path('' , coreindex , name='coreindex'),
    path('home/',home  , name='home'),
]



from django.urls import path 
from .views import *


urlpatterns = [
    path('' , index , name='test'),
    path('25/', test , name='index'),
]
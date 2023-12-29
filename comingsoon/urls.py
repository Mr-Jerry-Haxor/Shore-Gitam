from django.urls import path 
from .views import *


urlpatterns = [
    path('24/' , index , name='index'),
    path('', test , name='test'),
]
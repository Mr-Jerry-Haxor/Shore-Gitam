from django.urls import path 
from .views import *


urlpatterns = [
    path('24/' , index , name='test'),
    path('', test , name='index'),
]
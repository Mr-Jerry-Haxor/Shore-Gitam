from django.urls import path
from . import views

urlpatterns = [
    path('bgmi', views.bgmi_player, name='bgmireg'),
    path('volunteer' , views.volunteer_registration, name='volunteer'),
    path('noc_and_tickets_test', views.noc_and_travel_tickets , name='noc_and_tickets'),
]
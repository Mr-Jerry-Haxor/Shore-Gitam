from django.urls import path
from . import views

urlpatterns = [
    path('bgmi', views.bgmi_player, name='bgmireg'),
    path('volunteer' , views.volunteer_registration, name='volunteer'),
]
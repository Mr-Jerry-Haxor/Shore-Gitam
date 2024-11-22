from django.urls import path
from . import views


urlpatterns = [
    path('', views.security_home, name='securityhome'),
    path('festpass_scan/' , views.festpass_scan , name='festpass_scan'),
    path('festpass_scan1/' , views.festpass_scan1 , name='festpass_scan1'),
    path('festverify/', views.festpass_verify, name='festpassverify'),
    path('maingate/' , views.maingate_scan , name='maingate_scan'),
    path('maingate1/' , views.maingate_scan1 , name='maingate_scan1'),
    path('maingateverify/', views.maingate_verify, name='maingateverify'),
    path('cokescan/', views.coke_scan , name='cokescan'),
]
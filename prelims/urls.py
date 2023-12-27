from django.urls import path
from . import views

# app_name = "prelims"
urlpatterns = [
    path("", views.culturals_home, name="culturals_home"),
    path("register/<str:event_name>/", views.register, name="prelimsregister"),
    path("registered_events/", views.registered_events, name="prelims_registered_events"),
]

from django.urls import path
from .views import *


urlpatterns = [
    path("", index, name="index"),
    path("25/", test, name="index1"),
]

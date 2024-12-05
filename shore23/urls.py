from django.urls import path
from .views import *


urlpatterns = [
    path("", index, name="shore23"),
    path("sponsors/", sponsors, name="shore23sponsors"),
]

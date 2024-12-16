"""
URL configuration for shore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import render

def opening_soon(request):
    return render(request, "prelims/opening_soon.html")



urlpatterns = [
    path("shoreadmin/", admin.site.urls, name="django_admin"),
    # path('logout/', auth_views.LogoutView.as_view(),name='logout'),
    path("auth/", include("social_django.urls", namespace="social")),
    path("comingsoon/", include("comingsoon.urls")),
    path("coreteam/", include("coreteam.urls")),
    # path('shore23/' , include('shore23.urls')),
    path("hospitality/", include("hospitality.urls")),
    path("prelims/", include("prelims.urls")),
    path("preshore/", include("promotion.urls")),
    path("registrations/", include("events.urls")),
    # path("registrations/", opening_soon),
    # path('festpass/' , include('festpass.urls')),
    path("sports/", include("sports.urls")),
    path("users/", include("ngusers.urls")),
    path("team/", include("teams.urls")),
    path("security/", include("security.urls")),
    path("timeline/", include("timeline.urls")),
    path("productionadmin/", include("production_admin.urls")),
    path("", include("home.urls")),
    path("grievance/", include("grievance.urls")),
    # path("competitions/", include("competition.urls")),
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    settings.DEBUG = True
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    settings.DEBUG = False

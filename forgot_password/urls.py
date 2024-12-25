from django.urls import path
from django.views.generic.base import TemplateView
from .views import *

urlpatterns = [
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_done/', TemplateView.as_view(template_name="forgot_password/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_complete/', TemplateView.as_view(template_name="forgot_password/password_reset_complete.html"), name='password_reset_complete'),
]
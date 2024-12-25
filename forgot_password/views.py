from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from .forms import *


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'forgot_password/password_reset_form.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'forgot_password/password_reset_confirm.html'

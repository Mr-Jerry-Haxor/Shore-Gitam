from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from .forms import CustomPasswordResetForm, CustomSetPasswordForm


class CustomPasswordResetView(PasswordResetView):
    """
    Handles the password reset functionality.
    Users will receive a password reset email if they exist and are active.
    """
    form_class = CustomPasswordResetForm
    template_name = 'forgot_password/password_reset_form.html'
    success_url = '/password-reset-done/'  # Redirect to a 'password reset done' page


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Handles the password reset confirmation.
    Users can set a new password using the link provided in the email.
    """
    form_class = CustomSetPasswordForm
    template_name = 'forgot_password/password_reset_confirm.html'
    success_url = '/password-reset-complete/'  # Redirect to a 'password reset complete' page

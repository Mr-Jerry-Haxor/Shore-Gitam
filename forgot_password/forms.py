from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from coreteam.models import CustomUser

class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        active_users = CustomUser.objects.filter(email=email, is_active=True)
        return (user for user in active_users if user.has_usable_password())
    

class CustomSetPasswordForm(SetPasswordForm):
    pass

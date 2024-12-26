from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from coreteam.models import CustomUser

class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        # Case-insensitive email matching
        email_field_name = CustomUser.get_email_field_name()
        active_users = CustomUser.objects.filter(
            **{f'{email_field_name}__iexact': email},
            is_active=True
        )
        return (user for user in active_users if user.has_usable_password())
    

class CustomSetPasswordForm(SetPasswordForm):
    pass

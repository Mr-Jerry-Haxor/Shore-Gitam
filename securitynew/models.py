from django.db import models
from coreteam.models import CustomUser

class UserIn(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, unique=True)
    in_time = models.DateTimeField(auto_now=True)
    is_user_in = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.email:  # Check if email is not already set
            self.email = self.user.email  # Autofill email with user's email
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return self.user.name


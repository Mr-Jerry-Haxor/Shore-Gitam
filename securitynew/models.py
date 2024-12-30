from django.db import models
from coreteam.models import CustomUser

class UserIn(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    in_time = models.DateTimeField(auto_now=True)
    is_user_in = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name


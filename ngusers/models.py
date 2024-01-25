from typing import Any
from django.db import models


class AllowedParticipants(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    otp = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.email


class ProfilePicUpdated(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    updated = models.BooleanField(default=False)

    def __str__(self):
        return self.email

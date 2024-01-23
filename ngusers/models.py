from typing import Any
from django.db import models


class AllowedParticipants(models.Model):
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.email

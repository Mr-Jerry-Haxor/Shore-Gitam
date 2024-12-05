from django import forms
from django.contrib.auth.forms import UserCreationForm
from coreteam.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "password"]

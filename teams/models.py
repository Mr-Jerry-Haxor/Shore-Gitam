import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from urllib.parse import urlparse


def upload_profile_pic(instance, filename):
    current_datetime = timezone.now().strftime('%Y%m%d%H%M%S')
    ext = filename.split('.')[-1]
    new_filename = f"{instance.name}__{current_datetime}.{ext}"
    domain_folder = f"Team/"
    return os.path.join(domain_folder, new_filename)


class Domain(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    head_email = models.CharField(max_length=500, null=False, blank=False)
    order = models.IntegerField(unique=True, null=False, blank=False)

    def __str__(self) -> str:
        return self.name


class ParticipantApplication(models.Model):
    position_choices = [
        ("President", "President"),
        ("Vice-President", "Vice-President"),
        ("Event Manager", "Event Manager"),
        ("Head", "Head"),
        ("Co-head", "Co-head"),
        ("Lead", "Lead"),
        ("Co-lead", "Co-lead"),
        ("Member", "Member"),
    ]

    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    profile_pic = models.ImageField(upload_to=upload_profile_pic, null=False, blank=False)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=False, blank=False)
    position = models.CharField(max_length=100, choices=position_choices, null=False, blank=False)
    designation = models.CharField(max_length=100, null=False, blank=False)
    instagram_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def clean_url(self):
        if not self.linkedin_url or self.instagram_url:
            return
        try:
            result = urlparse(self.linkedin_url)
            if result.scheme != 'https' and result.scheme != 'http':
                raise ValidationError(
                    'Invalid LinkedIn URL. Please provide a valid URL starting with "http" or "https"'
                )
        except Exception as e:
            raise ValidationError("Invalid LinkedIn URL. ")

        try:
            result = urlparse(self.instagram_url)
            if result.scheme != 'https' and result.scheme != 'http':
                raise ValidationError(
                    'Invalid Instagram URL. Please provide a valid URL starting with "http" or "https"'
                )
        except Exception as e:
            raise ValidationError("Invalid Instagram URL. ")

    def validate_email(self):
        if not (self.email.endswith('@gitam.edu')
                or self.email.endswith('@gitam.in')):
            raise ValidationError("Please enter a vald Gitam email address.")

    def clean(self):
        super().clean()
        self.clean_url()
        self.validate_email()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

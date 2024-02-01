from django.db import models
from django.utils import timezone
import os

def profilepic_upload_path(instance, filename):
    current_datetime = timezone.now().strftime('%Y%m%d%H%M%S')
    ext = filename.split('.')[-1]
    new_filename = f"{instance.name}__{instance.regno}__{current_datetime}.{ext}"
    domain_folder = f"Festpass/"
    return os.path.join(domain_folder, new_filename)

class Student(models.Model):

    CAMPUS_CHOICES = (
        ('Visakhapatnam', 'Visakhapatnam'),
        ('Hyderabad', 'Hyderabad'),
        ('Bengaluru', 'Bangalore'),  # Updated choice spelling
    )

    name = models.CharField(max_length=100)
    regno = models.CharField(max_length=30 , blank=True , null=True)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=50)
    year_of_study = models.CharField(max_length=20)
    branch = models.CharField(max_length=100)
    institute = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    campus = models.CharField(max_length=100, choices=CAMPUS_CHOICES)
    hosteler = models.BooleanField(default=False)
    ispaid = models.BooleanField(default=False)
    isrejected = models.BooleanField(default=False)
    rejected_reason = models.TextField(blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    passhash = models.CharField(max_length=100, blank=True , null=True)
    profile_picture = models.ImageField(upload_to=profilepic_upload_path, null=True, blank=True)
    registred_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name


class participants_list(models.Model):
    emails = models.EmailField(unique=True)
    festpass = models.BooleanField(default=False)
    notfree = models.BooleanField(default=False)
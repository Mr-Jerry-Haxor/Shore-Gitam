from django.utils import timezone
import os
from django.db import models

class BGMIPlayer(models.Model):
    name = models.CharField(max_length=100)
    userid = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    regno = models.CharField(max_length=100)
    yearofstudy = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)



from django.db import models


def profilepic_upload_path(instance, filename):
    current_datetime = timezone.now().strftime('%Y%m%d%H%M%S')
    ext = filename.split('.')[-1]
    new_filename = f"{instance.name}__{instance.regno}__{current_datetime}.{ext}"
    domain_folder = f"volunteer/"
    return os.path.join(domain_folder, new_filename)

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    regno = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    year_of_study =  models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    institute = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    Campus = models.CharField(max_length=50)
    ishosteler = models.BooleanField(default=False)
    previous_experience = models.TextField()
    availability = models.TextField()
    why_you_interested = models.TextField()
    tshirt_size = models.CharField(max_length=30)
    domain_of_interest = models.CharField(max_length=150)
    isvolunteer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to=profilepic_upload_path)

    def __str__(self):
        return f"{self.name}"



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




from django.db import models
from django.utils import timezone
import os

def participant_noc_file_path(instance, filename):
    return f'participants_noc/noc/{instance.full_name}_{instance.event_type}_{instance.event_name}_{timezone.now().strftime("%Y%m%d%H%M%S")}.{filename.split(".")[-1]}'

def travel_ticket_file_path(instance, filename):
    return f'participants_noc/ticket/{instance.full_name}_{instance.event_type}_{instance.event_name}_{timezone.now().strftime("%Y%m%d%H%M%S")}.{filename.split(".")[-1]}'

def profile_pic_file_path(instance, filename):
    return f'participants_noc/profile_pic/{instance.full_name}_{instance.event_type}_{instance.event_name}_{timezone.now().strftime("%Y%m%d%H%M%S")}.{filename.split(".")[-1]}'

class ParticipantsNOC(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    regno = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Others')])
    yearofstudy = models.CharField(max_length=20, choices=[('First year', '1st Year'), ('Second year', '2nd Year'), ('Third year', '3rd Year'), ('Forth year', '4th Year'), ('Fifth year', '5th Year'), ('Sixth year', '6th Year'), ('Alumni', 'Alumni'), ('Other', 'Other')])
    branch = models.CharField(max_length=150)
    institute = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    campus = models.CharField(max_length=150)
    hosteler = models.CharField(max_length=50)
    eventtype = models.CharField(max_length=50, choices=[('Cultural', 'Cultural'), ('Sports', 'Sports'), ('Technical', 'Technical'), ('DOS/DOSL', 'DOS/DOSL')])
    eventname = models.CharField(max_length=255)
    teamname = models.CharField(max_length=255)
    tshirt = models.CharField(max_length=15, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('Other', 'Other')])
    accomodation = models.CharField(max_length=20, choices=[('NO', 'No'), ('YES', 'Yes')])
    travelling = models.CharField(max_length=50)
    departure = models.CharField(max_length=255, blank=True, null=True)
    arrival = models.CharField(max_length=255, blank=True, null=True)
    departureDatetime = models.DateTimeField(blank=True, null=True)
    arrivalDatetime = models.DateTimeField(blank=True, null=True)
    noc_file_input = models.FileField(upload_to=participant_noc_file_path, blank=True, null=True)
    ticket_file_input = models.FileField(upload_to=travel_ticket_file_path, blank=True, null=True)
    profile_pic = models.ImageField(upload_to=profile_pic_file_path, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

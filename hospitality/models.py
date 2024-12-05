from django.db import models

hostel_choices = (
    ("RBS", "Rabindranath Sadan"),
    ("RBS-AC", "Rabindranath Tagore Sadan AC"),
    ("VS", "Vinay Sadan"),
    ("NS", "Nirmala Sadan"),
    ("NS-AC", "Nirmala Sadan AC"),
    ("KS", "Kokila Sadan"),
    ("KS-AC", "Kokila Sadan AC"),
    ("DDS", "DDS"),
    ("DDS-AC", "DDS AC"),
    ("Nursing-hostel", "Nursing Hostel"),
)

meal_choices = (
    ("Breakfast", "Breakfast"),
    ("Lunch", "Lunch"),
    ("Hi-Tea", "Hi-Tea"),
    ("Dinner", "Dinner"),
)


class HospitalityUser(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    phone_number = models.CharField(max_length=255, null=False, unique=True)
    isfoodonly = models.BooleanField(default=False)
    meal_id = models.IntegerField(null=True, blank=True)
    qr_hash = models.CharField(max_length=255, null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)
    checkin = models.DateTimeField(null=True, blank=True)
    checkout = models.DateTimeField(null=True, blank=True)
    hostel = models.CharField(
        max_length=255, null=True, blank=True, choices=hostel_choices
    )
    room_number = models.IntegerField(null=True, blank=True)
    checkin_status = models.BooleanField(null=True, blank=True, default=False)
    checkout_status = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return self.name


class Meal(models.Model):
    meal_type = models.CharField(max_length=255, choices=meal_choices)
    date = models.DateField(auto_now=False, auto_now_add=False)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.meal_type} {self.date}"


class MealHistory(models.Model):
    user = models.ForeignKey(HospitalityUser, on_delete=models.CASCADE)
    meal_type = models.ForeignKey(Meal, on_delete=models.CASCADE)
    scanned_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} {self.meal_type.meal_type} {self.meal_type.date}"


from django.db import models
from django.utils import timezone
import os


def participant_noc_file_path(instance, filename):
    return f'participants_noc/noc/{instance.full_name}_{instance.eventtype}_{instance.eventname}_{timezone.now().strftime("%Y%m%d%H%M%S")}.{filename.split(".")[-1]}'


def travel_ticket_file_path(instance, filename):
    return f'participants_noc/ticket/{instance.full_name}_{instance.eventtype}_{instance.eventname}_{timezone.now().strftime("%Y%m%d%H%M%S")}.{filename.split(".")[-1]}'


def profile_pic_file_path(instance, filename):
    return f'participants_noc/profile_pic/{instance.full_name}_{instance.eventtype}_{instance.eventname}_{timezone.now().strftime("%Y%m%d%H%M%S")}.{filename.split(".")[-1]}'


class ParticipantsNOC(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=False)
    phone_number = models.CharField(max_length=15)
    regno = models.CharField(max_length=20)
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Others")],
    )
    yearofstudy = models.CharField(
        max_length=20,
        choices=[
            ("First year", "1st Year"),
            ("Second year", "2nd Year"),
            ("Third year", "3rd Year"),
            ("Forth year", "4th Year"),
            ("Fifth year", "5th Year"),
            ("Sixth year", "6th Year"),
            ("Alumni", "Alumni"),
            ("Other", "Other"),
        ],
    )
    branch = models.CharField(max_length=150)
    institute = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    campus = models.CharField(max_length=150)
    hosteler = models.CharField(max_length=50)
    eventtype = models.CharField(
        max_length=50,
        choices=[
            ("Cultural", "Cultural"),
            ("Sports", "Sports"),
            ("Technical", "Technical"),
            ("DOS/DOSL", "DOS/DOSL"),
        ],
    )
    eventname = models.CharField(max_length=255)
    teamname = models.CharField(max_length=255)
    tshirt = models.CharField(
        max_length=15,
        choices=[
            ("XS", "XS"),
            ("S", "S"),
            ("M", "M"),
            ("L", "L"),
            ("XL", "XL"),
            ("XXL", "XXL"),
            ("Other", "Other"),
        ],
        blank=True,
        null=True,
    )
    accomodation = models.CharField(
        max_length=20, choices=[("NO", "No"), ("YES", "Yes")]
    )
    travelling = models.CharField(max_length=50)
    departure = models.CharField(max_length=255, blank=True, null=True)
    arrival = models.CharField(max_length=255, blank=True, null=True)
    departureDatetime = models.DateTimeField(blank=True, null=True)
    arrivalDatetime = models.DateTimeField(blank=True, null=True)
    noc_file_input = models.FileField(
        upload_to=participant_noc_file_path, blank=True, null=True
    )
    ticket_file_input = models.FileField(
        upload_to=travel_ticket_file_path, blank=True, null=True
    )
    profile_pic = models.ImageField(
        upload_to=profile_pic_file_path, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

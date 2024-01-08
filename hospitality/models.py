from django.db import models

hostel_choices = (
    ("RBS", "Rabindranath Sadan"),
    ("RBS-AC", "Rabindranath Tagore Sadan AC"),
    ("VS", "Vinay Sadan"),
    ("NS", "Nirmala Sadan"),
    ("NS-AC", "Nirmala Sadan AC"),
    ("KS", "Kokila Sadan"),
    ("KS-AC", "Kokila Sadan AC"),
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
    phone_number = models.CharField(max_length=255, null=False, unique=True)  # length should be 10
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

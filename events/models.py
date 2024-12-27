import hashlib
import os
from django.db import models
from django.utils import timezone


status_choices = (
    ("pending", "pending"),
    ("approved", "approved"),
    ("rejected", "rejected"),
    ("eligible_for_payment", "Eligible for payment"),
)

event_choices = (("sports", "sports"), ("cultural", "cultural"))


def generate_md5(user_string):
    hashed_string = hashlib.md5(user_string.encode("UTF-8"))
    return hashed_string.hexdigest()


def event_file_upload_path(instance, filename):
    # Get the current date and time
    current_datetime = timezone.now().strftime("%Y%m%d%H%M%S")
    ext = filename.split(".")[-1]
    new_filename = f"{instance.name}__{instance.event_type}__{current_datetime}.{ext}"
    domain_folder = f"EventsRegistrations/events/{instance.event_type}"
    return os.path.join(domain_folder, new_filename)


def file_upload_path(instance, filename):
    # Get the current date and time
    current_datetime = timezone.now().strftime("%Y%m%d%H%M%S")

    # Extracting the file extension
    ext = filename.split(".")[-1]

    # Constructing the new file name
    new_filename = f"{instance.visible_name}__{instance.college.name}__{instance.sport.name}__{current_datetime}.{ext}"

    # Constructing the file path
    domain_folder = f"EventsRegistrations/{instance.sport.name}/{instance.college.name}"
    return os.path.join(domain_folder, new_filename)


def noc_file_upload_path(instance, filename):
    current_datetime = timezone.now().strftime("%Y%m%d%H%M%S")
    ext = filename.split(".")[-1]
    new_filename = f"{instance.name}__NOC__{instance.college.name}__{instance.sport.name}__{current_datetime}.{ext}"
    domain_folder = f"EventsRegistrations/{instance.sport.name}/{instance.college.name}"
    return os.path.join(domain_folder, new_filename)


# hackathon model
hackathon_choices = (("hackathon", "hackathon"),)


def file_upload_path_hackthon(instance, filename):
    current_datetime = timezone.now().strftime("%Y%m%d%H%M%S")
    ext = filename.split(".")[-1]
    new_filename = f"{instance.visible_name}__{instance.college.name}__{instance.hackathon.name}__{current_datetime}.{ext}"
    domain_folder = (
        f"EventsRegistrations/{instance.hackathon.name}/{instance.college.name}"
    )
    return os.path.join(domain_folder, new_filename)


def Hackathon_noc_file_upload_path(instance, filename):
    current_datetime = timezone.now().strftime("%Y%m%d%H%M%S")
    ext = filename.split(".")[-1]
    new_filename = f"{instance.name}__NOC__{instance.college.name}__{instance.hackathon.name}__{current_datetime}.{ext}"
    domain_folder = (
        f"EventsRegistrations/{instance.hackathon.name}/{instance.college.name}"
    )
    return os.path.join(domain_folder, new_filename)


class College(models.Model):
    college_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=20, unique=True)
    passkey = models.CharField(max_length=100, null=True, blank=True, unique=True)
    emails = models.TextField(null=True, blank=True)
    tosend = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Replace spaces with underscores and capitalize letters
        self.abbreviation = self.abbreviation.replace(" ", "_").upper()
        super(College, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=300, null=True, blank=True)
    ticket_price = models.IntegerField()
    event_type = models.CharField(
        max_length=100, null=False, blank=False, choices=event_choices
    )
    guidelines_url = models.URLField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to=event_file_upload_path, null=True, blank=True)
    event_venue = models.CharField(max_length=255, default="ABCD")
    event_time = models.TimeField(null=True, blank=True)
    event_start_date = models.DateField(null=True, blank=True)
    event_end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    no_of_teams = models.IntegerField(null=False, blank=False)
    max_univeristy_teams = models.IntegerField(null=False, blank=False)
    min_team_size = models.IntegerField(null=False, blank=False)
    max_team_size = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100, null=False, blank=False)
    visible_name = models.CharField(
        max_length=100, unique=True, null=False, blank=False
    )
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    sport = models.ForeignKey(Event, on_delete=models.CASCADE)
    isPaid = models.BooleanField(default=False)
    isWaiting = models.BooleanField(default=False)
    registered_at = models.DateTimeField(default=timezone.now)
    team_hash = models.CharField(max_length=100, null=True, blank=True)
    endorsment_file = models.FileField(
        upload_to=file_upload_path, null=True, blank=True
    )
    noc_file = models.FileField(upload_to=file_upload_path, null=True, blank=True)
    status = models.CharField(choices=status_choices, default="pending", max_length=50)
    participant_count = models.IntegerField(default=0)

    participants = models.ManyToManyField(
        "Participants", related_name="participant_teams"
    )

    def __str__(self):
        return self.visible_name

    def save(self, *args, **kwargs):
        if not self.pk:
            # generate team hash using visiblie_name and registered time
            self.team_hash = generate_md5(self.visible_name + str(self.registered_at))
        
        # Update participant count if the team already exists
        if self.pk:
            self.participant_count = self.team_participants.count()
            
        super().save(*args, **kwargs)


class Participants(models.Model):
    participant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=False)
    phone_number = models.CharField(
        max_length=10, null=False, blank=False, unique=False
    )
    accomdation = models.BooleanField(default=False)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    sport = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="team_participants"
    )
    isCaptain = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)
    isGitamite = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    shoreid = models.CharField(max_length=100, null=True, blank=True)
    nocFile = models.FileField(upload_to=noc_file_upload_path, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.email.endswith("@gitam.in"):
            self.isGitamite = True
        else:
            self.isGitamite = False

        super().save(*args, **kwargs)


class Hackathon(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    ticket_price = models.IntegerField()
    event_type = models.CharField(
        max_length=100, null=False, blank=False, choices=hackathon_choices
    )
    guidelines_url = models.URLField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to=event_file_upload_path, null=True, blank=True)
    event_venue = models.CharField(max_length=255, default="ABCD")
    event_time = models.TimeField(null=True, blank=True)
    event_start_date = models.DateField(null=True, blank=True)
    event_end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    no_of_teams = models.IntegerField(null=False, blank=False)
    max_univeristy_teams = models.IntegerField(null=False, blank=False)
    min_team_size = models.IntegerField(null=False, blank=False)
    max_team_size = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name


# hackathon team
class HackathonTeam(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100, null=False, blank=False)
    visible_name = models.CharField(
        max_length=100, unique=True, null=False, blank=False
    )
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    isPaid = models.BooleanField(default=False)
    isQualified = models.BooleanField(default=False)
    registered_at = models.DateTimeField(default=timezone.now)
    team_hash = models.CharField(max_length=100, null=True, blank=True)
    endorsment_file = models.FileField(
        upload_to=file_upload_path_hackthon, null=True, blank=True
    )
    noc_file = models.FileField(
        upload_to=file_upload_path_hackthon, null=True, blank=True
    )
    status = models.CharField(choices=status_choices, default="pending", max_length=50)

    def __str__(self):
        return self.visible_name

    def save(self, *args, **kwargs):
        # generate team hash using visiblie_name and registered time
        self.team_hash = generate_md5(self.visible_name + str(self.registered_at))
        super().save(*args, **kwargs)


# hackathon participants
class HackathonParticipants(models.Model):
    participant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    phone_number = models.CharField(max_length=10, null=False, blank=False, unique=True)
    accomdation = models.BooleanField(default=False)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    team = models.ForeignKey(HackathonTeam, on_delete=models.CASCADE)
    isCaptain = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)
    isGitamite = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    shoreid = models.CharField(max_length=100, null=True, blank=True)
    nocFile = models.FileField(
        upload_to=Hackathon_noc_file_upload_path, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.email.endswith("@gitam.in"):
            self.isGitamite = True
        else:
            self.isGitamite = False

        super().save(*args, **kwargs)

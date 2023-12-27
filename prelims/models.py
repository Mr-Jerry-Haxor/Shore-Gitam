from django.db import models

event_choices = (
    ("culturals", "culturals"),
)

campus_choices = (
    ("gitam_vzg", "GITAM Visakhapatnam"),
    ("gitam_hyd", "GITAM Hyderabad"),
    ("gitam_blr", "GITAM Bangalore"),
)


class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    event_type = models.CharField(
        max_length=100, null=False, blank=False, choices=event_choices
    )
    description = models.TextField(null=True, blank=True)
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    min_team_size = models.IntegerField(null=False, blank=False)
    max_team_size = models.IntegerField(null=False, blank=False)
    venue = models.CharField(max_length=100, null=True, blank=True)
    event_guidelines = models.TextField(null=True, blank=True)
    event_image = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    visible_name = models.CharField(
        max_length=100, unique=True, null=False, blank=False
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    captain_email = models.EmailField(null=False, blank=False)
    registered_at = models.DateTimeField(auto_now=True)
    reference_attatchment = models.FileField(
        upload_to="prelims_files/", null=True, blank=True
    )
    teammates = models.TextField(null=False, blank=True, max_length=5000)

    def __str__(self):
        return self.visible_name


class Participant(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone_number = models.CharField(max_length=10, null=False, blank=False)
    registration_number = models.CharField(
        max_length=100, null=True, blank=True
    )
    campus = models.CharField(
        max_length=100, null=False, blank=False, choices=campus_choices
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    isCaptain = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

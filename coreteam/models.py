from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.
# models.py (inside your custom user app)
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    president = models.BooleanField(default=False)
    vice_president = models.BooleanField(default=False)
    technology = models.BooleanField(default=False)
    events_cultural = models.BooleanField(default=False)
    events_sports = models.BooleanField(default=False)
    legal = models.BooleanField(default=False)
    operations = models.BooleanField(default=False)
    marketing = models.BooleanField(default=False)
    sponsorship = models.BooleanField(default=False)
    design = models.BooleanField(default=False)
    finance = models.BooleanField(default=False)
    media = models.BooleanField(default=False)
    security = models.BooleanField(default=False)
    hospitality = models.BooleanField(default=False)
    advisory = models.BooleanField(default=False)
    # Add other role fields as needed






class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    TASK_STATUSES = [
        ('todo', 'Todo'),
        ('in_progress', 'In Progress'),
        ('overdue', 'Overdue'),
        ('completed', 'Completed'),
    ]
    
    DOMAIN_CHOICES = [
        ('president', 'President'),
        ('vice-president', 'Vice President'),
        ('technology', 'Technology'),
        ('events-cultural', 'Events - Cultural'),
        ('events-sports', 'Events - Sports'),
        ('legal', 'Legal'),
        ('operations', 'Operations'),
        ('marketing', 'Marketing'),
        ('sponsorship', 'Sponsorship'),
        ('design', 'Design'),
        ('finance', 'Finance'),
        ('media', 'Media'),
        ('security', 'Security'),
        ('hospitality', 'Hospitality'),
    ]


    task_title = models.CharField(max_length=100)
    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    attached_file = models.FileField(upload_to='Taskattachments/', null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TASK_STATUSES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.CharField(max_length=100)
    assigned_by = models.CharField(max_length=100)
    advisory = models.BooleanField(default=False)

    def __str__(self):
        return self.task_title
    
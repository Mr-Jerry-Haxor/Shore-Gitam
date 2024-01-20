from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.
# models.py (inside your custom user app)
from django.contrib.auth.models import AbstractUser
import os
from django.utils import timezone

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
    hospitality_staff = models.BooleanField(default=False)
    events_cultural_staff = models.BooleanField(default=False)
    events_sports_staff = models.BooleanField(default=False)
    security_staff = models.BooleanField(default=False)
    # Add other role fields as needed   


def file_upload_path(instance, filename):
    # Get the current date and time
    current_datetime = timezone.now().strftime('%Y%m%d%H%M%S')

    # Extracting the file extension
    ext = filename.split('.')[-1]

    # Constructing the new file name
    new_filename = f"{instance.task_title}__{instance.domain}__{current_datetime}.{ext}"

    # Constructing the file path
    domain_folder = f"Taskattachments/{instance.domain}"
    return os.path.join(domain_folder, new_filename)



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
    attached_file = models.FileField(upload_to=file_upload_path, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TASK_STATUSES, default='todo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.CharField(max_length=500)
    assigned_by = models.CharField(max_length=500)
    advisory = models.BooleanField(default=False)

    def __str__(self):
        return self.task_title
    
    
    
def upload_file_to(instance, filename):

    ext = filename.split('.')[-1]
    new_filename = f"{instance.name}.{ext}"

    domain_folder = f"guidelines/"
    return os.path.join(domain_folder, new_filename)

class FileUpload(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=upload_file_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
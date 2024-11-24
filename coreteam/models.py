from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
# models.py (inside your custom user app)
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import os
from django.utils import timezone
from datetime import datetime

gender_choices = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
]


def profile_pic_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"profile_pics/{instance.first_name}__{instance.last_name}__{timestamp}.{ext}"


class CustomUser(AbstractUser):
    event_manager = models.BooleanField(default=False)
    campus_head_hyd = models.BooleanField(default=False)
    campus_head_blr = models.BooleanField(default=False)
    coordinator = models.BooleanField(default=False)
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
    isLead = models.BooleanField(default=False)
    # Add other role fields as needed

    prebooking = models.BooleanField(default=False)
    is_festpass_purchased = models.BooleanField(default=False)
    is_gitamite = models.BooleanField(default=True)
    accomdation = models.BooleanField(default=False)
    sports = models.BooleanField(default=False)

    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField( max_length=20,null=True, blank=True)
    registration_number = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=255, choices=gender_choices, blank=True, null=True)
    college = models.CharField(max_length=255, null=True, blank=True, default='GITAM University')
    year_of_study = models.CharField(max_length=255, null=True, blank=True)
    course = models.CharField(max_length=255, null=True, blank=True)
    branch = models.CharField(max_length=255, null=True, blank=True)
    campus = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=profile_pic_upload_to, blank=True, null=True)
    passhash = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [username, phone_number, age, gender, college, year_of_study, course, branch]

    def save(self, *args, **kwargs):
        # Delete old profile picture if updating with a new one
        if self.pk:
            old_user = CustomUser.objects.filter(pk=self.pk).first()
            if old_user and old_user.profile_picture != self.profile_picture:
                if old_user.profile_picture and os.path.isfile(old_user.profile_picture.path):
                    os.remove(old_user.profile_picture.path)
        
        
        super().save(*args, **kwargs)
    
    def clean(self):
        # Call the parent class's clean method
        super().clean()
        
        # Existing profile picture validation
        if self.profile_picture:
            if self.profile_picture.size > 2 * 1024 * 1024:
                raise ValidationError("The profile picture must be less than 2MB.")
            
            valid_extensions = ['png', 'jpg', 'jpeg']
            ext = os.path.splitext(self.profile_picture.name)[-1].lower().strip('.')
            if ext not in valid_extensions:
                raise ValidationError("Only PNG, JPG, and JPEG formats are allowed for the profile picture.")
        
        # Phone number validation
        if self.phone_number:
            # Convert to string to check the length and starting digit
            phone_str = str(self.phone_number)
            
            # Check if length is exactly 10 digits
            if len(phone_str) != 10:
                raise ValidationError({'phone_number': 'Phone number must be exactly 10 digits'})
            
            # Check if starts with valid digits (6,7,8,9)
            if not phone_str.startswith(('6', '7', '8', '9')):
                raise ValidationError({'phone_number': 'Phone number must start with 6, 7, 8, or 9'})
    
    def __str__(self):
        return self.email


def file_upload_path(instance, filename):
    # Get the current date and time
    current_datetime = timezone.now().strftime("%Y%m%d%H%M%S")

    # Extracting the file extension
    ext = filename.split(".")[-1]

    # Constructing the new file name
    new_filename = f"{instance.task_title}__{instance.domain}__{current_datetime}.{ext}"

    # Constructing the file path
    domain_folder = f"Taskattachments/{instance.domain}"
    return os.path.join(domain_folder, new_filename)


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]
    TASK_STATUSES = [
        ("todo", "Todo"),
        ("in_progress", "In Progress"),
        ("overdue", "Overdue"),
        ("completed", "Completed"),
    ]

    DOMAIN_CHOICES = [
        ("president", "President"),
        ("vice_president", "Vice President"),
        ("campus_head_hyd", "Campus Head - Hyderabad"),
        ("campus_head_blr", "Campus Head - Bangalore"),
        ("technology", "Technology"),
        ("events_cultural", "Events - Cultural"),
        ("events_sports", "Events - Sports"),
        ("legal", "Legal"),
        ("operations", "Operations"),
        ("marketing", "Marketing"),
        ("sponsorship", "Sponsorship"),
        ("design", "Design"),
        ("finance", "Finance"),
        ("media", "Media"),
        ("security", "Security"),
        ("hospitality", "Hospitality"),
    ]

    task_title = models.CharField(max_length=100)
    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    attached_file = models.FileField(upload_to=file_upload_path, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TASK_STATUSES, default="todo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.CharField(max_length=500)
    assigned_by = models.CharField(max_length=500)
    coordinator = models.BooleanField(default=False)
    submission_url = models.URLField(max_length=500, blank=True, null=True)
    submitted_by = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.task_title


class DomainLead(models.Model):
    DOMAIN_CHOICES = [
        ("president", "President"),
        ("vice_president", "Vice President"),
        ("campus_head_hyd", "Campus Head - Hyderabad"),
        ("campus_head_blr", "Campus Head - Bangalore"),
        ("technology", "Technology"),
        ("events_cultural", "Events - Cultural"),
        ("events_sports", "Events - Sports"),
        ("legal", "Legal"),
        ("operations", "Operations"),
        ("marketing", "Marketing"),
        ("sponsorship", "Sponsorship"),
        ("design", "Design"),
        ("finance", "Finance"),
        ("media", "Media"),
        ("security", "Security"),
        ("hospitality", "Hospitality"),
    ]

    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES)
    leads = models.CharField(max_length=500)  # csv of email ids

    def __str__(self):
        return self.domain


import os
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


def upload_file_to(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{instance.name}.{ext}"

    domain_folder = f"guidelines/"
    return os.path.join(domain_folder, new_filename)


class FileUpload(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=upload_file_to, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=FileUpload)
def file_upload_pre_delete(sender, instance, **kwargs):
    # Delete the file when the corresponding FileUpload instance is deleted
    if instance.file:
        instance.file.delete()

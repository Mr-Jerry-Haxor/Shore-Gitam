import os
from django.db import models
from django.utils import timezone


def sports_matches_file_upload_path(instance, filename):
    current_datetime = timezone.now().strftime('%Y%m%d%H%M%S')
    ext = filename.split('.')[-1]
    new_filename = f"{instance.name}__matches__{current_datetime}.{ext}"
    domain_folder = f"Sports/"
    return os.path.join(domain_folder, new_filename)


def sports_points_file_upload_path(instance, filename):
    current_datetime = timezone.now().strftime('%Y%m%d%H%M%S')
    ext = filename.split('.')[-1]
    new_filename = f"{instance.name}__points__{current_datetime}.{ext}"
    domain_folder = f"Sports/"
    return os.path.join(domain_folder, new_filename)


class Sport(models.Model):
    name = models.CharField(max_length=100)
    match_img = models.ImageField(upload_to=sports_matches_file_upload_path, null=True, blank=True)
    points_img = models.ImageField(upload_to=sports_points_file_upload_path, null=True, blank=True)
    
    def __str__(self):
        return self.name
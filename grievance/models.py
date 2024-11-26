from django.db import models
from coreteam.models import CustomUser
import os
from django.utils import timezone

from home.views import generate_md5

issue_types = (
    ('payment', 'Pending Payment Issue'),
)

issue_status = (
    ('submitted', 'Submitted'),
    ('under_review', 'Under Review'),   # no need to send mail
    # ('additonal_information_required', 'Additional Information Required'),
    ('resolved', 'Resolved'),
    ('rejected', 'Rejected'),
)


def documents_upload_to(instance, filename):
    # Construct the file name
    user_first_name = instance.user.first_name
    user_last_name = instance.user.last_name
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    file_extension = os.path.splitext(filename)[1]  # Get the file extension
    new_filename = f"{user_first_name}__{user_last_name}__{timestamp}{file_extension}"
    
    # Return the path to save the file
    return f"grievance/{new_filename}"


class Ticket(models.Model):
    ticket_hash = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    type = models.CharField(choices=issue_types, max_length=255)
    status = models.CharField(choices=issue_status, max_length=255, default=issue_status[0][0])
    utr = models.CharField(max_length=255, unique=True)
    remark = models.TextField(max_length=1000, blank=True, null=True)
    attached_documents = models.FileField(upload_to=documents_upload_to, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.user.first_name}__{self.status}"
    
    
    def save(self, *args, **kwargs):
        # Check if ticket_hash is empty
        if not self.ticket_hash:
            # Generate the hash using the id and utr
            self.ticket_hash = generate_md5(f"{self.id}{self.utr}")
        
        super().save(*args, **kwargs)  # Call the original save method



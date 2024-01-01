from django.db import models

# Create your models here.


class FestPass(models.Model):
    name = models.CharField(max_length=300, blank=True , null=True)
    mobile = models.CharField(max_length=300, blank=True , null=True)
    email = models.CharField(max_length=300, blank=True , null=True)
    gender = models.CharField(max_length=300, blank=True, null=True)
    roll_number = models.CharField(max_length=300, blank=True , null=True)
    participation_category = models.CharField(max_length=300 , blank=True , null=True)
    category = models.CharField(max_length=300, blank=True, null=True)
    participation_type = models.CharField(max_length=300, blank=True,null=True)
    faculty_or_other = models.CharField(max_length=300, blank=True, null=True)
    amount = models.CharField(max_length=300, blank=True , null=True)
    confirm_id = models.CharField(max_length=300, blank=True , null=True)
    txn_id = models.CharField(max_length=300, blank=True , null=True)
    transaction_status = models.CharField(max_length=300, blank=True , null=True)
    order_id = models.CharField(max_length=300, blank=True , null=True)
    bankref_number = models.CharField(max_length=300, blank=True , null=True)
    posted_date = models.DateTimeField(blank=True , null=True)
    updated_date = models.DateTimeField(blank=True , null=True)

    
class Registrations(models.Model):
    name = models.CharField(max_length=300, blank=True , null=True)
    mobile = models.CharField(max_length=300, blank=True , null=True)
    email = models.CharField(max_length=300, blank=True , null=True)
    gender = models.CharField(max_length=300, blank=True, null=True)
    roll_number = models.CharField(max_length=300, blank=True , null=True)
    participation_category = models.CharField(max_length=300 , blank=True , null=True)
    category = models.CharField(max_length=300, blank=True, null=True)
    participation_type = models.CharField(max_length=300, blank=True,null=True)
    faculty_or_other = models.CharField(max_length=300, blank=True, null=True)
    amount = models.CharField(max_length=300, blank=True , null=True)
    confirm_id = models.CharField(max_length=300, blank=True , null=True)
    txn_id = models.CharField(max_length=300, blank=True , null=True)
    transaction_status = models.CharField(max_length=300, blank=True , null=True)
    order_id = models.CharField(max_length=300, blank=True , null=True)
    bankref_number = models.CharField(max_length=300, blank=True , null=True)
    posted_date = models.DateTimeField(blank=True , null=True)
    updated_date = models.DateTimeField(blank=True , null=True)
from django.db import models

# Create your models here.


class FestPass(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    yearofstudy = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=50)
    campus = models.CharField(max_length=100)
    staff_or_student = models.CharField(max_length=100)
    gitamite_or_nongitamite = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    status_updated_at = models.DateTimeField(auto_now=True)

    
# class Registrations(models.Model):
#     name = models.CharField(max_length=100, blank=True , null=True)
#     email = models.CharField(max_length=100, blank=True , null=True)
#     yearofstudy = models.CharField(max_length=100 , blank=True , null=True)
#     phone_number = models.CharField(max_length=20, blank=True , null=True)
#     registration_number = models.CharField(max_length=50, blank=True , null=True)
#     campus = models.CharField(max_length=100, blank=True , null=True)
#     staff_or_student = models.CharField(max_length=100, blank=True , null=True)
#     gitamite_or_nongitamite = models.CharField(max_length=100, blank=True , null=True)
#     transaction_id = models.CharField(max_length=100, blank=True , null=True)
#     amount = models.CharField(max_length=100, blank=True , null=True)
#     payment_status = models.CharField(max_length=100, blank=True , null=True)
#     payment_date = models.DateTimeField(auto_now_add=True, blank=True , null=True)
#     payment_method = models.CharField(max_length=100, blank=True , null=True)
#     status_updated_at = models.CharField(max_length=100, blank=True , null=True)
#     participation_type = models.CharField(max_length=100, blank=True, null=True)
#     orderid = models.CharField(max_length=200 , blank=True , null=True)
#     bank_ref_number = models.CharField(max_length=200 , blank=True , null=True)
from django.db import models

# Create your models here.
"""

payments dump

main details table
 
fest scan , fest entries

food scan 


"""


from django.db import models

class payments_samyukta(models.Model):
    cnf_id = models.CharField(max_length=50)
    txn_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    participation_type = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name}"


class registrations_samyukta(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    participation_type = models.CharField(max_length=50)
    email_sent = models.BooleanField(default=False)
    sent_count = models.IntegerField(default=0)
    passhash = models.CharField(max_length=100)
    email_sent_error = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.name}"
        
class Fest_entries_samyukta(models.Model):
    STATUS_CHOICES = [
        ('IN', 'In'),
        ('OUT', 'Out'),
    ]
    fullname = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    verifiedby = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200 , null=True , choices=STATUS_CHOICES)
    
    def formatted_time_12hr(self):
        return self.time.strftime('%I:%M %p')
    
    def formatted_date(self):
        return self.date.strftime('%d-%m-%Y')
    
class Fest_status_samyukta(models.Model):
    fullname = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(max_length=200 , unique=True)
    status = models.CharField(max_length=200)
    food = models.BooleanField(default=False)  

class coke_list_samyukta(models.Model):
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=200)
    
    def __str__(self):
        return self.email
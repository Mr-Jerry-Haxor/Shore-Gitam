from django.db import models

# Create your models for log entry and exit for the students

"""

tables:

security staff : email ; (boolean :  main gate , fest , open audi )

main gate entries / status

fest entries / status

open audi entries / status


"""

class security_staff(models.Model):
    email_id = models.EmailField()
    is_main_gate = models.BooleanField(default=False)
    is_fest = models.BooleanField(default=False)
    is_open_audi = models.BooleanField(default=False)
    
    
class Maingate_entries(models.Model):
    fullname = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    verifiedby = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200 , null=True)
    
    def formatted_time_12hr(self):
        return self.time.strftime('%I:%M %p')
    
    def formatted_date(self):
        return self.date.strftime('%d-%m-%Y')
    
    
class Maingate_status(models.Model):
    fullname = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(max_length=200)
    status = models.CharField(max_length=200)
    
    
class Fest_entries(models.Model):
    fullname = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    verifiedby = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200 , null=True)
    
    def formatted_time_12hr(self):
        return self.time.strftime('%I:%M %p')
    
    def formatted_date(self):
        return self.date.strftime('%d-%m-%Y')
    
class Fest_status(models.Model):
    fullname = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(max_length=200 , unique=True)
    status = models.CharField(max_length=200)
    
    
class Fest_entries_day2(models.Model):
    fullname = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    verifiedby = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200 , null=True)
    
    def formatted_time_12hr(self):
        return self.time.strftime('%I:%M %p')
    
    def formatted_date(self):
        return self.date.strftime('%d-%m-%Y')
    
class Fest_status_day2(models.Model):
    fullname = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(max_length=200 , unique=True)
    status = models.CharField(max_length=200)
    
    
class Openaudi_entries(models.Model):
    fullname = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    verifiedby = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200 , null=True)
    
    def formatted_time_12hr(self):
        return self.time.strftime('%I:%M %p')
    
    def formatted_date(self):
        return self.date.strftime('%d-%m-%Y')
    
class Openaudi_status(models.Model):
    fullname = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(max_length=200)
    status = models.CharField(max_length=200)

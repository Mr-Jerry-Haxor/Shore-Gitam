from django.db import models

class BGMIPlayer(models.Model):
    name = models.CharField(max_length=100)
    userid = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    regno = models.CharField(max_length=100)
    yearofstudy = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


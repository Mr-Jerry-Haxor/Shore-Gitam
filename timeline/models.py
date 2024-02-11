from django.db import models

class Timeline(models.Model):
    event_choices = (
        ('Culturals', 'Culturals'),
        ('Sports', 'Sports'),
        ('Minor', 'Minor'),
    )

    day = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=3000, null=True, blank=True)
    event_location = models.URLField(max_length=1000, null=True, blank=True)
    event_type = models.CharField(choices=event_choices, max_length=100)
    venue = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Day {self.day} {self.name} {self.event_type}"
    
    def formatted_event_date(self):
        return self.date.strftime('%Y-%m-%d') if self.date else None
    
    def formatted_start_time(self):
        return self.start_time.strftime('%H:%M') if self.start_time else ''

    def formatted_end_time(self):
        return self.end_time.strftime('%H:%M') if self.end_time else ''
    
    def formatted_start_time_12hr(self):
        return self.start_time.strftime('%I:%M %p') if self.start_time else ''

    def formatted_end_time_12hr(self):
        return self.end_time.strftime('%I:%M %p') if self.end_time else ''
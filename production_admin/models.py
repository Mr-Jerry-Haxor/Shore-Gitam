from django.db import models


class PassStatus(models.Model):
    pre_booking = models.BooleanField(default=False)
    release_passes = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Pre Booking: {self.pre_booking}"

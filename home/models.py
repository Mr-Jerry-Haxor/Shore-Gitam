from django.db import models
from coreteam.models import CustomUser
from payments.models import FestPass


class FreePass(models.Model):
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Custom logic before saving, if needed
        FestPass.objects.create(
            email=self.email,
            txn_id="FREE_PASS",
            transaction_status="Y",
            posted_date=self.created_at,
            updated_date=self.created_at
        )

        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return self.email


class PaymentIssueEmail(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment = models.ForeignKey(FestPass, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default="NA")
    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.email

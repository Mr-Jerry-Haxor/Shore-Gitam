from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FestPass, Registrations
from home.views import send_email_async, send_festpass_email, send_payment_failed_email


@receiver(post_save, sender=FestPass)
def after_save_trigger(sender, instance, created, **kwargs):
    if created:
        if instance.transaction_status == "Y":
            # send email mentioning successful pass purchase
            send_email_async(instance.email, send_festpass_email)
        elif instance.transaction_status == "N":
            # send email mentioning failed pass purchase
            send_email_async(instance.email, send_payment_failed_email)
    else:
        if instance.transaction_status == "Y":
            # send email mentioning successful pass purchase
            send_email_async(instance.email, send_festpass_email)
        elif instance.transaction_status == "N":
            # send email mentioning failed pass purchase
            send_email_async(instance.email, send_payment_failed_email)


@receiver(post_save, sender=Registrations)
def after_save_trigger1(sender, instance, created, **kwargs):
    if created:
        if instance.transaction_status == "Y":
            # send email mentioning successful pass purchase
            send_email_async(instance.email, send_festpass_email)
        elif instance.transaction_status == "N":
            # send email mentioning failed pass purchase
            send_payment_failed_email(instance.email, send_festpass_email)
    else:
        if instance.transaction_status == "Y":
            # send email mentioning successful pass purchase
            send_email_async(instance.email, send_festpass_email)
        elif instance.transaction_status == "N":
            # send email mentioning failed pass purchase
            send_payment_failed_email(instance.email, send_festpass_email)
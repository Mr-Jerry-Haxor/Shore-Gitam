from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import payments, registrations
import hashlib
from django.shortcuts import redirect
from django.contrib import messages

def import_payments_to_registrations(request):
    # Get all payments
    all_payments = payments.objects.all()

    # For each payment, create a new registration if it doesn't exist
    for payment in all_payments:
        if not registrations.objects.filter(email=payment.email).exists():
            # Concatenate email, name, and mobile
            to_hash = str(payment.email) + str(payment.name) + str(payment.mobile) + payment.mobile

            # Generate MD5 hash
            passhash = hashlib.md5(to_hash.encode()).hexdigest()

            registration = registrations(
                email=payment.email,
                name=payment.name,
                mobile=payment.mobile,
                participation_type=payment.participation_type,
                passhash=passhash
            )
            registration.save()

    return HttpResponse("Data imported successfully")



from django.core.mail import send_mail, EmailMultiAlternatives
from .models import registrations
from django.template.loader import get_template
from django.conf import settings

import threading
from django.http import JsonResponse
from django.views import View
from .models import registrations
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template

class SendEmailsView(View):
    def get(self, request, *args, **kwargs):
        thread = threading.Thread(target=self.send_emails, args=())
        thread.daemon = True
        thread.start()
        return JsonResponse({"message": "Emails are being sent in the background"})

    @staticmethod
    def send_emails():
        unsent_registrations = registrations.objects.filter(email_sent=False)
        count = 0
        for registration in unsent_registrations:
            subject = 'Your E-ticket For Samyukta 2024'
            html_content = get_template("email_ticket.html").render(
                {
                    'registration': registration,
                }
            )
            try:
                send_mail(
                    subject=subject,
                    message="",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[str(registration.email)],
                    html_message=html_content,
                )

                registration.email_sent = True
                registration.sent_count += 1
                registration.save()
                print(f"{count} : Email to {registration.email} sent successfully")
                count += 1
            except Exception as e:
                registrations.email_sent_error = f"An error occurred: {e}"
                registration.save()

# now write a function to send email to particular email which is sent as a parameter

def send_email_to_particular_email(request, email):
    # Get the registration with the given email
    registration = registrations.objects.get(email=email)

    # Create email subject and message
    subject = 'Your E-ticket For Samyukta 2024'
    html_content = get_template("email_ticket.html").render(
        {
            'registration': registration,
        }
    )
    try:
        send_mail(
            subject=subject,
            message="",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[str(registration.email)],
            html_message=html_content,
        )

        # Update email_sent and sent_count
        registration.email_sent = True
        registration.sent_count += 1
        registration.save()
        print(f"Email to {registration.email} sent successfully")
    except Exception as e:
        registration.email_sent_error = f"An error occurred: {e}"
        registration.save()

    messages.success(f"Email sent successfully to {email}")
    redirect("samyukta:registrations_list")



from django.shortcuts import redirect
from django.views.generic import ListView
from django.db.models import Q
from .models import registrations

class RegistrationListView(ListView):
    model = registrations
    template_name = 'samyukta_registrations.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return registrations.objects.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(mobile__icontains=query)
            )
        else:
            return registrations.objects.all()


from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from django.views import View
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import payments_samyukta, registrations_samyukta, Fest_entries_samyukta, Fest_status_samyukta, coke_list_samyukta
import hashlib
import threading


def samyuktahome(request):
    return render(request,'samyukta_home.html')


def import_payments_to_registrations(request):
    # Get all payments
    all_payments = payments_samyukta.objects.all()

    # For each payment, create a new registration if it doesn't exist
    for payment in all_payments:
        if not registrations_samyukta.objects.filter(email=payment.email).exists():
            # Concatenate email, name, and mobile
            to_hash = str(payment.email) + str(payment.name) + str(payment.mobile) + payment.mobile

            # Generate MD5 hash
            passhash = hashlib.md5(to_hash.encode()).hexdigest()

            registration = registrations_samyukta(
                email=payment.email,
                name=payment.name,
                mobile=payment.mobile,
                participation_type=payment.participation_type,
                passhash=passhash
            )
            registration.save()

    return HttpResponse("Data imported successfully")




class SendEmailsView(View):
    def get(self, request, *args, **kwargs):
        thread = threading.Thread(target=self.send_emails, args=())
        thread.daemon = True
        thread.start()
        return JsonResponse({"message": "Emails are being sent in the background to the audience who didn't received yet."})

    @staticmethod
    def send_emails():
        unsent_registrations = registrations_samyukta.objects.filter(email_sent=False)
        count = 0
        for registration in unsent_registrations:
            subject = 'Your E-ticket For Samyukta 2024'
            html_content = get_template("samyukta_email_ticket.html").render(
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
                registration.email_sent_error = f"An error occurred: {e}"
                registration.save()


class ReSendEmailsView(View):
    def get(self, request, *args, **kwargs):
        thread = threading.Thread(target=self.send_emails, args=())
        thread.daemon = True
        thread.start()
        return JsonResponse({"message": "Emails are being sent again to all in the background to the audience who didn't received yet."})

    @staticmethod
    def send_emails():
        # First, set email_sent to False for all users
        registrations_samyukta.objects.update(email_sent=False)

        unsent_registrations = registrations_samyukta.objects.filter(email_sent=False)
        count = 0
        for registration in unsent_registrations:
            subject = 'Your E-ticket For Samyukta 2024'
            html_content = get_template("samyukta_email_ticket.html").render(
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

                # After sending the email, set email_sent to True and increment sent_count by 1
                registration.email_sent = True
                registration.sent_count += 1
                registration.save()
                print(f"{count} : Email to {registration.email} sent successfully")
                count += 1
            except Exception as e:
                registration.email_sent_error = f"An error occurred: {e}"
                registration.save()


# now write a function to send email to particular email which is sent as a parameter


def send_email_to_particular_email(request, email):
    # Get the registration with the given email
    registration = registrations_samyukta.objects.get(email=email)

    # Create email subject and message
    subject = 'Your E-ticket For Samyukta 2024'
    html_content = get_template("samyukta_email_ticket.html").render(
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
        messages.success(request, f"Email sent successfully to {registration.email}")
        redirect("samyukta:registrations_list")
    except Exception as e:
        registration.email_sent_error = f"An error occurred: {e}"
        registration.save()
        messages.error(request, f"An error occurred: {e}")
        redirect("samyukta:registrations_list")





class RegistrationListView(ListView):
    model = registrations_samyukta
    template_name = 'samyukta_registrations.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return registrations_samyukta.objects.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(mobile__icontains=query)
            )
        else:
            return registrations_samyukta.objects.all()
        

@login_required(login_url="/auth/login/google-oauth2/")
def festpass_scan_samyukta(request):
    if request.method == 'POST':
        qrhash = request.POST.get('qrhash')
        if registrations_samyukta.objects.filter(passhash=qrhash).exists():
            student = registrations_samyukta.objects.get(passhash=qrhash)
            email = student.email
            entries = Fest_entries_samyukta.objects.filter(email=email)
            entrycount = len(entries)
            if entrycount % 2 == 0:
                status = "IN"
            else:
                status = "OUT"
            insidecount = Fest_status_samyukta.objects.filter(status="IN").count()
            outsidecount = Fest_status_samyukta.objects.filter(status="OUT").count()
            return render(request, 'samyukta_qrverify.html', {'student': student, 'entries': entries ,  'cam' : "cam0"  , "status" : status , "insidecount" : insidecount , "outsidecount" : outsidecount})
        else:
            messages.error(request, 'This student has not registered for the festpass.')
            return redirect('samyukta:festpass_scan')
    else:
        return render(request, 'samyukta_scan.html')


@login_required(login_url="/auth/login/google-oauth2/")
def festpass_verify_samyukta(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        cam = request.POST.get('cam')
        fest_status = Fest_status_samyukta.objects.get(email=email)
        if fest_status.exists():
            status = fest_status.status
            if status == 'IN':
                Fest_status_samyukta.objects.filter(email=email).update(status='OUT')
                adding = Fest_entries_samyukta(email=email, fullname=Fest_status_samyukta.objects.get(email=email).fullname, verifiedby=request.user.email , status="OUT")
                adding.save()
                messages.success(request, "You have successfully exited.")
            elif status == 'OUT': 
                Fest_status_samyukta.objects.filter(email=email).update(status='IN')
                adding = Fest_entries_samyukta(email=email, fullname=Fest_status_samyukta.objects.get(email=email).fullname, verifiedby=request.user.email , status="IN") 
                adding.save()
                messages.success(request, "You have successfully entered.")
        else:
            student = registrations_samyukta.objects.get(email=email)
            studentname = student.name
            Feststatus = Fest_status_samyukta(email=email, fullname=studentname, status="IN")
            Feststatus.save()
            adding = Fest_entries_samyukta(email=email, fullname=studentname, verifiedby=request.user.email , status="IN")
            adding.save()
            messages.success(request, "You have successfully entered.")
        if cam == "cam0":
            return redirect('samyukta:festpass_scan')
        else:
            return redirect('samyukta:festpass_scan')

@login_required(login_url="/auth/login/google-oauth2/")     
def coke_scan_samyukta(request):
    if request.method == 'POST':
        qrhash = request.POST.get('qrhash')
        if registrations_samyukta.objects.filter(passhash=qrhash).exists():
            student = registrations_samyukta.objects.get(passhash=qrhash)
            email = student.email
            if Fest_status_samyukta.objects.filter(email=email).exists():
                if coke_list_samyukta.objects.filter(email=email).exists():
                    messages.error(request, 'This student has already Taken coke.')
                    return redirect('samyukta:cokescan')
                else:
                    c = coke_list_samyukta(email=email, status="Taken")
                    c.save()
                    messages.success(request, 'This student has successfully Grabbed Beverage.')
                    return render(request, 'samyukta_cokescan_verify.html')
            else:
                messages.error(request, 'This student has not scanned for festpass.')
                return redirect('samyukta:cokescan')
        else:
            messages.error(request, 'This student has not registered for the festpass.')
            return redirect('samyukta:cokescan')
    else:
        cokecount = coke_list_samyukta.objects.filter(status="Taken").count()
        return render(request, 'samyukta_cokescan.html' , {'cokecount': cokecount})

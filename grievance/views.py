from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives

from .models import Ticket, issue_types, issue_status
from coreteam.models import *
from home.views import send_email_async
from payments.models import FestPass

"""
User:
Form
Grievance Dashboard

Grievance User:
Grievance Dashboard
Change status of a ticket
Add comment for a ticket
"""

def status_remarks_updated(user_email):
    user = CustomUser.objects.get(email=user_email)
    ticket = Ticket.objects.get(user=user)

    subject = "Shore'25 - Update on raised ticket"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("grievance/update_email.html").render({
        "name": ticket.user.first_name,
        "title": ticket.title,
        "description": ticket.description,
        "status": ticket.status,
        "remarks": ticket.remark
    })

    msg = EmailMultiAlternatives(subject, html_content, from_email, [user_email])
    msg.content_subtype = "html"
    msg.send()


def send_ticket_created_email(user_email):
    user = CustomUser.objects.get(email=user_email)
    ticket = Ticket.objects.get(user=user)

    subject = "Shore'25 - Successfully Raised Ticket"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("grievance/submitted_email.html").render({
        "name": ticket.user.first_name,
        "title": ticket.title,
        "description": ticket.description,
        "date": ticket.submitted_at,
    })

    msg = EmailMultiAlternatives(subject, html_content, from_email, [user_email])
    msg.content_subtype = "html"
    msg.send()


def send_ticket_rejected(user_email):
    user = CustomUser.objects.get(email=user_email)
    ticket = Ticket.objects.get(user=user)

    subject = "Shore'25 - Your ticket has been rejected"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("grievance/rejected_email.html").render({
        "name": ticket.user.first_name,
        "title": ticket.title,
        "description": ticket.description,
        "remarks": ticket.remark,
    })

    msg = EmailMultiAlternatives(subject, html_content, from_email, [user_email])
    msg.content_subtype = "html"
    msg.send()


def send_ticket_resolved(user_email):
    user = CustomUser.objects.get(email=user_email)
    ticket = Ticket.objects.get(user=user)

    subject = "Shore'25 - Your ticket has been resolved"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("grievance/resolved_email.html").render({
        "name": ticket.user.first_name,
        "title": ticket.title,
        "description": ticket.description,
        "remarks": ticket.remark,
    })

    msg = EmailMultiAlternatives(subject, html_content, from_email, [user_email])
    msg.content_subtype = "html"
    msg.send()


def dashboard(request):
    if request.user.is_authenticated:
        context = {}

        context['types'] = issue_types
        context['status'] = issue_status

        context['total_tickets'] = Ticket.objects.all().count()
        context['submitted_tickets'] = Ticket.objects.filter(status='submitted').count()
        context['resolved_tickets'] = Ticket.objects.filter(status='resolved').count()
        context['rejected_tickets'] = Ticket.objects.filter(status='rejected').count()
        context['under_review_tickets'] = Ticket.objects.filter(status='under_review').count()


        if request.user.grievance_staff:
            tickets = Ticket.objects.all().order_by('-submitted_at')
        else:
            tickets = Ticket.objects.filter(user=request.user)
        
        context['tickets'] = tickets

        return render(request, "grievance/dashboard.html", context)
    
    return redirect("home:login")


def raise_ticket(request):
    if request.user.is_authenticated:
        if request.user.grievance_staff:
            return redirect("grievance:dashboard")

        context = {}
        context['issue_types'] = issue_types

        if request.POST:
            type = request.POST.get('issue-type')
            title = request.POST.get('title')
            description = request.POST.get('description')
            utr = request.POST.get('upi-reference')
            file = request.FILES.get('attachment')

            if file:
                valid_extensions = ['png', 'jpg', 'jpeg', 'pdf']
                max_size = 2 * 1024 * 1024  # 2 MB

                if file.size > max_size:
                    messages.error(request, 'File size should not exceed 2MB.')
                    return render(request, "grievance/raise_ticket.html", context)

                if not file.name.split('.')[-1].lower() in valid_extensions:
                    messages.error(request, 'File type is not supported. Only png, jpg, jpeg, and pdf are allowed.')
                    return render(request, "grievance/raise_ticket.html", context)

            ticket = Ticket.objects.create(
                user = request.user,
                title = title,
                description = description,
                type = type,
                utr = utr,
                attached_documents = file,
            )
            ticket.save()
            
            messages.success(request, 'Ticket raised successfully')

            # send email to user
            send_email_async(request.user.email, send_ticket_created_email)

            return redirect("grievance:dashboard")

        return render(request, "grievance/raise_ticket.html", context)
    
    return redirect("home:login")


def update_ticket(request, ticket_hash):
    if request.user.is_authenticated and request.user.grievance_staff:
        context = {}

        flag = False
        ticket = get_object_or_404(Ticket, ticket_hash=ticket_hash)
        context['ticket'] = ticket
        context['status'] = issue_status

        if request.POST:
            if "status" in request.POST:
                if request.POST['status'] != ticket.status:
                    flag = True
                    
                    ticket.status = request.POST["status"]
                    ticket.save()

                    messages.success(request, f"Updated {ticket.user.email}'s status to {ticket.status}")

                    """
                    if ticket.status == 'resolved':
                        flag = False
                        # modify transaction to Y
                        festpass_obj = FestPass.objects.filter(email=ticket.user.email)
                        if festpass_obj.exists():
                            festpass_obj = festpass_obj[0]
                            festpass_obj.transaction_status = "Y"
                            festpass_obj.save()

                        else:
                            obj = FestPass.objects.create(
                                name = ticket.user.first_name,
                                mobile = ticket.user.phone_number,
                                email = ticket.user.email,
                                gender = ticket.user.gender,
                                roll_number = ticket.user.registration_number,
                                participation_category = 'GITAM Students' if ticket.user.is_gitamite else 'Non GITAM Student',
                                participation_type = 'student',
                                amount = 399 if ticket.user.is_gitamite else 589,
                                txn_id = ticket.utr,
                                transaction_status = 'Y'
                            )
                            obj.save()

                        messages.info(request, f"Updated {ticket.user.email}'s status to {ticket.status} and modified transaction status to 'Y' in payments table.")

                        send_email_async(ticket.user.email, send_ticket_resolved)

                    elif ticket.status == 'rejected':
                        flag = False
                        festpass_obj = FestPass.objects.filter(email=ticket.user.email)
                        if festpass_obj.exists():
                            festpass_obj = festpass_obj[0]
                            festpass_obj.transaction_status = "N"
                            festpass_obj.save()
                        else:
                            obj = FestPass.objects.create(
                                name = ticket.user.first_name,
                                mobile = ticket.user.phone_number,
                                email = ticket.user.email,
                                gender = ticket.user.gender,
                                roll_number = ticket.user.registration_number,
                                participation_category = 'GITAM Students' if ticket.user.is_gitamite else 'Non GITAM Student',
                                participation_type = 'student',
                                amount = 399 if ticket.user.is_gitamite else 589,
                                txn_id = ticket.utr,
                                transaction_status = 'N'
                            )
                            obj.save()

                            messages.info(request, f"Updated {ticket.user.email}'s status to {ticket.status} and modified transaction status to 'N' in payments table.")

                            send_email_async(ticket.user.email, send_ticket_rejected)
                    """

            if "remarks" in request.POST:
                if request.POST["remarks"] != ticket.remark:
                    flag = True

                    ticket.remark = request.POST["remarks"]
                    ticket.save()
                    
                    messages.success(request, f"Added remark {ticket.remark}")

            if flag:
                # send email to user, update their latest status and remarks
                send_email_async(ticket.user.email, status_remarks_updated)

            return redirect("grievance:dashboard")
        
        return render(request, "grievance/raise_ticket.html", context)
    
    return redirect("home:login")
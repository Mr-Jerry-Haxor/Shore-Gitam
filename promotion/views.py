from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import BGMIPlayer, Volunteer
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.contrib import messages
import re
from django.contrib.auth.decorators import login_required
from events.models import College, Event, Hackathon
from hospitality.models import HospitalityUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from coreteam.models import CustomUser

from home.views import send_email_async
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_promotion_email(user_emails):
    subject = "Shore'25 || Purchase your Shore'25 fest pass"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("promotion_mail.html")

    msg = EmailMultiAlternatives(subject, html_content, from_email, user_emails)
    msg.content_subtype = "html"
    msg.send()


def send_success_volunteer_registration(user_email):
    user = Volunteer.objects.get(email=user_email)

    subject = "Shore'25 || Successfully volunteer registration"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("volunteer_success_email.html").render({"user": user})

    msg = EmailMultiAlternatives(subject, html_content, from_email, [user_email])
    msg.content_subtype = "html"
    msg.send()


def volunteer_accepted_email(user_email):
    user = Volunteer.objects.get(email=user_email)

    subject = "Shore'25 || Volunteer request accepted"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("volunteer_accept_email.html").render({"user": user})

    msg = EmailMultiAlternatives(subject, html_content, from_email, [user_email])
    msg.content_subtype = "html"
    msg.send()


@require_http_methods(["GET", "POST"])
def bgmi_player(request):
    if True:
        return render(
            request, "bgmiclose.html", {"titletext": "BGMI Registration Closed"}
        )
    if request.method == "GET":
        # Render the form template for GET requests
        return render(
            request, "bgmireg.html"
        )  # Replace 'player_registration.html' with your template file

    elif request.method == "POST":
        # Extract data from the submitted form
        try:
            name = request.POST.get("Name")
            userid = request.POST.get("userid")
            email = request.POST.get("email")
            regno = request.POST.get("regno")
            yearofstudy = request.POST.get("yearofstudy")
            campus = request.POST.get("campus")
            # Create a new BGMIPlayer object and save it to the database
            new_player = BGMIPlayer(
                name=name,
                userid=userid,
                email=email,
                regno=regno,
                yearofstudy=yearofstudy,
                campus=campus,
            )
            new_player.save()
            messages.success(request, "Registration successful")
        except IntegrityError as e:
            # Catch the specific IntegrityError for unique constraint failure
            messages.error(
                request, "Email already exists. Please use a different email"
            )
            return render(request, "bgmireg.html")

        # Return a success message as JSON response
        # return JsonResponse({'message': 'Player created successfully'}, status=201)
        return redirect("bgmireg")


@login_required(login_url="/auth/login/google-oauth2/")
def volunteer_registration(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone_number = request.POST.get("phone_number")
            regno = request.POST.get("regNo")
            gender = request.POST.get("gender")
            year_of_study = request.POST.get("year_of_study")
            branch = request.POST.get("branch")
            course = request.POST.get("course")
            is_hosteler = request.POST.get("hosteler") == "yes"
            previous_experience = request.POST.get("prev")
            tshirt_size = request.POST.get("tShirtSize")
            why_you_interested = request.POST.get("whyJoin")
            profile_pic = request.FILES.get("photo")

            if email != request.user.email:
                messages.error(request, "You can only register using your email.")
                return redirect("volunteer")

            # Validate image file type and size
            if isinstance(profile_pic, InMemoryUploadedFile):
                valid_types = ["image/jpeg", "image/jpg", "image/png"]
                max_size = 2 * 1024 * 1024  # 2MB

                if profile_pic.size > max_size:
                    messages.error(request, "File size must be less than 2MB.")
                    return redirect("volunteer")

                if profile_pic.content_type not in valid_types:
                    messages.error(
                        request, "Please upload an image file (JPG, JPEG, PNG)."
                    )
                    return redirect("volunteer")

            # Save data to the Volunteer model
            volunteer = Volunteer(
                name=name,
                email=email,
                phone_number=phone_number,
                regno=regno,
                gender=gender,
                year_of_study=year_of_study,
                branch=branch,
                course=course,
                ishosteler=is_hosteler,
                previous_experience=previous_experience,
                why_you_interested=why_you_interested,
                tshirt_size=tshirt_size,
                profile_pic=profile_pic,
            )
            volunteer.save()  # Save the data to the database
            messages.success(request, "Successfully completed volunteer registration.")

            send_email_async(email, send_success_volunteer_registration)

            return render(request, "volunteer_success.html")
        except IntegrityError as e:
            print(e)
            messages.error(
                request, "Email already exists. Please use a different email"
            )
            return redirect("volunteer")
        except Exception as e:
            print(e)
            messages.error(request, e)
            return redirect("volunteer")
    else:
        return render(request, "volunteer_registration.html")


def send_volunteer_emails(request):
    if request.user.is_superuser:
        volunteers = Volunteer.objects.all()
        for volunteer in volunteers:
            send_email_async(volunteer.email, send_success_volunteer_registration)
        return HttpResponse("Done, sent emails!!")
    return redirect("home:homepage")


@login_required(login_url="/auth/login/google-oauth2/")
def volunteer_dashboard(request):
    if request.user.president or request.user.hospitality_staff or request.user.is_superuser:
        context = {}
        context["volunteers"] = Volunteer.objects.all().order_by('-created_at')
        context["total_volunteers"] = Volunteer.objects.all().count()
        context["approved_volunteers"] = Volunteer.objects.filter(isvolunteer=True).count()
        context["remaining_volunteers"] = Volunteer.objects.filter(isvolunteer=False).count()
        return render(request, "volunteer_dashboard.html", context)
    else:
        return redirect("home:homepage")


@login_required(login_url="/auth/login/google-oauth2/")
def volunteer_accept(request, email):
    if request.user.president or request.user.hospitality_staff or request.user.is_superuser:
        volunteer = Volunteer.objects.get(email=email)
        volunteer.isvolunteer = True
        volunteer.save()

        send_email_async(email, volunteer_accepted_email)

        messages.success(request, f"Accepted {email}")
        return redirect("volunteer_dashboard")
    else:
        return redirect("home:homepage")


def noc(request):
    return redirect("hospitality:hospitalitynoc")


@login_required(login_url="/auth/login/google-oauth2/")
def send_emails_to_unpurchased(request):
    if request.user.is_superuser:
        users = CustomUser.objects.filter(is_festpass_purchased=False)
        emails = [user.email for user in users]

        try:
            send_email_async(emails, send_promotion_email)
            
            messages.success(request, "completed sending emails")
        except Exception as e:
            messages.error(request, e)
            return redirect("home:dashboard")
        
        return render(request, "promo.html")
    return redirect("home:homepage")



import xlwt
from django.http import HttpResponse
from events.models import Participants


def export_participants_to_excel(request):
    # Create an HttpResponse object with the appropriate Excel header.
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="participants.xls"'

    # Create a workbook and add a worksheet.
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Participants')

    # Define the header row and styles.
    header_style = xlwt.XFStyle()
    header_font = xlwt.Font()
    header_font.bold = True
    header_style.font = header_font

    # Define the column headers.
    columns = ['Name', 'Email', 'Phone Number', 'College', 'Sport', 'Team', 'Captain']

    # Write the headers to the sheet.
    for col_num, column_title in enumerate(columns):
        ws.write(0, col_num, column_title, header_style)

    # Fetch all participants.
    participants = Participants.objects.select_related('college', 'sport', 'team').all()

    # Write participant data to rows.
    for row_num, participant in enumerate(participants, start=1):
        ws.write(row_num, 0, participant.name)
        ws.write(row_num, 1, participant.email)
        ws.write(row_num, 2, participant.phone_number)
        ws.write(row_num, 3, participant.college.name)  # Assuming 'College' has a 'name' field.
        ws.write(row_num, 4, participant.sport.name)    # Assuming 'Event' has a 'name' field.
        ws.write(row_num, 5, participant.team.name)     # Assuming 'Team' has a 'name' field.
        ws.write(row_num, 6, 'Yes' if participant.isCaptain else 'No')

    # Save the workbook to the response.
    wb.save(response)
    return response

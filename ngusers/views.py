import threading
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.template.loader import get_template
from django.db import IntegrityError
from django.conf import settings
from coreteam.models import CustomUser
from festpass.models import Student
from hospitality.views import generate_otp
from .models import AllowedParticipants, ProfilePicUpdated
import requests
import json

def send_otp_email(user_email, otp):
    participant = AllowedParticipants.objects.get(email=user_email)

    subject = f"SHORE'24 GITAM, Sign Up OTP"
    html_content = get_template("ngusers/otp_template.html").render(
        {
            "user_otp": otp,
        }
    )

    try:
        send_mail(
            subject=subject,
            message="",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            html_message=html_content,
        )
    except Exception as e:
        print(f"An error occurred: {e}")


def user_login(request):
    if request.user.is_authenticated:
        return redirect("ngusers:home")
    context = {}
    if request.method == "POST":
        email = request.POST["email"]

        try:
            participant = AllowedParticipants.objects.get(email=email)
        except AllowedParticipants.DoesNotExist:
            messages.error(request, f"Account with email {email} does not exist")
            return redirect("ngusers:login")

        username = participant.username
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect("ngusers:home")
            return redirect("corehome")
        else:
            messages.error(request, "Invalid Email or Password")
            return redirect("ngusers:login")

    return render(request, "ngusers/login.html", context)


def verify_edu_email(email):
    data = {
                'mail': email,
            }
    response = requests.post('https://gevents.gitam.edu/registration/data/checkmail', data=data)
    if response.status_code == 200:
        studentdata = json.loads(response.text)
        if studentdata['status'] == 'success':
            try:
                if studentdata['data']['staff_email'] == email:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False
    else:
        return False


def verify_email(request):
    if request.user.is_authenticated:
        return redirect("ngusers:home")
    context = {}
    context["otp_sent"] = False
    if request.method == "POST":
        if "send-otp" in request.POST:
            email = request.POST["email"]
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect("ngusers:login")

            if not AllowedParticipants.objects.filter(email=email).exists():
                # check the email domain is @gitam.edu
                if not email.endswith("@gitam.edu"):
                    messages.error(request, "Only participants emails are allowed. If you have doubt,contact: Shore_tech@gitam.in")
                    return redirect("ngusers:register")
                else:
                    if verify_edu_email(email):
                        AllowedParticipants.objects.create(email=email)
                    else:
                        messages.error(request, "Mailid was not valid. If you have doubt,contact: Shore_tech@gitam.in")
                        return redirect("ngusers:register")

            participant = AllowedParticipants.objects.get(email=email)

            otp = generate_otp()

            email_thread = threading.Thread(target=send_otp_email, args=(email, otp))
            email_thread.start()

            context["otp_sent"] = True
            context["email"] = email

            participant.otp = otp
            participant.save()

        elif "verify-otp" in request.POST:
            otp = request.POST["otp"]
            email = request.POST["email"]
            if AllowedParticipants.objects.filter(email=email, otp=otp).exists():
                request.session["otp_verified"] = True
                return redirect("ngusers:set_password", email=email)
            else:
                messages.info(request, "OTP is incorrect")
                return redirect("ngusers:verify_email")

    return render(request, "ngusers/verify_email.html", context)


def set_password(request, email):
    if request.session.get("otp_verified"):
        context = {}
        participant = AllowedParticipants.objects.get(email=email)
        context["email"] = email
        if request.method == "POST":
            username = request.POST["username"]
            first_name = request.POST["first_name"].title()
            last_name = request.POST["last_name"].title()
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            if password == confirm_password:
                participant.username = username
                participant.first_name = first_name
                participant.last_name = last_name
                participant.save()

                try:
                    user = CustomUser.objects.create_user(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password,
                    )
                    user.save()
                except IntegrityError:
                    messages.error(request, "User with this username already exists")
                    return redirect("ngusers:set_password", email=email)
                messages.success(request, "Account created successfully")
                return redirect("ngusers:login")
            else:
                messages.error(request, "Passwords do not match")
                return redirect("ngusers:set_password", email=email)
        return render(request, "ngusers/set_password.html", context)
    return redirect("ngusers:register")


def update_picture(request):
    if not request.user.is_authenticated:
        return redirect("ngusers:login")

    context = {}
    email = request.user.email

    if ProfilePicUpdated.objects.filter(email=email, updated=True).exists():
        messages.info(
            request,
            "Profile picture already updated, can only update it once. Contact shore_tech@gitam.in for any queries"
        )
        return redirect("passhome")
    if Student.objects.filter(email=email).exists():
        student = Student.objects.get(email=email)
        context['student'] = student

        if request.method == "POST":
            if student.profile_picture:
                student.profile_picture.delete()
            student.profile_picture = request.FILES.get("profile_pic")
            student.save()

            ProfilePicUpdated.objects.create(email=email, updated=True)
            messages.success(request, "Profile picture updated successfully")
            return redirect("passhome")
        return render(request, "ngusers/update_picture.html", context)
    else:
        messages.error(request, "You Haven't register for the Fest pass")
        return redirect("passhome")


@login_required(login_url="ngusers:login")
def home(request):
    return redirect("corehome")

import threading
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.template.loader import get_template
from django.db import IntegrityError

from coreteam.models import CustomUser
from festpass.models import Student
from hospitality.views import generate_otp
from .models import AllowedParticipants, ProfilePicUpdated


def send_otp_email(user_email, otp):
    participant = AllowedParticipants.objects.get(email=user_email)

    subject = f"SHORE'24 GITAM, Sign Up OTP"
    html_content = get_template("ngusers/otp_template.html").render(
        {
            "user_otp": otp,
            "name": f"{participant.first_name} {participant.last_name}",
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
            return redirect("ngusers:register")

        username = participant.username
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect("ngusers:home")
            return redirect("corehome")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("ngusers:login")

    return render(request, "ngusers/login.html", context)


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
                    messages.error(request, "Email not allowed")
                    return redirect("ngusers:register")
                else:
                    AllowedParticipants.objects.create(email=email)

            participant = AllowedParticipants.objects.get(email=email)

            otp = generate_otp()
            print(f"\nOTP is: {otp}\n")

            # send otp in email using threading
            # email_thread = threading.Thread(target=send_otp_email, args=(email, otp))
            # email_thread.start()

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
                messages.success(request, "User created successfully")
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
        return redirect("corehome")

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


@login_required(login_url="ngusers:login")
def home(request):
    return redirect("corehome")

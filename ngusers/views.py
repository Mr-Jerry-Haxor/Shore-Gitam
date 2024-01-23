import threading
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from coreteam.models import CustomUser
from hospitality.views import send_otp_email, generate_otp
from .models import AllowedParticipants


def user_login(request):
    if request.user.is_authenticated:
        return redirect("ngusers:home")
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("ngusers:home")
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
                return redirect("ngusers:register")

            if not AllowedParticipants.objects.filter(email=email).exists():
                messages.error(request, "Email not allowed")
                return redirect("ngusers:register")

            participant = AllowedParticipants.objects.get(email=email)

            otp = generate_otp()
            print(f"\nOTP is: {otp}\n")

            # send otp in email using threading
            # email_thread = threading.Thread(
            #     target=send_otp_email, args=(email, otp)
            # )
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
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            if password == confirm_password:
                participant.username = username
                participant.first_name = first_name
                participant.last_name = last_name
                participant.save()

                user = CustomUser.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    is_staff=True,
                )
                user.save()
                messages.success(request, "User created successfully")
                return redirect("ngusers:login")
            else:
                messages.error(request, "Passwords do not match")
                return redirect("ngusers:set_password", email=email)
        return render(request, "ngusers/set_password.html", context)
    return redirect("ngusers:register")


@login_required(login_url="ngusers:login")
def home(request):
    print(f"\n{request.user}\n")
    return render(request, "ngusers/home.html")

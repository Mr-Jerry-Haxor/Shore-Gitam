from django.shortcuts import render, redirect
from coreteam.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .models import UserIn

@login_required(login_url="/auth/login/google-oauth2/")
def home(request):
    # home page
    if request.user.is_superuser or request.user.security or request.user.security_staff:
        return render(request, "securitynew/home.html")
    
    else:
        messages.error(request, "You are not authorized")
        return redirect("home:dashboard")


@login_required(login_url="/auth/login/google-oauth2/")
def scan_qr(request):
    # QR Scanner
    if request.user.is_superuser or request.user.security or request.user.security_staff:
        return render(request, "securitynew/scanner1.html")
    else:
        messages.error(request, "You are not authorized")
        return redirect("home:dashboard")


@login_required(login_url="/auth/login/google-oauth2/")
def view_user(request):
    # shows user details
    if request.user.is_superuser or request.user.security or request.user.security_staff:
        passhash = request.GET.get("passhash", None)
        context = {}
        try:
            user = CustomUser.objects.get(passhash=passhash)
            context["user"] = user

            # checking if user is already in
            userin_obj = UserIn.objects.filter(user=user)
            if userin_obj.exists():
                messages.error(request, f"User already checkin at {userin_obj.in_time}")
        except CustomUser.DoesNotExist:
            messages.error(request, "Pass does not exist")
            return redirect("securitynew:scan_qr")
        return redirect(request, "securitynew/view_user.html", context)
    else:
        messages.error(request, "You are not authorized")
        return redirect("home:dashboard")


@login_required(login_url="/auth/login/google-oauth2/")
def accept_user(request, passhash):
    # accepts user
    if request.user.is_superuser or request.user.security or request.user.security_staff:
        try:
            user = CustomUser.objects.get(passhash=passhash)
            UserIn.objects.create(
                user=user, is_user_in=True
            ).save()

            messages.info(request, f"User {user.email} checked in")

            return redirect("securitynew:scan_qr")
        except CustomUser.DoesNotExist:
            messages.error(request, "Pass does not exist")
            return redirect("securitynew:scan_qr")
    else:
        messages.error(request, "You are not authorized")
        return redirect("home:dashboard")

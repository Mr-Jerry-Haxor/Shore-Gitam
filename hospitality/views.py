import pytz
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .decorators import email_check_required
from .models import HospitalityUser, Meal, MealHistory
from .hash import generate_md5


@login_required(login_url="/auth/login/google-oauth2/")
def home(request):
    context = {}

    return render(request, "home.html", context)

@login_required(login_url="/auth/login/google-oauth2/")
@email_check_required(model=HospitalityUser)
def food(request):
    context = {}
    email = request.user.email

    desired_timezone = pytz.timezone("Asia/Kolkata")
    user = HospitalityUser.objects.get(email=email)
    context["user_details"] = user
    server_datetime = timezone.now().astimezone(desired_timezone)
    server_time = server_datetime.time()
    server_date = server_datetime.date()

    context["isMeal"] = True
    try:
        filtered_meal = Meal.objects.get(
            date=server_date, start_time__lte=server_time, end_time__gte=server_time
        )

        user_string = (
            f"{user.name}_{user.email}_{filtered_meal.meal_type}_{server_time}"
        )
        context["meal"] = filtered_meal.meal_type
        if (not user.meal_id) or (user.meal_id != filtered_meal.id):
            hashed_string = generate_md5(user_string, user.id)
            user.meal_id = filtered_meal.id
            user.qr_hash = hashed_string
            user.save()
            context["hashed_string"] = hashed_string
        else:
            """Check if the user has already scanned the QR code for the meal"""
            if MealHistory.objects.filter(user=user, meal_type=filtered_meal).exists():
                scanned_meal = MealHistory.objects.get(
                    user=user, meal_type=filtered_meal
                ).scanned_time
                context["message"] = "You have already availed this meal"
            else:
                hashed_string = generate_md5(user_string, user.id)
                user.qr_hash = hashed_string
                user.save()
                context["hashed_string"] = hashed_string
        return render(request, "food.html", context)
    except ObjectDoesNotExist:
        context["isMeal"] = False
        context["message"] = "No meal found"
        return render(request, "food.html", context)

    return render(request, "food.html", context)


@login_required(login_url="/auth/login/google-oauth2/")
def scan(request):
    if not (request.user.hospitality_staff or request.user.hospitality):
        return redirect('corehome')
    else:
        context = {}
        count = 0
        context["count"] = count

        desired_timezone = pytz.timezone("Asia/Kolkata")
        server_datetime = timezone.now().astimezone(desired_timezone)
        server_time = server_datetime.time()
        server_date = server_datetime.date()

        try:
            meal = Meal.objects.get(
                date=server_date, start_time__lte=server_time, end_time__gte=server_time
            )
            context["meal"] = meal
            context["count"] = MealHistory.objects.filter(meal_type=meal).count()
        except Meal.DoesNotExist:
            context["error"] = "No meal found"
            return render(request, "hospscan.html", context)

        if request.method == "POST":
            qr_hash = request.POST.get("qr_hash")
            user_id = qr_hash[-1]
            try:
                user = HospitalityUser.objects.get(id=user_id)
            except HospitalityUser.DoesNotExist:
                context["error"] = "User does not exist"
                return render(request, "hospscan.html", context)

            if user.qr_hash == qr_hash:
                """Check if the user has already scanned the QR code for the meal"""
                if MealHistory.objects.filter(user=user, meal_type=meal).exists():
                    context["error"] = "User already availed this meal"
                    return render(request, "hospscan.html", context)
                else:
                    meal_history = MealHistory.objects.create(user=user, meal_type=meal)
                    meal_history.save()
                    context["success"] = "Meal availed successfully"
                    context["user_detail"] = user
                    return render(request, "hospscan.html", context)

            return render(request, "hospscan.html", context)
        return render(request, "hospscan.html", context)


@login_required(login_url="/auth/login/google-oauth2/")
def admin_history(request, date):
    if not (request.user.hospitality_staff or request.user.hospitality or request.user.president):
        return redirect('corehome')
    else:
        context = {}
        date_object = datetime.strptime(date, "%Y-%m-%d").date()
        context["date"] = date_object

        meal_breakfast = MealHistory.objects.filter(
            meal_type__meal_type="Breakfast", meal_type__date=date_object
        )
        meal_lunch = MealHistory.objects.filter(
            meal_type__meal_type="Lunch", meal_type__date=date_object
        )
        meal_hitea = MealHistory.objects.filter(
            meal_type__meal_type="Hi-Tea", meal_type__date=date_object
        )
        meal_dinner = MealHistory.objects.filter(
            meal_type__meal_type="Dinner", meal_type__date=date_object
        )
        meal_all = MealHistory.objects.filter(meal_type__date=date_object)

        context["meal_breakfast"] = meal_breakfast
        context["meal_lunch"] = meal_lunch
        context["meal_hitea"] = meal_hitea
        context["meal_dinner"] = meal_dinner
        context["meal_all"] = meal_all

        return render(request, "admin_history.html", context)


@login_required(login_url="/auth/login/google-oauth2/")
@email_check_required(model=HospitalityUser)
def user_history(request):
    context = {}

    email = request.user.email
    meal_details = MealHistory.objects.filter(user__email=email).order_by(
        "-scanned_time"
    )
    context["meal_details"] = meal_details
    return render(request, "history.html", context)


@login_required(login_url="/auth/login/google-oauth2/")
def checkInOutHome(request):
    if not (request.user.hospitality_staff or request.user.hospitality or request.user.president):
        return redirect('corehome')
    else:
        context = {}

        if request.POST:
            email = request.POST.get("email")
            try:
                user = HospitalityUser.objects.get(email=email)
                if user.checkout_status:
                    context["info"] = f"User {email} has already checked out."
                    return render(request, "checkInOut.html", context)
                return redirect("hospitality:checkInOutForm", email=email)
            except HospitalityUser.DoesNotExist:
                context["error"] = f"User with email {email} does not exist."
                return render(request, "checkInOut.html", context)
        return render(request, "checkInOut.html", context)


@login_required(login_url="/auth/login/google-oauth2/")
def checkInOutForm(request, email):
    if not (request.user.hospitality_staff or request.user.hospitality or request.user.president):
        return redirect('corehome')
    else:
        context = {}
        desired_timezone = pytz.timezone("Asia/Kolkata")
        user = HospitalityUser.objects.get(email=email)
        context["user"] = user

        if request.POST:
            if "checkin" in request.POST:
                hostel = request.POST.get("hostel")
                room_no = request.POST.get("room_no")

                user.hostel = hostel
                user.room_number = room_no
                user.checkin = timezone.now().astimezone(desired_timezone)
                user.checkin_status = True
                user.save()

                return redirect("hospitality:checkInOutHome")
            elif "checkout" in request.POST:
                user.checkout = timezone.now().astimezone(desired_timezone)
                user.checkout_status = True
                user.save()

                context["info"] = f"Participant {user.name} has checked out successfully."
                return redirect("hospitality:checkInOutHome")

        return render(request, "checkInOutForm.html", context)


@login_required(login_url="/auth/login/google-oauth2/")
def checkInOutHistory(request):
    if not (request.user.hospitality_staff or request.user.hospitality or request.user.president):
        return redirect('corehome')
    else:
        context = {}
        checked_in_users = HospitalityUser.objects.filter(
            checkin_status=True, checkout_status=False
        ).order_by("-checkin")
        checked_out_users = HospitalityUser.objects.filter(
            checkin_status=True, checkout_status=True
        ).order_by("-checkout")
        all_users = HospitalityUser.objects.filter(checkin_status=True).order_by("-checkin")

        context["checked_in_users"] = checked_in_users
        context["checked_out_users"] = checked_out_users
        context["all_users"] = all_users
        return render(request, "checkInOutHistory.html", context)

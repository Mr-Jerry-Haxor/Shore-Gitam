import pytz
import threading
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from .utils import generate_otp
from .decorators import email_check_required
from .models import HospitalityUser, Meal, MealHistory
from .hash import generate_md5


def send_otp_email(user_email, otp):
    subject = f"SHORE'24 GITAM, OTP {otp}"
    html_content = get_template('otp_mail.html').render({"user_otp": otp})

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

@login_required(login_url="/auth/login/google-oauth2/")
def home(request):
    context = {}
    return render(request, "home.html", context)

@login_required(login_url="/auth/login/google-oauth2/")
@email_check_required(model=HospitalityUser)
def food(request):
    context = {}
    email = request.user.email

    user = HospitalityUser.objects.get(email=email)
    context["user_details"] = user
    server_datetime = timezone.now()
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


@login_required(login_url="/auth/login/google-oauth2/")
def scan(request):
    if not (request.user.hospitality_staff or request.user.hospitality):
        return redirect('corehome')
    else:
        context = {}
        count = 0
        context["count"] = count

        server_datetime = timezone.now()
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
        context["otp_sent"] = False

        if request.POST:
            if 'send-otp' in request.POST:
                user_email = request.POST.get("email")
                try:
                    user = HospitalityUser.objects.get(email=user_email)
                    if user.checkout_status:
                            context["info"] = f"User {user_email} has already checked out."
                            messages.info(request, f"User {user_email} has already checked out.")
                            return render(request, "checkInOut.html", context)

                    otp = generate_otp()
                    user.otp = otp
                    user.save()

                    email_thread = threading.Thread(
                        target=send_otp_email, args=(user_email, otp)
                    )
                    email_thread.start()

                    context["info"] = f"OTP sent to {user_email}"
                    messages.info(request, f"OTP sent to {user_email}")
                    context["otp_sent"] = True
                    context["user_email"] = user_email
                    return render(request, "checkInOut.html", context)
                except HospitalityUser.DoesNotExist:
                    context["error"] = f"User with email {user_email} does not exist."
                    messages.error(request, f"User with email {user_email} does not exist.")
                    return render(request, "checkInOut.html", context)
            elif 'submit-button' in request.POST:
                email = request.POST.get("email")
                otp = request.POST.get("otp")
                try:
                    user = HospitalityUser.objects.get(email=email)
                    if user.otp != int(otp):
                        context["error"] = "Invalid OTP"
                        messages.error(request, "Invalid OTP")
                        return render(request, "checkInOut.html", context)
                    if user.checkout_status:
                        context["info"] = f"User {email} has already checked out."
                        messages.info(request, f"User {email} has already checked out.")
                        return render(request, "checkInOut.html", context)
                    return redirect("hospitality:checkInOutForm", email=email)
                except HospitalityUser.DoesNotExist:
                    context["error"] = f"User with email {email} does not exist."
                    messages.error(request, f"User with email {email} does not exist.")
                    return render(request, "checkInOut.html", context)
        

        return render(request, "checkInOut.html", context)


@login_required(login_url="/auth/login/google-oauth2/")
def checkInOutForm(request, email):
    if not (request.user.hospitality_staff or request.user.hospitality or request.user.president):
        return redirect('corehome')
    else:
        context = {}
        user = HospitalityUser.objects.get(email=email)
        context["user"] = user

        if request.POST:
            if "checkin" in request.POST:
                hostel = request.POST.get("hostel")
                room_no = request.POST.get("room_no")

                user.hostel = hostel
                user.room_number = room_no
                user.checkin = timezone.now()
                user.checkin_status = True
                user.save()

                return redirect("hospitality:checkInOutHome")
            elif "checkout" in request.POST:
                user.checkout = timezone.now()
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

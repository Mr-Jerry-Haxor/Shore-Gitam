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
from .models import HospitalityUser, Meal, MealHistory, ParticipantsNOC
from .hash import generate_md5

from coreteam.models import CustomUser

from events.models import Participants, HackathonParticipants

from django.contrib.auth.decorators import login_required
from events.models import College, Event, Hackathon
from django.db import IntegrityError
from django.contrib import messages


@login_required(login_url="ngusers:login")
def add_hospitality_user(request):
    if not (request.user.hospitality_staff or request.user.hospitality or request.user.is_superuser):
        return redirect("corehome")
    else:
        if request.POST:
            user_email = request.POST.get("user_email")
            user = CustomUser.objects.create(email=user_email)
            user.hospitality_staff = True
            user.save()
            messages.success(request, "User added successfully")
        return render(request, "add_hospuser.html")


def send_otp_email(user_email, otp):
    subject = f"SHORE'24 GITAM, OTP {otp}"
    html_content = get_template("otp_mail.html").render({"user_otp": otp})

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


@login_required(login_url="ngusers:login")
def home(request):
    context = {}
    email = request.user.email
    if HospitalityUser.objects.filter(email=email).exists():
        # add a card to show the user's details
        participant = HospitalityUser.objects.get(email=email)
        context["name"] = participant.name
        context["email"] = participant.email
        context["phone_number"] = participant.phone_number
        context["hostel"] = participant.hostel
        context["room_number"] = participant.room_number
        context["checkin"] = participant.checkin
        context["checkout"] = participant.checkout

        server_datetime = timezone.now()
        server_time = server_datetime.time()
        server_date = server_datetime.date()

        try:
            meal = Meal.objects.get(
                date=server_date, start_time__lte=server_time, end_time__gte=server_time
            )
            context["meal"] = meal
        except Meal.DoesNotExist:
            context["meal"] = None

    return render(request, "home.html", context)


@login_required(login_url="ngusers:login")
@email_check_required(model=HospitalityUser)
def food(request):
    context = {}
    email = request.user.email

    user = HospitalityUser.objects.get(email=email)
    context["user_details"] = user
    server_datetime = timezone.now()
    server_time = server_datetime.time()
    server_date = server_datetime.date()

    if not user.checkin_status and not user.isfoodonly:
        messages.info(request, "You have not checked in yet")
        return redirect("hospitality:home")

    if user.checkout_status and not user.isfoodonly:
        messages.info(request, "You have already checked out")
        return redirect("hospitality:home")

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


@login_required(login_url="ngusers:login")
def scan(request):
    if not (request.user.hospitality_staff or request.user.hospitality):
        return redirect("corehome")
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
            messages.error(request, "No meal found")
            return render(request, "hospscan.html", context)

        if request.method == "POST":
            qr_hash = request.POST.get("qr_hash")
            user_id = qr_hash.split("_")[-1]
            try:
                user = HospitalityUser.objects.get(id=user_id)
            except HospitalityUser.DoesNotExist:
                messages.error(request, "User does not exist")
                return render(request, "hospscan.html", context)

            if user.qr_hash == qr_hash:
                """Check if the user has already scanned the QR code for the meal"""
                if MealHistory.objects.filter(user=user, meal_type=meal).exists():
                    messages.error(request, "User already availed this meal")
                    return render(request, "hospscan.html", context)
                else:
                    meal_history = MealHistory.objects.create(user=user, meal_type=meal)
                    meal_history.save()
                    messages.success(request, "Meal availed successfully")
                    context["user_detail"] = user
                    return render(request, "hospscan.html", context)
            else:
                messages.error(request, "Invalid QR code")
                return render(request, "hospscan.html", context)
        return render(request, "hospscan.html", context)


@login_required(login_url="ngusers:login")
def admin_history(request, date):
    if not (
        request.user.hospitality_staff
        or request.user.hospitality
        or request.user.president
    ):
        return redirect("corehome")
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


@login_required(login_url="ngusers:login")
@email_check_required(model=HospitalityUser)
def user_history(request):
    context = {}

    email = request.user.email
    meal_details = MealHistory.objects.filter(user__email=email).order_by(
        "-scanned_time"
    )
    context["meal_details"] = meal_details
    return render(request, "history.html", context)


@login_required(login_url="ngusers:login")
def checkInOutHome(request):
    if not (
        request.user.hospitality_staff
        or request.user.hospitality
        or request.user.president
    ):
        return redirect("corehome")
    else:
        context = {}
        context["otp_sent"] = False

        if request.POST:
            if "send-otp" in request.POST:
                user_email = request.POST.get("email")
                user = HospitalityUser.objects.filter(email=user_email)
                if user.exists():
                    user = user[0]
                    if user.isfoodonly:
                        messages.info(
                            request,
                            f"User {user_email} is only provided with food, not accomdation.",
                        )
                        return render(request, "checkInOut.html", context)
                    if user.checkout_status:
                        messages.info(
                            request, f"User {user_email} has already checked out."
                        )
                        return render(request, "checkInOut.html", context)

                    otp = generate_otp()
                    user.otp = otp
                    user.save()

                    email_thread = threading.Thread(
                        target=send_otp_email, args=(user_email, otp)
                    )
                    email_thread.start()

                    messages.info(request, f"OTP sent to {user_email}")
                    context["otp_sent"] = True
                    context["user_email"] = user_email
                    return render(request, "checkInOut.html", context)
                else:
                    user_email = user_email.lower()
                    if Participants.objects.filter(email=user_email).exists():
                        participant = Participants.objects.get(email=user_email)

                        if participant.team.status == "approved":
                            if participant.accomdation:
                                HospitalityUser.objects.create(
                                    name=participant.name,
                                    email=participant.email,
                                    phone_number=participant.phone_number,
                                )

                                user = HospitalityUser.objects.get(email=user_email)
                                if user.checkout_status:
                                    context["info"] = (
                                        f"User {user_email} has already checked out."
                                    )
                                    messages.info(
                                        request,
                                        f"User {user_email} has already checked out.",
                                    )
                                    return render(request, "checkInOut.html", context)

                                otp = generate_otp()
                                user.otp = otp
                                user.save()

                                email_thread = threading.Thread(
                                    target=send_otp_email, args=(user_email, otp)
                                )
                                email_thread.start()
                                messages.info(request, f"OTP sent to {user_email}")
                                context["otp_sent"] = True
                                context["user_email"] = user_email
                                return render(request, "checkInOut.html", context)
                            else:
                                messages.error(
                                    request,
                                    f"User with email {user_email} have not opted accomodation.",
                                )
                                return render(request, "checkInOut.html", context)
                        else:
                            messages.error(
                                request,
                                f"User with email {user_email} Team status is not Approved",
                            )
                            return render(request, "checkInOut.html", context)

                    if HackathonParticipants.objects.filter(email=user_email).exists():
                        participant = HackathonParticipants.objects.get(
                            email=user_email
                        )

                        if participant.team.status == "approved":
                            if participant.accomdation:
                                HospitalityUser.objects.create(
                                    name=participant.name,
                                    email=participant.email,
                                    phone_number=participant.phone_number,
                                )

                                user = HospitalityUser.objects.get(email=user_email)
                                if user.checkout_status:
                                    context["info"] = (
                                        f"User {user_email} has already checked out."
                                    )
                                    messages.info(
                                        request,
                                        f"User {user_email} has already checked out.",
                                    )
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
                            else:
                                messages.error(
                                    request,
                                    f"User with email {user_email} have not opted accomodation.",
                                )
                                return render(request, "checkInOut.html", context)
                        else:
                            messages.error(
                                request,
                                f"User with email {user_email} Team status is not Approved",
                            )
                            return render(request, "checkInOut.html", context)

                    messages.error(
                        request, f"User with email {user_email} does not exist."
                    )
                    return render(request, "checkInOut.html", context)
            elif "submit-button" in request.POST:
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


@login_required(login_url="ngusers:login")
def checkInOutForm(request, email):
    if not (
        request.user.hospitality_staff
        or request.user.hospitality
        or request.user.president
    ):
        return redirect("corehome")
    else:
        context = {}
        user = HospitalityUser.objects.get(email=email)

        if user.isfoodonly:
            messages.info(
                request, f"User {email} is only provided with food, not accomdation."
            )
            return redirect("hospitality:checkInOutHome")

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

                context["info"] = (
                    f"Participant {user.name} has checked out successfully."
                )
                return redirect("hospitality:checkInOutHome")

        return render(request, "checkInOutForm.html", context)


@login_required(login_url="ngusers:login")
def checkInOutHistory(request):
    if not (
        request.user.hospitality_staff
        or request.user.hospitality
        or request.user.president
    ):
        return redirect("corehome")
    else:
        context = {}
        checked_in_users = HospitalityUser.objects.filter(
            checkin_status=True, checkout_status=False
        ).order_by("-checkin")
        checked_out_users = HospitalityUser.objects.filter(
            checkin_status=True, checkout_status=True
        ).order_by("-checkout")
        all_users = HospitalityUser.objects.filter(checkin_status=True).order_by(
            "-checkin"
        )

        context["checked_in_users"] = checked_in_users
        context["checked_out_users"] = checked_out_users
        context["all_users"] = all_users
        return render(request, "checkInOutHistory.html", context)


# @login_required(login_url="/auth/login/google-oauth2/")
def noc_and_travel_tickets(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        regno = request.POST.get("regno")
        gender = request.POST.get("gender")
        yearofstudy = request.POST.get("yearofstudy")
        branch = request.POST.get("branch")
        institute = request.POST.get("institute")
        Department = request.POST.get("Department")
        campus = request.POST.get("campus")
        hosteler = request.POST.get("hosteler")
        eventtype = request.POST.get("eventtype")
        eventname = request.POST.get("eventname")
        teamname = request.POST.get("teamname")
        tshirt = request.POST.get("tshirt")
        noc_file_input = request.FILES.get("noc_file_input")
        accomodation = request.POST.get("accomodation")
        travelling = request.POST.get("travelling")
        profile_pic = request.FILES.get("profile_pic")

        try:
            studentnoc = ParticipantsNOC(
                full_name=name,
                email=email,
                phone_number=phone_number,
                regno=regno,
                gender=gender,
                yearofstudy=yearofstudy,
                branch=branch,
                institute=institute,
                department=Department,
                campus=campus,
                hosteler=hosteler,
                eventtype=eventtype,
                eventname=eventname,
                teamname=teamname,
                tshirt=tshirt,
                accomodation=accomodation,
                travelling=travelling,
                noc_file_input=noc_file_input,
                profile_pic=profile_pic,
            )
            studentnoc.save()

            if travelling == "1":
                departure = request.POST.get("departure")
                arrival = request.POST.get("arrival")
                departureDatetime = request.POST.get("departureDatetime")
                arrivalDatetime = request.POST.get("arrivalDatetime")
                ticket_file_input = request.FILES.get("ticket_file_input")

                studentnoc.departure = departure
                studentnoc.arrival = arrival
                studentnoc.departureDatetime = departureDatetime
                studentnoc.arrivalDatetime = arrivalDatetime
                studentnoc.ticket_file_input = ticket_file_input

                studentnoc.save()

            messages.success(request, "Registration successful")
            return redirect("noc_and_tickets")
        except IntegrityError as e:
            # Catch the specific IntegrityError for unique constraint failure
            messages.error(
                request, "Email already exists.Any issues,Contact: shore_tech@gitam.in "
            )
            return redirect("noc_and_tickets")

    else:
        context = {}
        colleges = College.objects.all()
        context["colleges"] = colleges
        events = Event.objects.all()
        hackathons = Hackathon.objects.all()
        context["events"] = events
        context["hackathons"] = hackathons
        return render(request, "noc_tickets_reg.html", context)


@login_required(login_url="ngusers:login")
def scan1(request):
    if not (request.user.hospitality_staff or request.user.hospitality):
        return redirect("corehome")
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
            messages.error(request, "No meal found")
            return render(request, "scan_qr.html", context)

        if request.method == "POST":
            qr_hash = request.POST.get("qr_hash")
            user_id = qr_hash[-1]
            try:
                user = HospitalityUser.objects.get(id=user_id)
            except HospitalityUser.DoesNotExist:
                messages.error(request, "User does not exist")
                return render(request, "scan_qr.html", context)

            if user.qr_hash == qr_hash:
                """Check if the user has already scanned the QR code for the meal"""
                if MealHistory.objects.filter(user=user, meal_type=meal).exists():
                    messages.error(request, "User already availed this meal")
                    return render(request, "scan_qr.html", context)
                else:
                    meal_history = MealHistory.objects.create(user=user, meal_type=meal)
                    meal_history.save()
                    messages.success(request, "Meal availed successfully")
                    context["user_detail"] = user
                    return render(request, "scan_qr.html", context)

            return render(request, "scan_qr.html", context)
        return render(request, "scan_qr.html", context)

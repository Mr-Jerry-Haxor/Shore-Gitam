import hashlib
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.db import transaction, IntegrityError
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count

from .models import Event, Team, Participant, campus_choices
from home.views import send_email_async


def send_success_email(email):
    team = Team.objects.get(captain_email=email)
    email_list = []
    email_list.append(email)
    for participant in team.participants.all():
        email_list.append(participant)
    subject = f"Shore'25 - Successfully Registered for {team.event.name}"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("prelims/success_email.html").render(
        {"team": team, "captain": Participant.objects.get(team=team, isCaptain=True)}
    )

    msg = EmailMultiAlternatives(subject, html_content, from_email, email_list)
    msg.content_subtype = "html"
    msg.send()


def generate_md5(user_string):
    hashed_string = hashlib.md5(user_string.encode("UTF-8"))
    return hashed_string.hexdigest()


def culturals_home(request):
    """home page for culturals"""
    context = {}
    events = Event.objects.filter(event_type="culturals")
    context["events"] = events

    return render(request, "prelims/prelims_home.html", context)


@login_required(login_url="home:login")
def registered_events(request):
    email = request.user.email
    context = {}
    participant = Participant.objects.filter(email=email)

    context["participant"] = participant

    if request.method == "POST":
        team_id = request.POST.get("team_id")
        uploadedFile = request.FILES["fileUpload"]
        team = Team.objects.get(id=team_id)
        team.reference_attatchment.save(uploadedFile.name, uploadedFile, save=True)

    return render(request, "prelims_registered_events.html", context)


@login_required(login_url="home:login")
def view_teams(request, event_name):
    if request.user.events_cultural:
        context = {}
        events = [event.name for event in Event.objects.all()]
        context["events"] = events
        event = Event.objects.get(name=event_name)
        teams = Team.objects.filter(event=event)

        context["event"] = event
        context["teams"] = teams

        return render(request, "prelims_view_teams.html", context)
    else:
        messages.error(request, "You are not authorized to view this page")
        return redirect("prelims:home")


@login_required(login_url="home:login")
def view_team(request, team_hash):
    if request.user.events_cultural:
        context = {}
        events = [event.name for event in Event.objects.all()]
        context["events"] = events
        team = Team.objects.get(team_hash=team_hash)
        participants = Participant.objects.filter(team=team)

        context["captain"] = Participant.objects.get(team=team, isCaptain=True)
        context["team"] = team
        context["participants"] = participants

        return render(request, "prelims_view_team.html", context)
    else:
        messages.error(request, "You are not authorized to view this page")
        return redirect("culturals_home")


@login_required(login_url="/auth/login/google-oauth2/")
def register(request, event_name):
    context = {}
    context["campus_choices"] = campus_choices
    email = request.user.email

    event = Event.objects.get(name=event_name)

    if Participant.objects.filter(email=email, event=event).exists():
        messages.error(request, f"You have already registered for {event.name}")
        return redirect("prelims:home")

    context["event"] = event

    teammates = ""
    if request.method == "POST":
        visible_team_name = request.POST.get("team_name")
        captain_name = request.POST.get("name_1")
        captain_email = request.POST.get("email_1")
        captain_phone = request.POST.get("phone_1")
        captain_regnum = request.POST.get("regnum_1").upper()
        captain_campus = request.POST.get("campus_1")

        if request.user.email != captain_email:
            messages.error(request, "You can only register with your email")
            return render(request, "prelims/prelims_registration.html", context)

        if Participant.objects.filter(email=captain_email, event=event).exists():
            messages.error(request, f"You have already registered for {event.name}")
            return render(request, "prelims/prelims_registration.html", context)

        try:
            validate_email(captain_email)
            if not (
                captain_email.endswith("@gitam.in")
                or captain_email.endswith("@gitam.edu")
            ):
                raise ValidationError("Invalid Email Domain")
        except ValidationError:
            messages.error(request, "Invalid email")
            return render(request, "prelims/prelims_registration.html", context)

        if len(captain_phone) != 10 or not captain_phone.isdigit():
            messages.error(request, "Invalid Phone Number")
            return render(request, "prelims/prelims_registration.html", context)

        try:
            with transaction.atomic():
                team = Team.objects.create(
                    event=event,
                    visible_name=visible_team_name,
                    captain_email=captain_email,
                )
                team.save()

                try:
                    captain = Participant.objects.create(
                        name=captain_name,
                        email=captain_email,
                        phone_number=captain_phone,
                        registration_number=captain_regnum,
                        campus=captain_campus,
                        event=event,
                        team=team,
                        isCaptain=True,
                    )
                    captain.save()

                    team.participants.add(captain)

                    teammates += f"{captain_name}, "
                except IntegrityError:
                    messages.error(
                        request, "You have already registered for this event"
                    )
                    team.delete()
                    return render(request, "prelims/prelims_registration.html", context)

                max_team_size = int(event.max_team_size)
                for i in range(2, max_team_size + 1):
                    if f"name_{i}" in request.POST:
                        name = request.POST.get(f"name_{i}")
                        email = request.POST.get(f"email_{i}")
                        phone = request.POST.get(f"phone_{i}")
                        regnum = request.POST.get(f"regnum_{i}").upper()
                        campus = request.POST.get(f"campus_{i}")

                        if Participant.objects.filter(
                            email=email, event=event
                        ).exists():
                            messages.error(
                                request,
                                f"Participant with email {email} and registration number {regnum} have already registered for {event.name}",
                            )
                            team.delete()
                            return render(
                                request, "prelims/prelims_registration.html", context
                            )

                        try:
                            validate_email(email)
                            if not (
                                email.endswith("@gitam.in")
                                or email.endswith("@gitam.edu")
                            ):
                                raise ValidationError("Invalid Email Domain")
                        except ValidationError:
                            messages.error(request, "Invalid email")
                            return render(
                                request, "prelims/prelims_registration.html", context
                            )

                        if len(phone) != 10 or not phone.isdigit():
                            messages.error(request, "Invalid Phone Number")
                            return render(
                                request, "prelims/prelims_registration.html", context
                            )

                        try:
                            participant = Participant.objects.create(
                                name=name,
                                email=email,
                                phone_number=phone,
                                registration_number=regnum,
                                campus=campus,
                                event=event,
                                team=team,
                                isCaptain=False,
                            )
                            participant.save()

                            team.participants.add(participant)

                            teammates += f"{name}, "
                        except IntegrityError:
                            messages.error(
                                request,
                                f"Participant with registration number {regnum} have already registered for {event.name}",
                            )
                            team.delete()
                            return render(
                                request, "prelims/prelims_registration.html", context
                            )
                    else:
                        break
                team.teammates = teammates
                team.save()

                send_email_async(send_success_email, team.captain_email)
        except IntegrityError:
            messages.error(request, "Team Name already exists")
            return render(request, "prelims/prelims_registration.html", context)

        return redirect("prelims:dashboard")

    return render(request, "prelims/prelims_registration.html", context)


@login_required(login_url="home:login")
def dashboard(request):
    if request.user.is_authenticated:
        context = {}

        teams = Team.objects.filter(captain_email=request.user.email)
        context["teams"] = teams

        return render(request, "prelims/prelims_dash_cap.html", context)

    return redirect("home:login")


@login_required(login_url="home:login")
def prelims_admin_dashboard(request):
    if request.user.is_authenticated:
        if (
            request.user.events_cultural
            or request.user.events_cultural_staff
            or request.user.is_superuser
        ):

            context = {}

            teams = Team.objects.all()
            total_teams = teams.count()
            unique_participants_count = (
                Participant.objects.values("email").distinct().count()
            )

            context["teams"] = teams
            context["total_teams"] = total_teams
            context["total_participants"] = unique_participants_count

            return render(request, "prelims/dashboard_prelims_admin.html", context)
        messages.error(request, "You are not authorized to access the page")
        return redirect("prelims:dashboard")

    return redirect("home:login")


@login_required(login_url="home:login")
def upload_file(request, team_hash):
    if request.user.is_authenticated:
        team = Team.objects.get(team_hash=team_hash)
        if not team.reference_attatchment:
            if team.captain_email == request.user.email:
                if request.POST:
                    file = request.FILES.get("file")
                    
                    # Check if the uploaded file size is less than 10 MB
                    if file.size > 10 * 1024 * 1024:  # 10 MB
                        messages.error(request, "File size must be less than 10 MB")
                        return redirect("prelims:dashboard")
                    
                    team.reference_attatchment = file
                    team.save()

                    messages.success(request, "File uploaded successfully")
                    return redirect("prelims:dashboard")
                else:
                    return render(request, "prelims/upload_files.html")            
            else:
                messages.error(request, "Only captain can upload the file")
                return redirect("prelims:dashboard")
        else:
            messages.error(request, "Already uploaded attachment")
            return redirect("prelims:dashboard")

    return redirect("home:login")

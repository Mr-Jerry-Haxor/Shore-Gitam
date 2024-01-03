from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from .models import College, Event, Team, Participants, Hackathon, HackathonTeam, HackathonParticipants


def send_pass_mail(team_id, event_id):
    team = Team.objects.get(team_id=team_id)
    event = Event.objects.get(event_id=event_id)

    # get all the participants of the team
    participants = Participants.objects.filter(team=team)
    participant_emails = [ participant.email for participant in participants ]
    
    subject, from_email= f"SHORE'24 GITAM,Thank you for Registering", settings.EMAIL_HOST_USER
    html_content1 = get_template('registered_mail.html').render({
        "event": event, "team": team, "teammates": participants,
        "status_link":  f'https://shore.gitam.edu/registrations/success/{team.team_hash}'
    })
    msg = EmailMultiAlternatives(subject, html_content1, from_email, participant_emails)
    msg.content_subtype = "html"
    msg.send() 

def send_pass_mail_hackathon(team_id, event_id):
    team = HackathonTeam.objects.get(team_id=team_id)
    event = Hackathon.objects.get(event_id=event_id)

    # get all the participants of the team
    participants = HackathonParticipants.objects.filter(team=team)
    participant_emails = [ participant.email for participant in participants ]
    
    subject, from_email= f"SHORE'24 GITAM,Thank you for Registering", settings.EMAIL_HOST_USER
    html_content1 = get_template('registered_mail.html').render({
        "event": event, "team": team, "teammates": participants,
        "status_link":  f'https://shore.gitam.edu/registrations/hackathon/success/{team.team_hash}'
    })
    msg = EmailMultiAlternatives(subject, html_content1, from_email, participant_emails)
    msg.content_subtype = "html"
    msg.send() 


def send_pass_mail_updated(team_id, event_id):
    team = Team.objects.get(team_id=team_id)
    event = Event.objects.get(event_id=event_id)

    # get all the participants of the team
    participants = Participants.objects.filter(team=team)
    participant_emails = [ participant.email for participant in participants ]
    
    subject, from_email= f"SHORE'24 GITAM, Your team status is updated to {team.status}", settings.EMAIL_HOST_USER
    html_content1 = get_template('registered_mail.html').render({
        "event": event, "team": team, "teammates": participants,
        "status_link":  f'https://shore.gitam.edu/registrations/success/{team.team_hash}',
        "status_text" : f"Your Team status is updated to {team.status}",
    })
    msg = EmailMultiAlternatives(subject, html_content1, from_email, participant_emails)
    msg.content_subtype = "html"
    msg.send() 


def event_home(request):
    # messages.success(request,"Welcome to Shore24 ,GITAM's Biggest Fest Ever")
    return render(request, "event_home.html")


def sports_home(request):
    context = {}
    events = Event.objects.filter(event_type="sports")
    context["events"] = events
    context["title"] = "Sports"

    return render(request, "eventspage.html", context)


def culturals_home(request):
    context = {}
    events = Event.objects.filter(event_type="cultural").all()
    context["events"] = events
    context["title"] = "Culturals"

    return render(request, "eventspage.html", context)


def selectCollege(request, sport_name):
    context = {}
    colleges = College.objects.all()
    context["colleges"] = colleges
    context["sport_name"] = sport_name

    if request.method == "POST":
        college_id = request.POST.get("college")
        passkey = request.POST.get("passkey")

        college = College.objects.get(college_id=college_id)
        if college.passkey == passkey:
            request.session["college_name"] = college.name
            request.session["passkey_valid"] = True
            return redirect("events:register", sport_name=sport_name)
        else:
            messages.error(request, "Invalid passkey.")
            return render(request, "selectCollege.html", context)

    return render(request, "selectCollege.html", context)

@login_required(login_url="/auth/login/google-oauth2/")
def addCollege(request):
    if request.user.events_cultural or request.user.events_cultural_staff or request.user.events_sports or request.user.events_sports_staff:
        context = {}
        if request.POST:
            name = request.POST.get("college_name")
            abbreviation = request.POST.get("college_ab")
            passkey = request.POST.get("college_passkey")

            try:
                college = College.objects.create(
                    name=name, abbreviation=abbreviation, passkey=passkey
                )
                college.save()
                messages.success(
                    request,
                    f"College with name {name} abbreviation {abbreviation} added successfully.",
                )
                return render(request, "addCollege.html", context)
            except IntegrityError:
                messages.error(
                    request,
                    f"College with name {name} abbreviation {abbreviation} already exists.",
                )
                return render(request, "addCollege.html", context)

        return render(request, "addCollege.html")
    else:
        messages.error(request, "You are not authorized to access this page.")
        return render(request, "index")

@login_required(login_url="/auth/login/google-oauth2/")
def addEvent(request):
    context = {}
    if request.user.events_sports or request.user.events_cultural:
        if request.POST:
            name = request.POST.get("sport_name")
            event_type = request.POST.get("event_type")
            min_team_size = request.POST.get("team_size")
            max_team_size = request.POST.get("max_team_size")
            no_of_teams = request.POST.get("no_of_teams")
            no_of_teams_college = request.POST.get("no_of_teams_college")

            if (
                int(min_team_size) <= 0
                or int(no_of_teams) <= 0
                or int(max_team_size) <= 0
                or int(no_of_teams_college) <= 0
            ):
                messages.error(
                    request,
                    "Team size, no of teams, team from each college cannot be zero.",
                )
                return render(request, "addEvent.html", context)

            if int(min_team_size) > int(max_team_size):
                messages.error(
                    request, "Minimum team size cannot be greater than max team size."
                )
                return render(request, "addEvent.html", context)

            try:
                sport = Event.objects.create(
                    name=name,
                    event_type=event_type,
                    min_team_size=min_team_size,
                    max_team_size=max_team_size,
                    no_of_teams=no_of_teams,
                    max_univeristy_teams=no_of_teams_college,
                )
                sport.save()
                messages.success(
                    request,
                    f"Event with name {name} and team size {min_team_size} - {max_team_size} added successfully.",
                )
                return render(request, "addEvent.html", context)
            except IntegrityError:
                messages.error(
                    request,
                    f"Event with name {name} and team size {min_team_size} - {max_team_size} already exists.",
                )
                return render(request, "addEvent.html", context)
    else:
        messages.error(request, "You do not have access for this page!!")
        return redirect("index")
    return render(request, "addEvent.html", context)

def register(request, sport_name):
    context = {}
    passkey_status = request.session.get("passkey_valid")
    if not passkey_status:
        messages.error(request, "Invalid passkey.")
        return redirect("events:selectCollege", sport_name=sport_name)
    college_name = request.session.get("college_name")
    if college_name == "Other":
        context["passkey_not_required"] = True
    college = College.objects.get(name=college_name)
    sport = Event.objects.get(name=sport_name)
    allowed_team_count = sport.no_of_teams

    if (Team.objects.filter(college=college, sport=sport).count() >= sport.max_univeristy_teams):
        messages.error(request, f"Max registrations for {sport.name} from {college.name} received")
        return redirect("events:eventshome")

    context["team_size"] = range(2, sport.min_team_size + 1)
    context["sport"] = sport
    context["college"] = college

    if request.POST:
        visible_team_name = request.POST.get("team_name")
        endorsementFile = request.FILES.get("endorsment_file")

        team_name = college.abbreviation + "_" + sport.name
        teams_count = Team.objects.all().count()

        if (
            Team.objects.filter(college=college, sport=sport).count()
            < sport.max_univeristy_teams
        ):
            try:
                team = Team.objects.create(
                    team_name=team_name,
                    visible_name=visible_team_name,
                    college=college,
                    sport=sport,
                    isWaiting=True if teams_count > allowed_team_count else False,
                    endorsment_file=endorsementFile
                )
                team.save()
                
            except IntegrityError:
                messages.error(request, f"Team with name {visible_team_name} already exists.")
                return render(request, "register_new.html", context)

            captain_name = request.POST.get("name_1")
            captain_email = request.POST.get("email_1")
            captain_phone_number = request.POST.get("phone_1")
            captain_accomdation = request.POST.get("accomdation_1")

            # if event type is cultural, then a participant is atmost allowed to participate in only 2 culturals
            if sport.event_type == 'cultural':
                if Participants.objects.filter(email=captain_email).count() == 2:
                    messages.error(request, f"A participant is allowed to participant atmost in only two culturals. {captain_name} already registered for 2 cultural events.")
                    return redirect("events:eventshome")

            # phone number length should be 10 and should be digits
            if (
                len(captain_phone_number) != 10
                or not captain_phone_number.isdigit()
            ):
                messages.error(
                    request,
                    f"Invalid phone number {captain_phone_number}.",
                )
                team.delete()
                return render(request, "register_new.html", context)

            # validate email
            try:
                validate_email(captain_email)
            except ValidationError:
                messages.error(
                    request,
                    f"Invalid email {captain_email}.",
                )
                team.delete()
                return render(request, "register_new.html", context)

            try:
                captain = Participants.objects.create(
                    name=captain_name,
                    email=captain_email,
                    phone_number=captain_phone_number,
                    accomdation=True if captain_accomdation == "yes" else False,
                    college=college,
                    sport=sport,
                    team=team,
                    isCaptain=True,
                )
                captain.save()
            except IntegrityError:
                messages.error(
                    request,
                    f"Participant with {captain_email} or {captain_phone_number} already registered.",
                )
                team.delete()
                return render(request, "register_new.html", context)

            for i in range(2, sport.max_team_size + 1):
                if f"name_{i}" not in request.POST:
                    break
                name = request.POST.get(f"name_{i}")
                email = request.POST.get(f"email_{i}")
                phone_number = request.POST.get(f"phone_{i}")
                accomdation = request.POST.get(f"accomdation_{i}")

                if sport.event_type == 'cultural':
                    if Participants.objects.filter(email=email).count() == 2:
                        messages.error(request, f"A participant is allowed to participant atmost in only two culturals. {name} already registered for 2 cultural events.")
                        return redirect("events:eventshome")

                # phone number length should be 10 and should be digits
                if len(phone_number) != 10 or not phone_number.isdigit():
                    messages.error(
                        request,
                        f"Invalid phone number {phone_number}.",
                    )
                    team.delete()
                    return render(request, "register_new.html", context)

                # validate email
                try:
                    validate_email(email)
                except ValidationError:
                    messages.error(
                        request,
                        f"Invalid email {email}.",
                    )
                    team.delete()
                    return render(request, "register_new.html", context)

                try:
                    player = Participants.objects.create(
                        name=name,
                        email=email,
                        phone_number=phone_number,
                        accomdation=True if accomdation == "yes" else False,
                        college=college,
                        sport=sport,
                        team=team,
                    )
                    player.save()
                except IntegrityError:
                    messages.error(
                        request,
                        f"Participant with {email} or {phone_number} already registered.",
                    )
                    team.delete()
                    return render(request, "register_new.html", context)

            messages.success(
                request, f"Team {team.visible_name} registered successfully."
            )

            # sending email
            send_pass_mail(team_id=team.team_id, event_id=sport.event_id)

            return redirect("events:success", team_hash=team.team_hash)
            # return render(request, "success.html", context)
        else:
            messages.error(
                request,
                f"Limit reached for {college.name} for {sport.name}.",
            )
            return render(request, "register_new.html", context)
    return render(request, "register_new.html", context)


def success(request, team_hash):
    # complete success page, add team hash to view their team status, add functionality to send emails on successful registration.
    context = {}
    team = Team.objects.get(team_hash=team_hash)
    players = Participants.objects.filter(team=team)

    context["team"] = team
    context["players"] = players

    return render(request, "success.html", context)


@login_required(login_url="/auth/login/google-oauth2/")
def registered_sports(request, sport_name):
    if request.user.events_sports or request.user.events_sports_staff:
        context = {}
        sport = Event.objects.get(name=sport_name)
        teams = Team.objects.filter(sport=sport).all
        context["teams"] = teams
        context["sport"] = sport

        return render(request, "registered_sports.html", context)
    else:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("events:eventshome")


@login_required(login_url="/auth/login/google-oauth2/")
def registered_culturals(request, sport_name):
    if request.user.events_cultural or request.user.events_cultural_staff:
        context = {}
        sport = Event.objects.get(name=sport_name)
        teams = Team.objects.filter(sport=sport).all
        context["teams"] = teams
        context["sport"] = sport

        return render(request, "registered_culturals.html", context)
    else:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("events:eventshome")


@login_required(login_url="/auth/login/google-oauth2/")
def view_team(request, team_hash):
    if request.user.events_cultural or request.user.events_cultural_staff or request.user.events_sports or request.user.events_sports_staff:
        context = {}
        team = Team.objects.get(team_hash=team_hash)
        participants = Participants.objects.filter(team=team)

        context["team"] = team
        context["participants"] = participants

        if request.method == "POST":
            new_status = request.POST.get("status-radio")
            team.status = new_status
            team.save()
            messages.success(
                request, f"Team {team.visible_name} status changed to {new_status}."
            )

            # sending emails to all the participants upon status change
            send_pass_mail_updated(team_id=team.team_id, event_id=team.sport.event_id)

            if team.sport.event_type == "sports":
                return redirect("events:registered_sports", sport_name=team.sport.name)
            else:
                return redirect("events:registered_culturals", sport_name=team.sport.name)

        return render(request, "view_team.html", context)
    else:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("events:eventshome")


@login_required(login_url="/auth/login/google-oauth2/")
def events_admin_sports(request):
    if request.user.events_sports or request.user.events_sports_staff:
        context = {}
        sports = Event.objects.filter(event_type="sports").all()

        context["events"] = sports

        return render(request, "events_admin_sports.html", context)
    else:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("events:eventshome")


@login_required(login_url="/auth/login/google-oauth2/")
def events_admin_culturals(request):
    if request.user.events_cultural or request.user.events_cultural_staff:
        context = {}
        sports = Event.objects.filter(event_type="cultural").all()

        context["events"] = sports

        return render(request, "events_admin_culturals.html", context)
    else:
        messages.error(request, "You are not authorized to access this page.")
        return redirect("events:eventshome")

""" Hackathon Views """
def hackathon_home(request):
    context = {}
    hackathons = Hackathon.objects.all()
    
    context["isHackathon"] = True
    context["events"] = hackathons
    context["title"] = "Hackathons"

    return render(request, "eventspage.html", context)


def select_hackathon_college(request, hackathon_name):
    context = {}
    colleges = College.objects.all()
    context["isHackathon"] = True
    context["colleges"] = colleges
    context["hackathon_name"] = hackathon_name

    if request.method == "POST":
        college_id = request.POST.get("college_name")
        college = College.objects.get(college_id=college_id)

        request.session["college_name"] = college.name
        request.session["passkey_valid"] = True

        return redirect("events:hackathon_register", hackathon_name=hackathon_name)

    return render(request, "hackathon/hackathon_selectCollege.html", context)


def register_hackathon(request, hackathon_name):
    context = {
        "isHackathon": True
    }
    
    college_name = request.session.get("college_name")
    college = College.objects.get(name=college_name)
    hackathon = Hackathon.objects.get(name=hackathon_name)
    
    context["college"] = college
    context["sport"] = hackathon
    context["team_size"] = range(2, hackathon.min_team_size + 1)

    if request.POST:
        visible_team_name = request.POST.get("team_name")
        endorsementFile = request.FILES.get("endorsment_file")

        team_name = college.abbreviation + "_" + hackathon.name
        teams_count = HackathonTeam.objects.all().count()

        try:
            team = HackathonTeam.objects.create(
                team_name=team_name,
                visible_name=visible_team_name,
                college=college,
                hackathon=hackathon,
                endorsment_file=endorsementFile
            )
            team.save()
        except IntegrityError:
            messages.error(request, f"Team with name {visible_team_name} already exists.")
            return render(request, "hackathon/hackathon_register.html", context)
        
        captain_name = request.POST.get("name_1")
        captain_email = request.POST.get("email_1")
        captain_phone_number = request.POST.get("phone_1")
        captain_accomdation = request.POST.get("accomdation_1")

        # phone number length should be 10 and should be digits
        if (
            len(captain_phone_number) != 10
            or not captain_phone_number.isdigit()
        ):
            messages.error(
                request,
                f"Invalid phone number {captain_phone_number}.",
            )
            team.delete()
            return render(request, "hackathon/hackathon_register.html", context)
        
        # validate email
        try:
            validate_email(captain_email)
        except ValidationError:
            messages.error(
                request,
                f"Invalid email {captain_email}.",
            )
            team.delete()
            return render(request, "hackathon/hackathon_register.html", context)
        
        try:
            captain = HackathonParticipants.objects.create(
                name=captain_name,
                email=captain_email,
                phone_number=captain_phone_number,
                accomdation=True if captain_accomdation == "yes" else False,
                college=college,
                hackathon=hackathon,
                team=team,
                isCaptain=True,
            )
            captain.save()
        except IntegrityError:
            messages.error(
                request,
                f"Participant with {captain_email} or {captain_phone_number} already registered.",
            )
            team.delete()
            return render(request, "hackathon/hackathon_register.html", context)
        
        for i in range(2, hackathon.max_team_size + 1):
            if f"name_{i}" not in request.POST:
                break
            name = request.POST.get(f"name_{i}")
            email = request.POST.get(f"email_{i}")
            phone_number = request.POST.get(f"phone_{i}")
            accomdation = request.POST.get(f"accomdation_{i}")

            # phone number length should be 10 and should be digits
            if len(phone_number) != 10 or not phone_number.isdigit():
                messages.error(
                    request,
                    f"Invalid phone number {phone_number}.",
                )
                team.delete()
                return render(request, "hackathon/hackathon_register.html", context)

            # validate email
            try:
                validate_email(email)
            except ValidationError:
                messages.error(
                    request,
                    f"Invalid email {email}.",
                )
                team.delete()
                return render(request, "hackathon/hackathon_register.html", context)

            try:
                player = HackathonParticipants.objects.create(
                    name=name,
                    email=email,
                    phone_number=phone_number,
                    accomdation=True if accomdation == "yes" else False,
                    college=college,
                    hackathon=hackathon,
                    team=team,
                )
                player.save()
            except IntegrityError:
                messages.error(
                    request,
                    f"Participant with {email} or {phone_number} already registered.",
                )
                team.delete()
                return render(request, "hackathon/hackathon_register.html", context)
        
        messages.success(
            request, f"Team {team.visible_name} registered successfully."
        )

        # sending email
        try:
            send_pass_mail_hackathon(team_id=team.team_id, event_id=hackathon.event_id)
        except Exception as e:
            print(e)
            messages.error(request, "Error sending email. Please contact the organizers.")
            team.delete()

        # creating login accounts for all the participants

        return redirect("events:hackathon_success", team_hash=team.team_hash)

    return render(request, "hackathon/hackathon_register.html", context)


def hackathon_success(request, team_hash):
    context = {}
    team = HackathonTeam.objects.get(team_hash=team_hash)
    players = HackathonParticipants.objects.filter(team=team)

    context["team"] = team
    context["players"] = players

    return render(request, "hackathon/hackathon_success.html", context)

@login_required(login_url="/auth/login/google-oauth2/")
def registered_hackathon(request):
    if request.user.events_cultural or request.user.events_cultural_staff:
        context = {}
        teams = HackathonTeam.objects.all
        context["teams"] = teams

        return render(request, "hackathon_registered.html", context)

@login_required(login_url="/auth/login/google-oauth2/")
def hackathon_admin(request):
    # should add hackathon staff, hackathon admin
    context = {}
    teams = HackathonTeam.objects.all()
    context["teams"] = teams
    return render(request, "hackathon/hackathon_admin.html", context)

@login_required(login_url="/auth/login/google-oauth2/")
def view_hackathon_team(request, team_hash):
    # if request.user.events_cultural or request.user.events_cultural_staff:  # change this line
        context = {}
        team = HackathonTeam.objects.get(team_hash=team_hash)
        participants = HackathonParticipants.objects.filter(team=team)

        context["team"] = team
        context["participants"] = participants

        if request.method == "POST":
            new_status = request.POST.get("status-radio")
            team.status = new_status
            team.save()
            messages.success(
                request, f"Team {team.visible_name} status changed to {new_status}."
            )
            return redirect("events:hackathon_admin")

        return render(request, "hackathon/hackathon_view_team.html", context)
    # else:
    #     messages.error(request, "You are not authorized to access this page.")
    #     return redirect("events:eventshome")

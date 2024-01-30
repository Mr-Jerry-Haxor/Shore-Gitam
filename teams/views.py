from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import ParticipantApplication, Domain


def team(request):
    context = {}
    context['domains'] = Domain.objects.all().order_by('order')
    # Query all Participant applications
    all_applications = ParticipantApplication.objects.select_related('domain').order_by('domain__order')

    # Group applications by domain and position for easier rendering in the template
    applications_by_domain = {}
    for application in all_applications:
        domain_name = application.domain.name
        position = application.position

        if domain_name not in applications_by_domain:
            applications_by_domain[domain_name] = {}

        if position not in applications_by_domain[domain_name]:
            applications_by_domain[domain_name][position] = []

        applications_by_domain[domain_name][position].append(application)

    order = ['Head', 'Co-head', 'Lead', 'Co-lead', 'Member']

    for key in applications_by_domain:
        sorted_dict = {k: applications_by_domain[key][k] for k in order if k in applications_by_domain[key]}
        sorted_dict.update({k: applications_by_domain[key][k] for k in applications_by_domain[key] if k not in order})
        applications_by_domain[key] = sorted_dict

    context['applications_by_domain'] = applications_by_domain

    return render(request, "teams/team.html", context)


@login_required(login_url="ngusers:login")
def apply(request):
    context = {}
    email = request.user.email
    context['positions'] = ['Head', 'Co-head', 'Lead', 'Co-lead', 'Member']

    if not ParticipantApplication.objects.filter(email=email).exists():
        context["email"] = email
        context["domains"] = Domain.objects.all()
        if request.POST:
            name = request.POST["name"]
            domain = request.POST["domain"]
            position = request.POST["position"]
            designation = request.POST["designation"]
            instagram_url = request.POST["instagram_url"]
            linkedin_url = request.POST["linkedin_url"]
            profile_pic = request.FILES["profile_pic"]

            domain_obj = Domain.objects.get(name=domain)
            application = ParticipantApplication(
                name=name,
                email=email,
                domain=domain_obj,
                position=position,
                designation=designation,
                instagram_url=instagram_url,
                linkedin_url=linkedin_url,
                profile_pic=profile_pic,
            )

            application.save()
            messages.success(
                request,
                "Application submitted successfully. Verification is pending.")
            return redirect("teams:view_application")
    else:
        messages.info(request, "You have already submitted an application.")
        return redirect("teams:view_application")
    # return render(request, "teams/apply1.html", context)
    return render(request, "teams/apply.html", context)


@login_required(login_url="ngusers:login")
def view_application(request):
    context = {}
    context["domains"] = Domain.objects.all()
    context['positions'] = ['President', 'Vice-President', 'Event Manager' 'Head', 'Co-head', 'Lead', 'Co-lead', 'Member']
    email = request.user.email
    try:
        application = ParticipantApplication.objects.get(email=email)
        context["application"] = application
    except ParticipantApplication.DoesNotExist:
        messages.info(request, "You have not submitted an application yet.")
        return redirect("teams:apply")

    if request.POST:
        # position = request.POST["position"]
        application.name = request.POST["name"]
        new_domain = request.POST["domain"]
        application.domain = Domain.objects.get(name=new_domain)
        application.designation = request.POST["designation"]
        application.instagram_url = request.POST["instagram_url"]
        application.linkedin_url = request.POST["linkedin_url"]
        if "profile_pic" in request.FILES:
            application.profile_pic = request.FILES["profile_pic"]
        application.verified = False
        application.save()

        messages.success(request, "Application updated successfully.")
        return redirect("teams:view_application")

    return render(request, "teams/view_application.html", context)


@login_required(login_url="ngusers:login")
def verify_application(request):
    context = {}
    email = request.user.email

    try:
        all_domains = Domain.objects.all()
        for domain in all_domains:
            accepted_emails = domain.head_email.split(",")
            if email in accepted_emails:
                actual_domain = domain
            else:
                actual_domain = False

        if not actual_domain:
            raise Domain.DoesNotExist

        applications = ParticipantApplication.objects.filter(domain=actual_domain).order_by(
            "verified", "name"
        )
        context["applications"] = applications
    except Domain.DoesNotExist:
        messages.info(request, "You are not authorised to verify applications.")
        return redirect("teams:apply")

    return render(request, "teams/verify_application.html", context)


@login_required(login_url="ngusers:login")
def verify_individual_application(request, email):
    logged_in_user_email = request.user.email
    try:
        domain = Domain.objects.get(head_email=logged_in_user_email)
        application = ParticipantApplication.objects.get(email=email)

        if application.domain == domain:
            application.verified = True
            application.save()
            messages.success(
                request,
                f"{application.name}'s application verified successfully.",
            )
            return redirect("teams:verify_application")
        else:
            messages.info(
                request,
                "You are not authorised to verify applications from other domains.",
            )
            return redirect("teams:apply")
    except Domain.DoesNotExist:
        messages.info(request, "You are not authorised to verify applications.")
        return redirect("teams:apply")
    except ParticipantApplication.DoesNotExist:
        messages.info(request, "Application does not exist.")
        return redirect("teams:verify_application")


@login_required(login_url="ngusers:login")
def disprove_individual_application(request, email):
    logged_in_user_email = request.user.email
    try:
        domain = Domain.objects.get(head_email=logged_in_user_email)
        application = ParticipantApplication.objects.get(email=email)

        if application.domain == domain:
            application.verified = False
            application.save()
            messages.success(
                request,
                f"{application.name}'s application disapproved successfully.",
            )
            return redirect("teams:verify_application")
        else:
            messages.info(
                request,
                "You are not authorised to disapprove applications from other domains.",
            )
            return redirect("teams:apply")
    except Domain.DoesNotExist:
        messages.info(request, "You are not authorised to disapprove applications.")
        return redirect("teams:apply")
    except ParticipantApplication.DoesNotExist:
        messages.info(request, "Application does not exist.")
        return redirect("teams:verify_application")

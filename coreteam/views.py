from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from coreteam.models import CustomUser
from hospitality.models import *
from security.models import security_staff


@login_required(login_url="/auth/login/google-oauth2/")
def submit_task(request, task_id):
    context = {}
    if request.method == "POST":
        submission_url = request.POST.get("submission_url")

        if submission_url is None or submission_url == "":
            messages.error(request, "Submission URL is required")
            return redirect("submit_task", task_id=task_id)

        task = Task.objects.get(id=task_id)
        task.status = "Completed"
        task.submission_url = submission_url
        task.save()

        if not settings.DEVELOPMENT:
            sendmail_submission(task_id)
        else:
            print("\nEmails not sent in development mode\n")

        messages.success(request, "Task submitted successfully")
        return redirect("coretasks", domain_name=task.domain)
    task = Task.objects.get(id=task_id)
    context["task"] = task

    return render(request, "submit_task.html", context)


@login_required(login_url="/auth/login/google-oauth2/")
def remove_submission(request, task_id):
    task = Task.objects.get(id=task_id)

    if not getattr(request.user, task.domain, False):
        print("\nUser does not have permission to remove this submission\n")

        messages.error(request, "You do not have permission to remove this submission")
        return redirect("coretasks", domain_name=task.domain)

    task.status = "In Progress"
    task.submission_url = ""
    task.save()

    messages.success(request, "Submission removed successfully")
    return redirect("coretasks", domain_name=task.domain)


@login_required(login_url="/auth/login/google-oauth2/")
def give_access_to_domain_head(request):
    access_emails = []
    if (
        request.user.is_superuser
        or request.user.president
        or (request.user.email in access_emails)
    ):
        if request.method == "POST":
            head_email = request.POST.get("domain_head_email")
            domain = request.POST.get("domain")

            try:
                user = CustomUser.objects.get(email=head_email)

                if user.__dict__[domain]:
                    messages.error(
                        request,
                        f"User with email {head_email} already has access to {domain}",
                    )
                    return redirect("domain_heads")

                user.__dict__[domain] = True
                user.save()

                messages.success(
                    request,
                    f"User with email {head_email} has been given access to {domain}",
                )
                return redirect("domain_heads")
            except CustomUser.DoesNotExist:
                messages.error(request, f"User with email {head_email} does not exist")
                return redirect("domain_heads")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect("domain_heads")

        return render(request, "add_domains.html")
    else:
        messages.error(request, "You do not have permission to access this page")
        return redirect("corehome")


# Define accessible domains by role, including 'coordinator' and 'alltasks' permissions
role_domains = {
    "coordinator": [
        "alltasks",
        "president",
        "vice_president",
        "campus_head_hyd",
        "campus_head_blr",
        "technology",
        "events_cultural",
        "events_sports",
        "legal",
        "operations",
        "marketing",
        "sponsorship",
        "design",
        "finance",
        "media",
        "security",
        "hospitality",
    ],
    "president": [
        "alltasks",
        "president",
        "vice_president",
        "campus_head_hyd",
        "campus_head_blr",
        "technology",
        "events_cultural",
        "events_sports",
        "legal",
        "operations",
        "marketing",
        "sponsorship",
        "design",
        "finance",
        "media",
        "security",
        "hospitality",
    ],
    "vice_president": [
        "vice_president",
        "campus_head_hyd",
        "campus_head_blr",
        "technology",
        "events_cultural",
        "events_sports",
        "legal",
        "operations",
        "marketing",
        "sponsorship",
        "design",
        "finance",
        "media",
        "security",
        "hospitality",
    ],
    "technology": ["technology"],
    "events_cultural": ["events_cultural"],
    "events_sports": ["events_sports"],
    "legal": ["legal"],
    "operations": ["operations"],
    "marketing": ["marketing"],
    "sponsorship": ["sponsorship"],
    "design": ["design"],
    "finance": ["finance"],
    "media": ["media"],
    "security": ["security"],
    "hospitality": ["hospitality"],
}


@login_required(login_url="/auth/login/google-oauth2/")
def coretasks(request, domain_name):

    # Map each domain to its Task domain value for querying
    domain_mapping = {
        "campus_head_hyd": "campus_head_hyd",
        "campus_head_blr": "campus_head_blr",
        "president": "president",
        "vice_president": "vice_president",
        "technology": "technology",
        "events_cultural": "events_cultural",
        "events_sports": "events_sports",
        "legal": "legal",
        "operations": "operations",
        "marketing": "marketing",
        "sponsorship": "sponsorship",
        "design": "design",
        "finance": "finance",
        "media": "media",
        "security": "security",
        "hospitality": "hospitality",
        "alltasks": None,  # 'alltasks' is a special case where all tasks are retrieved
    }

    # Define user permissions based on their role attributes
    user_permissions = {
        "campus_head_hyd": getattr(request.user, "campus_head_hyd", False),
        "campus_head_blr": getattr(request.user, "campus_head_blr", False),
        "coordinator": getattr(request.user, "coordinator", False),
        "president": request.user.is_staff and getattr(request.user, "president", False),
        "vice_president": getattr(request.user, "vice_president", False),
        "technology": getattr(request.user, "technology", False),
        "events_cultural": getattr(request.user, "events_cultural", False),
        "events_sports": getattr(request.user, "events_sports", False),
        "legal": getattr(request.user, "legal", False),
        "operations": getattr(request.user, "operations", False),
        "marketing": getattr(request.user, "marketing", False),
        "sponsorship": getattr(request.user, "sponsorship", False),
        "design": getattr(request.user, "design", False),
        "finance": getattr(request.user, "finance", False),
        "media": getattr(request.user, "media", False),
        "security": getattr(request.user, "security", False),
        "hospitality": getattr(request.user, "hospitality", False),
    }

    if request.user.campus_head_hyd and domain_name == "campus_head_hyd":
        tasks = Task.objects.filter(domain="campus_head_hyd").order_by("-due_date")
        dashcontext = {
            "tasks": tasks,
            "domain": domain_name,
        }
        return render(request, "dashboard.html", dashcontext)
    
    if request.user.campus_head_blr and domain_name == "campus_head_blr":
        tasks = Task.objects.filter(domain="campus_head_blr").order_by("-due_date")
        dashcontext = {
            "tasks": tasks,
            "domain": domain_name,
        }
        return render(request, "dashboard.html", dashcontext)

    if request.user.coordinator and domain_name == "coordinator":
        tasks = Task.objects.filter(coordinator=True).order_by("-due_date")
        dashcontext = {
            "tasks": tasks,
            "domain": domain_name,
        }
        return render(request, "dashboard.html", dashcontext)

    # Check if the user has access to the requested domain
    for role, domains in role_domains.items():
        if user_permissions.get(role) and domain_name in domains:
            tasks = (
                Task.objects.filter(domain=domain_mapping[domain_name]).order_by(
                    "-due_date"
                )
                if domain_mapping[domain_name]
                else Task.objects.all().order_by("-due_date")
            )
            dashcontext = {
                "tasks": tasks,
                "domain": domain_name,
            }
            return render(request, "dashboard.html", dashcontext)

    # Redirect if the user doesn't have permission for the requested domain
    return redirect("index")


@login_required(login_url="/auth/login/google-oauth2/")
def home(request):
    if request.user.is_authenticated:
        name = request.user.first_name
        ishospitality = HospitalityUser.objects.filter(
            email=request.user.email
        ).exists()
        issecurity = security_staff.objects.filter(email_id=request.user.email).exists()
        return render(
            request,
            "corehome_new.html",
            {"name": name, "ishospitality": ishospitality, "issecurity": issecurity},
        )
    else:
        return redirect("index")


def sendmail_submission(taskid):
    task = Task.objects.filter(id=taskid).values()[0]

    task_title = task["task_title"]
    domain = task["domain"]
    description = task["description"]
    priority = task["priority"]
    due_date = task["due_date"]
    status = task["status"]
    assigned_to = task["assigned_to"]
    assigned_by = task["assigned_by"]
    coordinator = task["coordinator"]
    submission_url = task["submission_url"]

    president_emails = CustomUser.objects.filter(president=True).values_list(
        "email", flat=True
    )
    vicepresident_emails = CustomUser.objects.filter(vice_president=True).values_list(
        "email", flat=True
    )
    domain_email_queries = {
        "technology": CustomUser.objects.filter(technology=True).values_list(
            "email", flat=True
        ),
        "events-cultural": CustomUser.objects.filter(events_cultural=True).values_list(
            "email", flat=True
        ),
        "events-sports": CustomUser.objects.filter(events_sports=True).values_list(
            "email", flat=True
        ),
        "legal": CustomUser.objects.filter(legal=True).values_list("email", flat=True),
        "operations": CustomUser.objects.filter(operations=True).values_list(
            "email", flat=True
        ),
        "marketing": CustomUser.objects.filter(marketing=True).values_list(
            "email", flat=True
        ),
        "sponsorship": CustomUser.objects.filter(sponsorship=True).values_list(
            "email", flat=True
        ),
        "design": CustomUser.objects.filter(design=True).values_list(
            "email", flat=True
        ),
        "finance": CustomUser.objects.filter(finance=True).values_list(
            "email", flat=True
        ),
        "media": CustomUser.objects.filter(media=True).values_list("email", flat=True),
        "security": CustomUser.objects.filter(security=True).values_list(
            "email", flat=True
        ),
        "hospitality": CustomUser.objects.filter(hospitality=True).values_list(
            "email", flat=True
        ),
    }

    domain_emails = domain_email_queries.get(domain, president_emails)

    emails_list = set(president_emails) | set(vicepresident_emails) | set(domain_emails)

    if coordinator:
        coordinator_emails = CustomUser.objects.filter(coordinator=True).values_list(
            "email", flat=True
        )
        emails_list |= set(coordinator_emails)

    emails_list = list(emails_list)

    subject = f"Shore25 Tasks: {task_title} Submitted"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("submittaskmail.html").render(
        {
            "task_title": task_title,
            "domain": domain,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "status": status,
            "assigned_to": assigned_to,
            "assigned_by": assigned_by,
            "submission_url": submission_url,
        }
    )

    msg = EmailMultiAlternatives(subject, html_content, from_email, emails_list)
    msg.content_subtype = "html"
    msg.send()


def sendmail_create(taskid):
    task = Task.objects.filter(id=taskid).values()[0]

    task_title = task["task_title"]
    domain = task["domain"]
    description = task["description"]
    priority = task["priority"]
    due_date = task["due_date"]
    status = task["status"]
    assigned_to = task["assigned_to"]
    assigned_by = task["assigned_by"]
    coordinator = task["coordinator"]

    president_emails = CustomUser.objects.filter(president=True).values_list(
        "email", flat=True
    )
    vicepresident_emails = CustomUser.objects.filter(vice_president=True).values_list(
        "email", flat=True
    )

    domain_email_queries = {
        "technology": CustomUser.objects.filter(technology=True).values_list(
            "email", flat=True
        ),
        "events-cultural": CustomUser.objects.filter(events_cultural=True).values_list(
            "email", flat=True
        ),
        "events-sports": CustomUser.objects.filter(events_sports=True).values_list(
            "email", flat=True
        ),
        "legal": CustomUser.objects.filter(legal=True).values_list("email", flat=True),
        "operations": CustomUser.objects.filter(operations=True).values_list(
            "email", flat=True
        ),
        "marketing": CustomUser.objects.filter(marketing=True).values_list(
            "email", flat=True
        ),
        "sponsorship": CustomUser.objects.filter(sponsorship=True).values_list(
            "email", flat=True
        ),
        "design": CustomUser.objects.filter(design=True).values_list(
            "email", flat=True
        ),
        "finance": CustomUser.objects.filter(finance=True).values_list(
            "email", flat=True
        ),
        "media": CustomUser.objects.filter(media=True).values_list("email", flat=True),
        "security": CustomUser.objects.filter(security=True).values_list(
            "email", flat=True
        ),
        "hospitality": CustomUser.objects.filter(hospitality=True).values_list(
            "email", flat=True
        ),
    }

    domain_emails = domain_email_queries.get(domain, president_emails)

    emails_list = set(president_emails) | set(vicepresident_emails) | set(domain_emails)

    if coordinator:
        coordinator_emails = CustomUser.objects.filter(coordinator=True).values_list(
            "email", flat=True
        )
        emails_list |= set(coordinator_emails)

    emails_list = list(emails_list)

    subject = f"Shore25 Tasks: {task_title} Created"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("createtaskmail.html").render(
        {
            "task_title": task_title,
            "domain": domain,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "status": status,
            "assigned_to": assigned_to,
            "assigned_by": assigned_by,
        }
    )

    msg = EmailMultiAlternatives(subject, html_content, from_email, emails_list)
    msg.content_subtype = "html"
    msg.send()


@login_required(login_url="/auth/login/google-oauth2/")
def createtask(request, domain_name):
    # Define user permissions based on their role attributes
    user_permissions = {
        "coordinator": getattr(request.user, "coordinator", False),
        "campus_head_hyd": getattr(request.user, "campus_head_hyd", False),
        "campus_head_blr": getattr(request.user, "campus_head_blr", False),
        "president": request.user.is_staff
        and getattr(request.user, "president", False),
        "vice_president": getattr(request.user, "vice_president", False),
        "technology": getattr(request.user, "technology", False),
        "events_cultural": getattr(request.user, "events_cultural", False),
        "events_sports": getattr(request.user, "events_sports", False),
        "legal": getattr(request.user, "legal", False),
        "operations": getattr(request.user, "operations", False),
        "marketing": getattr(request.user, "marketing", False),
        "sponsorship": getattr(request.user, "sponsorship", False),
        "design": getattr(request.user, "design", False),
        "finance": getattr(request.user, "finance", False),
        "media": getattr(request.user, "media", False),
        "security": getattr(request.user, "security", False),
        "hospitality": getattr(request.user, "hospitality", False),
    }
    Domain_choice = {
        "president": "President",
        "vice_president": "Vice President",
        "campus_head_hyd": "Campus Head - Hyderabad",
        "campus_head_blr": "Campus Head - Bangalore",
        "technology": "Technology",
        "events_cultural": "Events - Cultural",
        "events_sports": "Events - Sports",
        "legal": "Legal",
        "operations": "Operations",
        "marketing": "Marketing",
        "sponsorship": "Sponsorship",
        "design": "Design",
        "finance": "Finance",
        "media": "Media",
        "security": "Security",
        "hospitality": "Hospitality",
    }

    if request.method == "GET":
        assigned_by = f"{request.user.first_name} {request.user.last_name}"
        if (
            request.user.coordinator
            or request.user.president
            or request.user.vice_president
        ):
            DOMAIN_CHOICES = []
            for key, value in Domain_choice.items():
                DOMAIN_CHOICES.append((key, value))
            context = {"DOMAIN_CHOICES": DOMAIN_CHOICES, "assigned_by": assigned_by}
            return render(request, "createtask.html", context)
        elif (
            request.user.technology
            or request.user.events_cultural
            or request.user.events_sports
            or request.user.legal
            or request.user.operations
            or request.user.marketing
            or request.user.sponsorship
            or request.user.design
            or request.user.finance
            or request.user.media
            or request.user.security
            or request.user.hospitality
        ):
            DOMAIN_CHOICES = []
            for key, value in user_permissions.items():
                if value:
                    DOMAIN_CHOICES.append((key, Domain_choice[key]))
            context = {"DOMAIN_CHOICES": DOMAIN_CHOICES, "assigned_by": assigned_by}
            return render(request, "createtask.html", context)
        else:
            return redirect("corehome")
    elif request.method == "POST":
        domain = request.POST.get("domain")
        authorized = False
        # if anyone user_permissions are true and doamin is in role permissions then only they can create task
        for role, domains in role_domains.items():
            if user_permissions.get(role):
                if domain in domains:
                    authorized = True
        if authorized:
            task_title = request.POST.get("task_title")
            domain = request.POST.get("domain")
            description = request.POST.get("description")
            priority = request.POST.get("priority")
            attached_file = request.FILES.get("attached_file")
            due_date = request.POST.get("due_date")
            status = request.POST.get("status")
            assigned_to = request.POST.get("assigned_to")
            assigned_by = request.POST.get("assigned_by")
            coordinator = (
                "coordinator" in request.POST
            )  # Checking if the checkbox is checked

            task = Task.objects.create(
                task_title=task_title,
                domain=domain,
                description=description,
                priority=priority,
                attached_file=attached_file,
                due_date=due_date,
                status=status,
                assigned_to=assigned_to,
                assigned_by=assigned_by,
                coordinator=coordinator,
            )

            if not settings.DEVELOPMENT:
                sendmail_create(task.id)
            else:
                print("\nEmails not sent in development mode\n")

            messages.success(request, "Task Created Successfully")
            return redirect("coretasks", domain_name=domain_name)
        else:
            messages.error(
                request, "You do not have permission to create task in this domain"
            )
            return redirect("corehome")


def sendmail_edit(taskid):
    task = Task.objects.filter(id=taskid).values()[0]

    task_title = task["task_title"]
    domain = task["domain"]
    description = task["description"]
    priority = task["priority"]
    due_date = task["due_date"]
    status = task["status"]
    assigned_to = task["assigned_to"]
    assigned_by = task["assigned_by"]
    coordinator = task["coordinator"]

    president_emails = CustomUser.objects.filter(president=True).values_list(
        "email", flat=True
    )
    vicepresident_emails = CustomUser.objects.filter(vice_president=True).values_list(
        "email", flat=True
    )

    domain_email_queries = {
        "technology": CustomUser.objects.filter(technology=True).values_list(
            "email", flat=True
        ),
        "events-cultural": CustomUser.objects.filter(events_cultural=True).values_list(
            "email", flat=True
        ),
        "events-sports": CustomUser.objects.filter(events_sports=True).values_list(
            "email", flat=True
        ),
        "legal": CustomUser.objects.filter(legal=True).values_list("email", flat=True),
        "operations": CustomUser.objects.filter(operations=True).values_list(
            "email", flat=True
        ),
        "marketing": CustomUser.objects.filter(marketing=True).values_list(
            "email", flat=True
        ),
        "sponsorship": CustomUser.objects.filter(sponsorship=True).values_list(
            "email", flat=True
        ),
        "design": CustomUser.objects.filter(design=True).values_list(
            "email", flat=True
        ),
        "finance": CustomUser.objects.filter(finance=True).values_list(
            "email", flat=True
        ),
        "media": CustomUser.objects.filter(media=True).values_list("email", flat=True),
        "security": CustomUser.objects.filter(security=True).values_list(
            "email", flat=True
        ),
        "hospitality": CustomUser.objects.filter(hospitality=True).values_list(
            "email", flat=True
        ),
    }

    domain_emails = domain_email_queries.get(domain, president_emails)

    emails_list = set(president_emails) | set(vicepresident_emails) | set(domain_emails)

    if coordinator:
        coordinator_emails = CustomUser.objects.filter(coordinator=True).values_list(
            "email", flat=True
        )
        emails_list |= set(coordinator_emails)

    emails_list = list(emails_list)

    subject = f"Shore25 Tasks: {task_title} edited"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("edittaskmail.html").render(
        {
            "task_title": task_title,
            "domain": domain,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "status": status,
            "assigned_to": assigned_to,
            "assigned_by": assigned_by,
        }
    )

    msg = EmailMultiAlternatives(subject, html_content, from_email, emails_list)
    msg.content_subtype = "html"
    msg.send()


@login_required(login_url="/auth/login/google-oauth2/")
def edit_task(request, domain_name, taskid):
    if not request.user.is_staff:
        return redirect("index")

    user_roles = {
        "coordinator": request.user.coordinator,
        "president": request.user.president,
        "vice_president": request.user.vice_president,
        "technology": request.user.technology,
        "events_cultural": request.user.events_cultural,
        "events_sports": request.user.events_sports,
        "legal": request.user.legal,
        "operations": request.user.operations,
        "marketing": request.user.marketing,
        "sponsorship": request.user.sponsorship,
        "design": request.user.design,
        "finance": request.user.finance,
        "media": request.user.media,
        "security": request.user.security,
        "hospitality": request.user.hospitality,
    }

    for role, has_role in user_roles.items():
        if has_role and (
            role == domain_name
            or domain_name == "alltasks"
            or domain_name == Task.objects.filter(id=taskid).values()[0]["domain"]
        ):
            if domain_name == "alltasks" and not request.user.president:
                return redirect("corehome")
            if request.method == "GET":
                taskdetails = Task.objects.filter(id=taskid).values()[0]
                return render(request, "edittask.html", {"task": taskdetails})
            elif request.method == "POST":
                now_attached_file = request.FILES.get("attached_file")
                task = Task.objects.get(id=taskid)

                if "del_file" in request.POST:
                    task.attached_file.delete()

                if now_attached_file:
                    task.attached_file.delete()  # Delete the old file
                    task.attached_file.save(
                        now_attached_file.name, now_attached_file, save=True
                    )

                task.task_title = request.POST.get("task_title")
                task.domain = request.POST.get("domain")
                task.description = request.POST.get("description")
                task.priority = request.POST.get("priority")
                task.due_date = request.POST.get("due_date")
                task.status = request.POST.get("status")
                task.assigned_to = request.POST.get("assigned_to")
                task.assigned_by = request.POST.get("assigned_by")
                task.coordinator = "coordinator" in request.POST
                task.save()

                if not settings.DEVELOPMENT:
                    sendmail_edit(taskid)
                else:
                    print("\nEmails not sent in development mode\n")

                return redirect("coretasks", domain_name=domain_name)
            else:
                return redirect("corehome")

    return redirect("corehome")

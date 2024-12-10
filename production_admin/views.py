import os
import subprocess
import pexpect
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from io import StringIO
from django.core.management.base import CommandError
from coreteam.models import CustomUser
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from concurrent.futures import ThreadPoolExecutor

from home.views import send_email_async

from prelims.models import Team, Participant, Event

from dotenv import load_dotenv

load_dotenv()

import random


def get_random_number():
    random_num = random.randint(1, 99999)
    return random_num


def index(request):
    if request.user.is_superuser:
        return render(request, "production_admin/index.html")
    else:
        return redirect("corehome")


def change_username(request):
    if request.user.is_superuser:
        users = CustomUser.objects.all()
        for user in users:
            num = get_random_number()
            user.username = f"{user.email}__{num}"
            user.save()

        return HttpResponse("Completed!!")
    else:
        return HttpResponse("Unauthorized!!")


def send_email_prebooking(email):
    user = CustomUser.objects.get(email=email)
    subject = "Shore'25 || Purchase your pass for SHORe'25"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("home/festpass_purchase_email.html").render(
        {
            "name": user.first_name.title(),
        }
    )

    msg = EmailMultiAlternatives(subject, html_content, from_email, [email])
    msg.content_subtype = "html"
    msg.send()


def add_campus_to_teams_prelims(request):
    if request.user.is_authenticated and request.user.is_superuser:
        teams = Team.objects.all()
        for team in teams:
            if not team.campus:
                team.campus = Participant.objects.get(email=team.captain_email).campus
                team.save()

        return HttpResponse("Completed")
    else:
        return redirect("home:dashboard")


def send_festpasspurchase_emails(request):
    """Send emails to prebooked students for purchasing the festpass"""
    if request.user.is_authenticated and request.user.is_superuser:
        prebooked_users = CustomUser.objects.filter(
            is_festpass_purchased=False, prebooking=True
        )
        emails = [user.email for user in prebooked_users]

        with ThreadPoolExecutor(max_workers=50) as executor:
            for email in emails:
                executor.submit(send_email_async, email, send_email_prebooking)

        return HttpResponse("Sent emails in background")
    else:
        return redirect("home:dashboard")


def remove_prebooking(request):
    if request.user.is_authenticated and request.user.is_superuser:
        prebooked_users = CustomUser.objects.filter(
            is_festpass_purchased=False, prebooking=True
        )
        for user in prebooked_users:
            user.prebooking = False
            user.save()

        return HttpResponse("Completed")
    else:
        return redirect("home:dashboard")


def git_pull(request):
    """Pull the latest changes from the main branch."""
    if settings.DEVELOPMENT:
        messages.success(
            request,
            "[DEVELOPMENT MODE] Git pull would show results here. "
            "This action is disabled in development environment."
        )
        return redirect("production_admin:index")

    try:
        git_pull_result = subprocess.run(
            ["git", "pull", "origin", "main"],
            check=True,
            capture_output=True,
            text=True,
        )
        messages.success(request, f"Git pull results: {git_pull_result.stdout}")
    except subprocess.CalledProcessError as e:
        messages.error(request, f"Error during git pull: {e.stderr}")

    return redirect("production_admin:index")


def restart_gunicorn(request):
    """Restart the Gunicorn server."""
    if settings.DEVELOPMENT:
        messages.success(
            request,
            "[DEVELOPMENT MODE] Gunicorn restart would show results here. "
            "This action is disabled in development environment."
        )
        return redirect("production_admin:index")

    server_password = os.getenv("SERVER_PASSWORD")
    restart_command = (
        f"echo {server_password} | sudo -S systemctl restart gunicorn.socket"
    )
    try:
        restart_result = subprocess.run(
            restart_command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        messages.success(request, "Gunicorn service restarted successfully")
    except subprocess.CalledProcessError as e:
        messages.error(request, f"Error restarting Gunicorn: {e.stderr}")
    except subprocess.TimeoutExpired:
        messages.error(request, "Timeout while trying to restart Gunicorn")

    return redirect("production_admin:index")


def pull_and_restart(request):
    if request.user.is_superuser:
        # Check if we're in development mode
        if settings.DEVELOPMENT:
            messages.success(
                request,
                "[DEVELOPMENT MODE] Git pull would show results here. "
                "This action is disabled in development environment.",
            )
            messages.success(
                request,
                "[DEVELOPMENT MODE] Gunicorn restart would show results here. "
                "This action is disabled in development environment.",
            )
            return redirect("production_admin:index")
        
        try:
            git_pull_result = subprocess.run(
                ["git", "pull", "origin", "main"],
                check=True,
                capture_output=True,
                text=True,
            )
            messages.success(request, f"Git pull results: {git_pull_result.stdout}")
        except subprocess.CalledProcessError as e:
            messages.error(request, f"Error during git pull: {e.stderr}")

        server_password = os.getenv("SERVER_PASSWORD")
        restart_command = (
            f"echo {server_password} | sudo -S systemctl restart gunicorn.socket"
        )
        try:
            restart_result = subprocess.run(
                restart_command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            messages.success(request, "Gunicorn service restarted successfully")
        except subprocess.CalledProcessError as e:
            messages.error(request, f"Error restarting Gunicorn: {e.stderr}")
        except subprocess.TimeoutExpired:
            messages.error(request, "Timeout while trying to restart Gunicorn")

    else:
        return redirect("corehome")


def migrate_database(request, app_name):
    if app_name == "all":
        app_name = None

    if request.user.is_superuser:
        if settings.DEVELOPMENT:
            messages.success(
                request,
                "[DEVELOPMENT MODE] Makemigrations would show results here. "
                "This action is disabled in development environment.",
            )
            return redirect("production_admin:index")

        try:
            # Get the project root directory (one level up from manage.py)
            project_root = Path(settings.BASE_DIR).parent
            venv_activate = project_root / "venv" / "bin" / "activate"

            # Prepare the command with cd and source activation
            command_prefix = f"cd {project_root} && source {venv_activate} && "

            # Prepare migration commands
            makemigrations_command = command_prefix + "python3 manage.py makemigrations"
            if app_name:
                makemigrations_command += f" {app_name}"

            migrate_command = command_prefix + "python3 manage.py migrate"
            if app_name:
                migrate_command += f" {app_name}"

            # Run makemigrations
            makemigrations_result = subprocess.run(
                makemigrations_command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
            )
            messages.success(
                request, f"Makemigrations results: {makemigrations_result.stdout}"
            )

            # Run migrate
            migrate_result = subprocess.run(
                migrate_command, shell=True, check=True, capture_output=True, text=True
            )
            messages.success(request, f"Migrate results: {migrate_result.stdout}")
            return redirect("production_admin:index")
        except subprocess.CalledProcessError as e:
            messages.error(request, f"Error during migration: {e.stderr}")
            return redirect("production_admin:index")
    else:
        return redirect("corehome")


def run_command(request):
    if not request.user.is_superuser:
        return redirect("corehome")

    if request.method != "POST":
        return redirect("production_admin:index")

    command = request.POST.get("command")
    args = request.POST.get("args", "").split()

    if settings.DEVELOPMENT:
        messages.success(
            request,
            f"[DEVELOPMENT MODE] Command '{command} {' '.join(args)}' would run here. "
            "This action is disabled in development environment.",
        )
        return redirect("production_admin:index")

    try:
        # Get the project root directory
        project_root = Path(settings.BASE_DIR).parent

        # Try different possible virtualenv paths
        possible_venv_paths = [
            project_root / "venv" / "bin" / "activate",  # Unix/Linux
            project_root / "venv" / "Scripts" / "activate",  # Windows
            project_root / ".venv" / "bin" / "activate",  # Alternative Unix/Linux
            project_root / "env" / "bin" / "activate",  # Another common name
        ]

        # Find the first existing virtualenv path
        venv_path = None
        for path in possible_venv_paths:
            if path.exists():
                venv_path = path
                break

        if venv_path:
            # Use the virtualenv if found
            full_command = f"cd {project_root} && source {venv_path} && python manage.py {command} {' '.join(args)}"
        else:
            # Fall back to system Python if no virtualenv found
            full_command = (
                f"cd {project_root} && python manage.py {command} {' '.join(args)}"
            )

        # Run the command
        result = subprocess.run(
            full_command, shell=True, check=True, capture_output=True, text=True
        )

        messages.success(request, f"Command output:\n{result.stdout}")
        if result.stderr:
            messages.warning(request, f"Command stderr:\n{result.stderr}")

    except subprocess.CalledProcessError as e:
        messages.error(request, f"Error running command: {e.stderr}")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")

    return redirect("production_admin:index")

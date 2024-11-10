import os
import subprocess
import pexpect
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from dotenv import load_dotenv
load_dotenv()

def index(request):
    if request.user.is_superuser:
        return render(request, "production_admin/index.html")
    else:
        return redirect("corehome")


def pull_and_restart(request):
    if request.user.is_superuser:
        # Check if we're in development mode
        if settings.DEVELOPMENT:
            messages.success(
                request, 
                "[DEVELOPMENT MODE] Git pull would show results here. "
                "This action is disabled in development environment."
            )
            messages.success(
                request, 
                "[DEVELOPMENT MODE] Gunicorn restart would show results here. "
                "This action is disabled in development environment."
            )
            return redirect("production_admin:index")
            
        try:
            # First do git pull
            git_pull_result = subprocess.run(
                ["git", "pull", "origin", "main"],
                check=True,
                capture_output=True,
                text=True,
            )
            messages.success(request, f"Git pull results: {git_pull_result.stdout}")

            # Try using echo to pipe the password to sudo
            server_password = os.getenv('SERVER_PASSWORD')
            restart_command = f"echo {server_password} | sudo -S systemctl restart gunicorn.socket"
            
            try:
                # Use shell=True because we're using pipe
                restart_result = subprocess.run(
                    restart_command,
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                messages.success(request, "Gunicorn service restarted successfully")
            except subprocess.CalledProcessError as e:
                messages.error(
                    request, f"Error restarting Gunicorn: {e.stderr}"
                )
            except subprocess.TimeoutExpired:
                messages.error(
                    request, "Timeout while trying to restart Gunicorn"
                )

            return redirect("production_admin:index")
            
        except subprocess.CalledProcessError as e:
            messages.error(
                request, f"Error during git pull: {e.stderr}"
            )
            return redirect("production_admin:index")
    else:
        return redirect("corehome")


def migrate_database(request, app_name):
    if app_name == 'all':
        app_name = None
    
    if request.user.is_superuser:
        if settings.DEVELOPMENT:
            messages.success(
                request, 
                "[DEVELOPMENT MODE] Makemigrations would show results here. "
                "This action is disabled in development environment."
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
                text=True
            )
            messages.success(
                request, f"Makemigrations results: {makemigrations_result.stdout}"
            )

            # Run migrate
            migrate_result = subprocess.run(
                migrate_command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            messages.success(request, f"Migrate results: {migrate_result.stdout}")
            return redirect("production_admin:index")
        except subprocess.CalledProcessError as e:
            messages.error(request, f"Error during migration: {e.stderr}")
            return redirect("production_admin:index")
    else:
        return redirect("corehome")

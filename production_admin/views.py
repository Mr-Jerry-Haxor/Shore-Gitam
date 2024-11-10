import subprocess
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings


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
            git_pull_result = subprocess.run(
                ["git", "pull", "origin", "main"],
                check=True,
                capture_output=True,
                text=True,
            )
            messages.success(request, f"Git pull results: {git_pull_result.stdout}")

            restart_gunicorn_result = subprocess.run(
                ["sudo", "systemctl", "restart", "gunicorn.socket"],
                check=True,
                capture_output=True,
                text=True,
            )
            messages.success(
                request, f"Gunicorn restart results: {restart_gunicorn_result.stdout}"
            )

            return redirect("production_admin:index")
        except subprocess.CalledProcessError as e:
            messages.error(
                request, f"Error during git pull or gunicorn restart: {e.stderr}"
            )
            return redirect("production_admin:index")


def migrate_database(request, app_name):
    if app_name == 'all':
        # Handle migration for all apps
        app_name = None  # or however you want to handle this case
    
    if request.user.is_superuser:
        # check if in development mode
        if settings.DEVELOPMENT:
            messages.success(
                request, 
                "[DEVELOPMENT MODE] Makemigrations would show results here. "
                "This action is disabled in development environment."
            )
            return redirect("production_admin:index")

        try:
            makemigrations_command = ["python", "manage.py", "makemigrations"]
            if app_name:
                makemigrations_command.append(app_name)
            makemigrations_result = subprocess.run(
                makemigrations_command, check=True, capture_output=True, text=True
            )
            messages.success(
                request, f"Makemigrations results: {makemigrations_result.stdout}"
            )
            migrate_command = ["python", "manage.py", "migrate"]
            if app_name:
                migrate_command.append(app_name)
            migrate_result = subprocess.run(
                migrate_command, check=True, capture_output=True, text=True
            )
            messages.success(request, f"Migrate results: {migrate_result.stdout}")
            return redirect("production_admin:index")
        except subprocess.CalledProcessError as e:
            messages.error(request, f"Error during migration: {e.stderr}")
            return redirect("production_admin:index")
    else:
        return redirect("corehome")

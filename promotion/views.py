from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import BGMIPlayer, Volunteer
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.contrib import messages
import re
from django.contrib.auth.decorators import login_required
from events.models import College, Event, Hackathon
from hospitality.models import HospitalityUser
from django.core.files.uploadedfile import InMemoryUploadedFile


@require_http_methods(["GET", "POST"])
def bgmi_player(request):
    if True:
        return render(
            request, "bgmiclose.html", {"titletext": "BGMI Registration Closed"}
        )
    if request.method == "GET":
        # Render the form template for GET requests
        return render(
            request, "bgmireg.html"
        )  # Replace 'player_registration.html' with your template file

    elif request.method == "POST":
        # Extract data from the submitted form
        try:
            name = request.POST.get("Name")
            userid = request.POST.get("userid")
            email = request.POST.get("email")
            regno = request.POST.get("regno")
            yearofstudy = request.POST.get("yearofstudy")
            campus = request.POST.get("campus")
            # Create a new BGMIPlayer object and save it to the database
            new_player = BGMIPlayer(
                name=name,
                userid=userid,
                email=email,
                regno=regno,
                yearofstudy=yearofstudy,
                campus=campus,
            )
            new_player.save()
            messages.success(request, "Registration successful")
        except IntegrityError as e:
            # Catch the specific IntegrityError for unique constraint failure
            messages.error(
                request, "Email already exists. Please use a different email"
            )
            return render(request, "bgmireg.html")

        # Return a success message as JSON response
        # return JsonResponse({'message': 'Player created successfully'}, status=201)
        return redirect("bgmireg")


# @login_required(login_url="/auth/login/google-oauth2/")
def volunteer_registration(request):
    if request.method == "POST":
        print(f"\n{request.POST}\n")
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone_number = request.POST.get("phone_number")
            regno = request.POST.get("regNo")
            gender = request.POST.get("gender")
            year_of_study = request.POST.get("year_of_study")
            branch = request.POST.get("branch")
            course = request.POST.get("course")
            is_hosteler = request.POST.get("hosteler") == "yes"
            previous_experience = request.POST.get("prev")
            tshirt_size = request.POST.get("tShirtSize")
            why_you_interested = request.POST.get("whyJoin")
            profile_pic = request.FILES.get("photo")

            if email != request.user.email:
                messages.error(request, "You can only register using your email.")
                return redirect("volunteer")

            # Validate email domain
            if not re.match(r".+@(?:gitam\.edu|gitam\.in)$", email):
                messages.error(
                    request, "Invalid email domain. Please use a Gitam email."
                )
                return redirect("volunteer")

            # Validate image file type and size
            if isinstance(profile_pic, InMemoryUploadedFile):
                valid_types = ["image/jpeg", "image/jpg", "image/png"]
                max_size = 2 * 1024 * 1024  # 2MB

                if profile_pic.size > max_size:
                    messages.error(request, "File size must be less than 2MB.")
                    return redirect("volunteer")

                if profile_pic.content_type not in valid_types:
                    messages.error(
                        request, "Please upload an image file (JPG, JPEG, PNG)."
                    )
                    return redirect("volunteer")

            # Save data to the Volunteer model
            volunteer = Volunteer(
                name=name,
                email=email,
                phone_number=phone_number,
                regno=regno,
                gender=gender,
                year_of_study=year_of_study,
                branch=branch,
                course=course,
                ishosteler=is_hosteler,
                previous_experience=previous_experience,
                why_you_interested=why_you_interested,
                tshirt_size=tshirt_size,
                profile_pic=profile_pic,
            )
            volunteer.save()  # Save the data to the database
            messages.success(request, "Successfully completed volunteer registration.")
            return render(request, "volunteer_success.html")
        except IntegrityError as e:
            print(e)
            messages.error(
                request, "Email already exists. Please use a different email"
            )
            return redirect("volunteer")
        except Exception as e:
            print(e)
            messages.error(request, e)
            return redirect("volunteer")
    else:
        return render(request, "volunteer_registration.html")


def noc(request):
    return redirect("hospitality:hospitalitynoc")

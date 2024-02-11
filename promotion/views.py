from django.shortcuts import render , redirect
from django.http import JsonResponse
from .models import BGMIPlayer , Volunteer
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.contrib import messages
import re
from django.contrib.auth.decorators import login_required
from events.models import College , Event , Hackathon
from hospitality.models import HospitalityUser

@require_http_methods(["GET", "POST"])
def bgmi_player(request):
    if True:
        return render(request,'bgmiclose.html',{"titletext":"BGMI Registration Closed"})
    if request.method == 'GET':
        # Render the form template for GET requests
        return render(request, 'bgmireg.html')  # Replace 'player_registration.html' with your template file

    elif request.method == 'POST':
        # Extract data from the submitted form
        try:
            name = request.POST.get('Name')
            userid = request.POST.get('userid')
            email = request.POST.get('email')
            regno = request.POST.get('regno')
            yearofstudy = request.POST.get('yearofstudy')
            campus = request.POST.get('campus')
            # Create a new BGMIPlayer object and save it to the database
            new_player = BGMIPlayer(
                name=name,
                userid=userid,
                email=email,
                regno=regno,
                yearofstudy=yearofstudy,
                campus=campus
            )
            new_player.save()
            messages.success(request, "Registration successful")
        except IntegrityError as e:
            # Catch the specific IntegrityError for unique constraint failure
            messages.error(request, "Email already exists. Please use a different email")
            return render(request, 'bgmireg.html')

        # Return a success message as JSON response
        # return JsonResponse({'message': 'Player created successfully'}, status=201)
        return redirect('bgmireg')
    

@login_required(login_url="/auth/login/google-oauth2/")
def volunteer_registration(request):
    # if True:
    #     return render(request,'bgmiclose.html',{"titletext":"Volunteer Registration Closed"})
    if request.method == 'POST':
        try:
            name = request.POST.get('name') 
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            regno = request.POST.get('regno')
            gender = request.POST.get('gender')
            year_of_study = request.POST.get('yearofstudy')
            branch = request.POST.get('branch')
            institute = request.POST.get('institute')
            department = request.POST.get('Department') 
            campus = request.POST.get('campus')  
            is_hosteler = request.POST.get('hosteler')
            previous_experience = request.POST.get('previousexp')
            availability = request.POST.get('availability')
            domain_of_interest = request.POST.get('domain')
            tshirt_size = request.POST.get('tshirt')
            why_you_interested = request.POST.get('why_you_interested') 
            profile_pic = request.FILES.get('file_input') 
            
            if not re.match(r'.+@(?:gitam\.edu|gitam\.in)$', email):
                messages.error(request, "Invalid email domain. Please use a Gitam email.")
                return redirect('volunteer')
            
            # Save data to the Volunteer model
            volunteer = Volunteer(
                name=name,
                email=email,
                phone_number=phone_number,
                regno=regno,
                gender=gender,
                year_of_study=year_of_study,
                branch=branch,
                institute=institute,
                department=department,
                Campus=campus,
                ishosteler=is_hosteler,
                previous_experience=previous_experience,
                availability=availability,
                why_you_interested=why_you_interested,
                tshirt_size=tshirt_size,
                domain_of_interest=domain_of_interest,
                profile_pic=profile_pic
            )
            volunteer.save()  # Save the data to the database
            messages.success(request, "Registration successful")
            return redirect('volunteer')
        except IntegrityError as e:
            # Catch the specific IntegrityError for unique constraint failure
            messages.error(request, "Email already exists. Please use a different email")
            return render(request, 'voulnteerreg.html')
    else:
        return render(request, 'voulnteerreg.html')


def noc(request):
    return redirect("hospitality:hospitalitynoc")


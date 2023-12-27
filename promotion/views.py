from django.shortcuts import render , redirect
from django.http import JsonResponse
from .models import BGMIPlayer
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from django.contrib import messages

@require_http_methods(["GET", "POST"])
def bgmi_player(request):
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

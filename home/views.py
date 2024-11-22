import hashlib
import random
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from coreteam.models import CustomUser
from payments.models import FestPass


def generate_md5(user_string):
    hashed_string = hashlib.md5(user_string.encode("UTF-8"))
    return hashed_string.hexdigest()


def random_value():
    return random.randint(10000, 99999)


def homepage(request):
    return render(request, 'home/homepage.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home:dashboard')
    else:
        if request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home:dashboard')
            else:
                messages.error(request, "Wrong login credentials")
                return redirect('home:login')

        return render(request, 'home/login.html')


@login_required(login_url="home:login")
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect('home:login')
    else:
        messages.error(request, "You are not logged in")
        return redirect('home:login')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home:dashboard')
    if request.POST:
        # email, phone number, first name, last name, age, gender, college, year of study, course, branch, password
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        college = request.POST.get('college')
        year_of_study = request.POST.get('yearOfStudy')
        course = request.POST.get('course')
        branch = request.POST.get('branch')
        registration_number = request.POST.get('collegeRegNo')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # validate phone number, it should be 10 digits and should start with 6, 7, 8 or 9
        if len(phone_number) != 10 or phone_number[0] not in ['6', '7', '8', '9']:
            messages.error(request, "Invalid phone number")
            return redirect('home:signup')
        
        # validate email, it should be a valid email, also check if it contains '@gitam.in' or '@gitam.edu', if yes then ask them to login with the google account
        if '@gitam.in' in email or '@gitam.edu' in email:
            messages.error(request, "GITAM Student should use Google Sign In")
            return redirect('home:signup')
        
        if '@' not in email or '.' not in email:
            messages.error(request, "Invalid email")
            return redirect('home:signup')
        
        # validate age, it should be a number and should be greater than 18
        if not age.isdigit() or int(age) < 18:
            messages.error(request, "Invalid age")
            return redirect('home:signup')
        
        # validate password, it should be atleast 8 characters long, contain atleast 1 uppercase, 1 lowercase, 1 digit and 1 special character
        if len(password) < 8:
            messages.error(request, "Password should be atleast 8 characters long")
            return redirect('home:signup')
        
        if not any(char.isupper() for char in password):
            messages.error(request, "Password should contain atleast 1 uppercase character")
            return redirect('home:signup')
        
        if not any(char.islower() for char in password):
            messages.error(request, "Password should contain atleast 1 lowercase character")
            return redirect('home:signup')
        
        if not any(char.isdigit() for char in password):
            messages.error(request, "Password should contain atleast 1 digit")
            return redirect('home:signup')
        
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in password):
            messages.error(request, "Password should contain atleast 1 special character")
            return redirect('home:signup')
        
        # validate confirm password, it should match with the password
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('home:signup')
        
        # Check for empty fields
        if not all([email, phone_number, first_name, last_name, age, gender, college, year_of_study, course, branch, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect('home:signup')
        
        # Check if the user already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "User already exists")
            return redirect('home:signup')
        
        # Create a new user
        username = f"{first_name}__{last_name}__{registration_number}__{email}"
        profile_picture = request.FILES.get('profilePic')
        user = CustomUser.objects.create_user(
            username=username,
            email=email, 
            phone_number=phone_number, 
            registration_number=registration_number,
            first_name=first_name, 
            last_name=last_name,
            age=age,
            gender=gender,
            college=college,
            year_of_study=year_of_study,
            course=course,
            branch=branch,
            password=password,
            profile_picture=profile_picture,
            is_gitamite=False
        )
        user.save()
        messages.success(request, "User registered successfully")

        return redirect('home:login')

    return render(request, 'home/signup.html')


@login_required(login_url="home:login")
def festpass(request):
    if request.user.is_authenticated:
        # redirecting non gitamite users to dashboard
        if not request.user.is_gitamite:
            return redirect("home:dashboard")
        

        if request.user.is_festpass_purchased:
            return redirect('home:eticket')
        if request.GET:
            if request.user.is_festpass_purchased:
                return redirect('home:eticket')        
            else:
                return render(request, 'home/festpass.html')
        elif request.POST:
            user = CustomUser.objects.get(email=request.user.email)

            reg_num = request.POST.get('registrationNumber')
            phone_number = request.POST.get('phone')
            branch = request.POST.get('branch')
            gender = request.POST.get('gender')
            year_of_study = request.POST.get('yearOfStudy')
            if 'campus' in request.POST:
                campus = request.POST.get('campus')
            course = request.POST.get('course')
            profile_picture = request.FILES.get('profilePic')
            sports_participation = request.POST.get('participatingInSports')
            accomdation = request.POST.get('needAccommodation')

            # validate phone number, it should be 10 digits and should start with 6, 7, 8 or 9
            if len(phone_number) != 10 or phone_number[0] not in ['6', '7', '8', '9']:
                messages.error(request, "Invalid phone number")
                return redirect('home:festpass')

            # Check for empty fields
            if not all([reg_num, phone_number, branch, gender, year_of_study]):
                messages.error(request, "All fields are required.")
                return redirect('home:festpass')  # Redirect back to the festpass page
            
            user.registration_number = reg_num
            user.phone_number = phone_number
            user.branch = branch
            user.gender = gender
            user.year_of_study = year_of_study
            if 'campus' in request.POST:
                user.campus = campus
            user.course = course
            user.sports = sports_participation == 'yes'
            user.accomdation = accomdation == 'yes'
            
            # Save user data first
            user.save()

            # Save profile picture if it exists
            if profile_picture:
                user.profile_picture = profile_picture
                user.save()

            # if the user does not have a profile picture then show an error message
            if not user.profile_picture:
                messages.error(request, 'Please upload a profile picture to continue.')
                return redirect('home:festpass')


            """Check whether any of the important field is empty (first_name, last_name, email, registration_number, phone_number, college, branch, course, year_of_study, campus(for is_gitamite=True))"""
            important_fields = [user.first_name, user.last_name, user.email, user.registration_number, 
                                user.phone_number, user.college, user.branch, user.course, 
                                user.year_of_study, user.campus if user.is_gitamite else 'non gitamite']
            
            for field in important_fields:
                if field is None or field == '':
                    messages.error(request, f'{field} is empty.')

                    return redirect('home:festpass')

            # generate a passhash
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            hashtext = str(user.email) + str(user.registration_number) + str(timestamp) + str(random_value())
            hash_md5 = generate_md5(hashtext)

            user.passhash = hash_md5
            user.save()

            """After saving the user data successfully, redirect to their respective payment portals"""
            if user.is_gitamite:
                return redirect("https://gevents.gitam.edu/registration/MjkzMg")
            elif not user.is_gitamite and sports_participation == 'no':
                return HttpResponse("Non GITAM Student's festpass gevent page")
            elif not user.is_gitamite and sports_participation == 'yes':
                return HttpResponse("Non GITAM Student's festpass + sports gevent page")

        return render(request, 'home/festpass.html')
    return redirect('home:login')


@login_required(login_url="home:login")
def eticket(request):
    """Need to modify!!!"""
    # check if is_festpass_purchased is true and also verify the related transaction is success
    if request.user.is_authenticated:
        # if request.user.is_festpass_purchased and FestPass.objects.filter(email=request.user.email).exists():  # also check if the related transaction is success or not in the payments table
        if request.user.is_festpass_purchased:
            return render(request, 'home/eticket.html')
        else:
            messages.error(request, 'Please purchase the festpass to get your eticket.')
            return redirect('home:dashboard')

    return redirect('home:login')


@login_required(login_url="/auth/login/google-oauth2/")
def dashboard(request):
    if request.user.is_authenticated:
        context = {}
        # if request.user.is_festpass_purchased and FestPass.objects.filter(email=request.user.email).exists():
        if request.user.is_festpass_purchased:
            context['festpass_validated'] = True
            return render(request, 'home/dashboard.html', context)
        return render(request, 'home/dashboard.html')
    
    return redirect('home:login')

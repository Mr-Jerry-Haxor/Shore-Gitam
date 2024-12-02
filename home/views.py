import hashlib
import threading
import requests
import json
import random
from datetime import datetime
import os


from concurrent.futures import ThreadPoolExecutor
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.db.models import Count , Max
from coreteam.models import CustomUser
from payments.models import FestPass
from production_admin.models import PassStatus
from .models import *


class EmailThread(threading.Thread):
    """
    Custom thread class for sending emails.
    Takes a different email sending function as argument.
    """
    def __init__(self, user_email, send_mail_function):
        threading.Thread.__init__(self)
        self.user_email = user_email
        self.send_mail_function = send_mail_function

    def run(self):
        """
        This method is called when the thread starts.
        """
        try:
            self.send_mail_function(self.user_email)
        except Exception as e:
            print(f"Failed to send email to {self.user_email}: {e}")


def send_email_async(user_email, send_mail_function):
    """
    Function to send an email asynchronously using a thread.
    Accepts a send mail function as argument.
    """
    email_thread = EmailThread(user_email, send_mail_function)

    # Start the thread
    email_thread.start()

    # Clean up (optional; threads clean themselves up upon completion)
    return email_thread


def send_prebooking_email(user_email):
    user = CustomUser.objects.get(email=user_email)

    subject = "Success! Pre-Booking Confirmed for SHORe'25"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("home/prebooking_email.html").render({
        "name": user.first_name,
        "email": user.email,
        "reg_num": user.registration_number
    })

    msg = EmailMultiAlternatives(subject, html_content, from_email, [user_email])
    msg.content_subtype = "html"
    msg.send()


def send_festpass_email(user_email):
    user = CustomUser.objects.get(email=user_email)

    subject = "Success! Festpass Confirmed for SHORe'25"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("home/festpass_email.html").render({
        "user": user
    })

    msg = EmailMultiAlternatives(subject, html_content, from_email, [user_email])
    msg.content_subtype = "html"
    msg.send()


def send_payment_failed_email(user_email):
    user = CustomUser.objects.get(email=user_email)

    subject = "Payment Failed! Payment for SHORe'25 festpass failed"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("home/payment_issue.html").render({
        "user": user,
        "payment": FestPass.objects.filter(email=user_email).order_by('-updated_date').first()
    })

    msg = EmailMultiAlternatives(subject, html_content, from_email, [user_email])
    msg.content_subtype = "html"
    msg.send()


def send_payment_pending_email(user_email):
    user = CustomUser.objects.get(email=user_email)

    subject = "Payment Pending! Payment for SHORe'25 festpass is pending"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("home/payment_pending.html").render({
        "user": user,
        "payment": FestPass.objects.filter(email=user_email).order_by('-updated_date').first()
    })

    msg = EmailMultiAlternatives(subject, html_content, from_email, [user_email])
    msg.content_subtype = "html"
    msg.send()


def is_transaction_success(user_email):
    if FestPass.objects.filter(email=user_email).exists():
        user_transactions = FestPass.objects.filter(email=user_email)
        y_count = user_transactions.filter(transaction_status="Y").count()
        if y_count > 0:
            return True
        else:
            return False
    else:
        return False
        


def is_transaction_failed(user_email):
    if FestPass.objects.filter(email=user_email).exists():
        user_transactions = FestPass.objects.filter(email=user_email)
        y_count = user_transactions.filter(transaction_status="Y").count()
        if y_count == 0:
            return True
        else:
            return False
    else:
        return False



def is_transaction_pending(user_email):
    if FestPass.objects.filter(email=user_email).exists():
        user_transactions = FestPass.objects.filter(email=user_email)
        y_count = user_transactions.filter(transaction_status="Y").count()
        p_count = user_transactions.filter(transaction_status="P").count()
        if y_count == 0 and p_count > 0:
            return True
        else:
            return False
    else:
        return False



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
    # removing signup temporarily, need to enable once festpasses for non gitam students are enabled
    messages.info(request, "Please use Sign in with Google")
    return redirect("home:login")

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
        context = {}

        # redirecting non gitamite users to dashboard
        if not request.user.is_gitamite:
            return redirect("home:dashboard")
        
        """Checking for prebooking"""
        context['prebooking'] = False

        if prebooking and request.user.prebooking:
            return redirect('home:prebooking')

        if request.user.is_festpass_purchased:
            return redirect('home:eticket')

        if request.GET:
            if request.user.is_festpass_purchased:
                return redirect('home:eticket')        
            else:
                if is_transaction_success(request.user.email):
                    request.user.is_festpass_purchased = True
                    request.user.save()
                    send_email_async(request.user.email, send_festpass_email)
                    return redirect('home:eticket')
                
                data = {
                    "email": str(request.user.email)
                }

                try:
                    response = requests.post(
                        "https://gevents.gitam.edu/registration/data/checkmail",
                        data=data,
                    )

                    if response.status_code == 200:
                        student_data = json.loads(response.text)
                        context['student_data'] = student_data
                        if student_data["status"] == "success":
                            return render(request, 'home/festpass.html', context)
                        else:
                            return render(request, 'home/festpass.html', context)
                    else:
                        return render(request, 'home/festpass.html', context)
                except:
                    return render(request, 'home/festpass.html', context)

        elif request.POST:
            """Check whether user has accepted all terms and conditions or not"""
            if (
                "terms1" not in request.POST or
                "terms2" not in request.POST or
                "terms3" not in request.POST
            ):
                messages.error(request, "Please accept all the terms and conditions to purchase festpass")
                return redirect("home:festpass")

            user = CustomUser.objects.get(email=request.user.email)

            name = request.POST.get('visible_name')
            reg_num = request.POST.get('registrationNumber')
            phone_number = request.POST.get('phone')
            branch = request.POST.get('branch')
            gender = request.POST.get('gender')
            year_of_study = request.POST.get('yearOfStudy')
            if 'campus' in request.POST:
                campus = request.POST.get('campus')
            course = request.POST.get('course')
            profile_picture = request.FILES.get('profilePic')

            # Validate the file extension
            if profile_picture:
                valid_extensions = ['.jpg', '.jpeg', '.png']
                extension = os.path.splitext(profile_picture.name)[1].lower()
                if extension not in valid_extensions:
                    messages.error(request, "Invalid file type. Only JPG, JPEG, and PNG files are allowed.")
                    return redirect('home:festpass')

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
            
            user.name = name
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
                                user.phone_number, user.branch, user.course, 
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

            """Check if prebooking is enabled, and if yes then jus mark prebooking as true and redirect to prebooking success page"""
            if prebooking:
                user.prebooking = True
                user.save()

                # send prebooking email
                send_email_async(request.user.email, send_prebooking_email)

                return redirect("home:prebooking")

            """After saving the user data successfully, redirect to their respective payment portals"""
            if user.is_gitamite:
                return redirect(f"https://gevents.gitam.edu/registration/MjkzMg..?rid={user.registration_number}&type=student")
            elif not user.is_gitamite and sports_participation == 'no':
                return HttpResponse("Non GITAM Student's festpass gevent page")
            elif not user.is_gitamite and sports_participation == 'yes':
                return HttpResponse("Non GITAM Student's festpass + sports gevent page")

        return render(request, 'home/festpass.html', context)
    return redirect('home:login')


@login_required(login_url="home:login")
def eticket(request):
    """Need to modify!!!"""
    # check if is_festpass_purchased is true and also verify the related transaction is success
    if request.user.is_authenticated:
        # if request.user.is_festpass_purchased and FestPass.objects.filter(email=request.user.email).exists():  # also check if the related transaction is success or not in the payments table
        if request.user.is_festpass_purchased:
            if FestPass.objects.filter(email=request.user.email).exists():
                user_transactions = FestPass.objects.filter(email=request.user.email)
                y_count = user_transactions.filter(transaction_status="Y").count()
                if y_count == 0:
                    user = CustomUser.objects.get(email=request.user.email)
                    user.is_festpass_purchased = False
                    user.save()
                    return redirect('home:dashboard')
                elif y_count > 0:
                    return render(request, 'home/eticket.html', context={'user': request.user})
            else:
                messages.error(request, 'Please purchase the festpass to get your eticket.')
                return redirect('home:dashboard')
            return render(request, 'home/eticket.html')
        else:
            if FestPass.objects.filter(email=request.user.email).exists():
                user_transactions = FestPass.objects.filter(email=request.user.email)
                y_count = user_transactions.filter(transaction_status="Y").count()
                if y_count > 0:
                    user = CustomUser.objects.get(email=request.user.email)
                    user.is_festpass_purchased = True
                    user.save()
                    send_email_async(request.user.email, send_festpass_email)
                    return render(request, 'home/eticket.html')
            else:
                messages.error(request, 'Please purchase the festpass to get your eticket.')
                return redirect('home:dashboard')

    return redirect('home:login')


@login_required(login_url="/auth/login/google-oauth2/")
def dashboard(request):
    if request.user.is_authenticated:
        context = {}

        """Checking for prebooking"""
        try:
            prebooking = PassStatus.objects.get(id=1).pre_booking
        except Exception as e:
            # prebooking = PassStatus.objects.get(id=2).pre_booking
            print(e)
        context['prebooking'] = False
         

        # check if hashpass is created and not request.user.is_festpass_purchased is false and transaction is success in payments table
        if request.user.passhash and not request.user.is_festpass_purchased and is_transaction_success(request.user.email):
            # make is_festpass_purchased to True
            user = CustomUser.objects.get(email=request.user.email)
            user.is_festpass_purchased = True
            user.save()
            # send festpass email
            send_email_async(request.user.email, send_festpass_email)
            context['festpass_validated'] = True
        elif is_transaction_failed(request.user.email):
            transactions = FestPass.objects.filter(email=request.user.email).values('txn_id').annotate(
                count=Count('txn_id'),
                posted_date=Max('posted_date'),
                transaction_status=Max('transaction_status')
            )
            # transactions = FestPass.objects.filter(email=request.user.email)
            context['transactions'] = transactions
            
        
        elif is_transaction_pending(request.user.email):
            transactions = FestPass.objects.filter(email=request.user.email)
            context['transactions'] = transactions
            

        fields_to_check = [
            'event_manager', 'campus_head_hyd', 'campus_head_blr', 'coordinator', 
            'president', 'vice_president', 'technology', 'events_cultural', 
            'events_sports', 'legal', 'operations', 'marketing', 'sponsorship', 
            'design', 'finance', 'media', 'security', 'hospitality', 'advisory', 
            'hospitality_staff', 'events_cultural_staff', 'events_sports_staff', 
            'security_staff', 'isLead'
        ]

        if request.user.is_superuser or any(getattr(request.user, field, False) for field in fields_to_check):
            context['isCoreMember'] = True
        else:
            context['isCoreMember'] = False

        if request.user.is_festpass_purchased and is_transaction_success(request.user.email):
            context['festpass_validated'] = True
            
        total_tickets_sold = FestPass.objects.filter(transaction_status="Y").count() #.values('email').annotate(count=Count('email')).order_by('-count')

        total_unique_tickets = FestPass.objects.filter(
            txn_id__isnull = False,
            transaction_status = "Y"
        ).values("txn_id").distinct().count()

        context['total_tickets_sold'] = total_unique_tickets
            
        return render(request, 'home/dashboard.html', context)
    
    else:
        return redirect('home:login')


@login_required(login_url="home:login")
def prebooking(request):
    if request.user.is_authenticated:
        if request.user.prebooking:
            return render(request, "home/prebooking_success.html")
        else:
            messages.error(request, "Please fill in your details")
            return redirect("home:festpass")
    
    return redirect('home:login')


def send_name_email(emails):
    subject = "Important! Please update your name!"
    from_email = settings.EMAIL_HOST_USER
    html_content = get_template("home/update_name_email.html").render({
        "update_name_url": ""
    })

    msg = EmailMultiAlternatives(subject, html_content, from_email, emails)
    msg.content_subtype = "html"
    msg.send()


@login_required(login_url="home:login")
def send_student_emails(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users = CustomUser.objects.filter(name__isnull=True, is_festpass_purchased=True)
        emails = [user.email for user in users]

        with ThreadPoolExecutor(max_workers=50) as executor:
            for email in emails:
                executor.submit(send_email_async, email, send_name_email)

        return HttpResponse("Sent emails in the background")
    
    return redirect("home:dashboard")


@login_required(login_url="/auth/login/google-oauth2/")
def update_name(request):
    if request.user.is_authenticated:
        user_obj = CustomUser.objects.get(email=request.user.email)
        if user_obj.name:
            messages.info(request, "Name already exists, no need to update your name.")
            return redirect("home:dashboard")
        if request.POST:
            name = request.POST.get('name')
            user_obj.name = name
            user_obj.save()

            messages.success(request, "Successfully updated your name")
            return redirect("home:dashboard")
        return render(request, "home/update_name.html")
    else:
        return redirect("home:login")

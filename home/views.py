from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required, login_url="index")
def homepage(request):
    return render(request, 'home/homepage.html')

@user_passes_test(superuser_required, login_url="index")
def login(request):
    return render(request, 'home/login.html')

@user_passes_test(superuser_required, login_url="index")
def signup(request):
    return render(request, 'home/signup.html')

@user_passes_test(superuser_required, login_url="index")
def festpass(request):
    return render(request, 'home/festpass.html')

from django.shortcuts import render, HttpResponse , redirect 
from django.contrib.auth.decorators import login_required




@login_required(login_url="/auth/login/google-oauth2/")
def coreindex(request):
    if request.user.is_staff:
        return render(request , 'dashboard.html')
    elif not request.user.is_authenticated:
        return redirect('index')


@login_required(login_url="/auth/login/google-oauth2/")
def home(request):
    print(request.user.media)
    return render(request, 'coreindex.html')
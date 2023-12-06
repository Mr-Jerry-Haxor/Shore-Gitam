from django.shortcuts import render, HttpResponse

# Create your views here.

def coreindex(request):
    return render(request, 'coreindex.html')


def home(request):
    return HttpResponse("Welcome home")
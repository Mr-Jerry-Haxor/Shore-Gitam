from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "shore23.html")


def sponsors(request):
    return render(request, "sponsors.html")

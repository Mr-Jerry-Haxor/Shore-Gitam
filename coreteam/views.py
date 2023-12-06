from django.shortcuts import render

# Create your views here.

def coreindex(request):
    return render(request, 'coreindex.html')
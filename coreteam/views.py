from django.shortcuts import render, HttpResponse , redirect

# Create your views here.

def coreindex(request):
    if not request.user.is_authenticated:
        return render(request, 'coreindex.html')
    elif request.user.is_staff:
        return HttpResponse("Staff member")
    else:
        return redirect('index')


def home(request):
    return HttpResponse("Welcome home")
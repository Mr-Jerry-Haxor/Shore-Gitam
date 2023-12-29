from django.shortcuts import render , HttpResponse

# Create your views here.


def test(request):
    # return render(request, 'countdown.html')
    return render(request, 'SHORE24_home.html')

def index(request):
    return render(request, 'SHORE24_home.html')
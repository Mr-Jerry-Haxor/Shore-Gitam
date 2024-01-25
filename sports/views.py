from django.shortcuts import render
from .models import Sport


def matches(request):
    context = {}
    context['sports'] = Sport.objects.all()
    return render(request, 'sports/matches.html', context)

def points(request):
    context = {}
    context['sports'] = Sport.objects.all()
    return render(request, 'sports/points.html', context)
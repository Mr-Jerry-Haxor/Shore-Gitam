from django.shortcuts import render
from .models import Sport


def matches(request):
    context = {"type": "Matches"}
    context['sports'] = Sport.objects.all()
    return render(request, 'sports/matches.html', context)


def points(request):
    context = {"type": "Points"}
    context['sports'] = Sport.objects.all()
    return render(request, 'sports/matches.html', context)
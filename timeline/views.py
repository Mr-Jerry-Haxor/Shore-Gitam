from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

from .models import Timeline

def index(request):
    return redirect('timeline:timeline', day_no=1)


def timeline(request, day_no):
    context = {}
    context['selected_day'] = int(day_no)

    timeline = Timeline.objects.filter(day=day_no).order_by('start_time')

    if not timeline.exists():
        messages.info(request, f'No events on Day {day_no}')
        return render(request, 'timeline/timeline.html', context)

    distinct_days = Timeline.objects.values_list('day', flat=True).distinct()
    event_types = Timeline.objects.filter(day=day_no).values_list(
        'event_type', flat=True).distinct()

    event_order = ['Culturals', 'Sports', 'Minor']
    sorted_order = []
    for x in event_order:
        if x in event_types:
            sorted_order.append(x)
    print(sorted_order)

    context['event_types'] = sorted_order
    context['timeline'] = timeline
    context['days'] = distinct_days

    return render(request, 'timeline/timeline.html', context)

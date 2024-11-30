from django import template
from prelims.models import Event, Team, Participant
from coreteam.models import CustomUser

register = template.Library()


def get_teammates_object(team):
    try:
        return CustomUser.objects.get(email=email.strip())
    except CustomUser.DoesNotExist:
        return None

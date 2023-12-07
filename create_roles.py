# Define your role names
ROLES = [
    'president',
    'vice-president',
    'technology',
    'events-cultural',
    'events-sports',
    'legal',
    'operations',
    'marketing',
    'sponsorship',
    'design',
    'finance',
    'media',
    'security',
    'hospitality',
]


from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create groups
        for role in ROLES:
            group, created = Group.objects.get_or_create(name=role)

        # Assign permissions to groups
        for role in ROLES:
            group = Group.objects.get(name=role)
            permissions = Permission.objects.filter(
                content_type__in=ContentType.objects.filter(app_label='shore')
            )
            group.permissions.set(permissions)

# timeline/management/commands/import_timeline_data.py
from django.core.management.base import BaseCommand
from timeline.models import Timeline, Timeline1, Day

class Command(BaseCommand):
    help = 'Import data from Timeline to Timeline1 model'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data import...'))

        # Your data migration logic here
        # Example: Copy data from Timeline to Timeline1
        for old_timeline in Timeline.objects.all():
            new_timeline = Timeline1(
                name=old_timeline.name,
                description=old_timeline.description,
                event_location=old_timeline.event_location,
                event_type=old_timeline.event_type,
                venue=old_timeline.venue,
                date=old_timeline.date,
                start_time=old_timeline.start_time,
                end_time=old_timeline.end_time
            )
            new_timeline.save()

            # Assuming you have a M2M relation with Day, and it's named 'day'
            new_timeline.day.set(old_timeline.day.all())

        self.stdout.write(self.style.SUCCESS('Data import completed successfully.'))

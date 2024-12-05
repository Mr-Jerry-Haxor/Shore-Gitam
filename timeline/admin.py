from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Timeline


class TimelineAdmin(ImportExportModelAdmin):
    list_display = (
        "day",
        "name",
        "event_type",
        "venue",
        "date",
        "start_time",
        "end_time",
    )
    list_filter = ("day", "event_type")
    search_fields = ["name", "description", "venue"]

    def formatted_event_date(self, obj):
        return obj.formatted_event_date()

    def formatted_start_time(self, obj):
        return obj.formatted_start_time()

    def formatted_end_time(self, obj):
        return obj.formatted_end_time()

    def formatted_start_time_12hr(self, obj):
        return obj.formatted_start_time_12hr()

    def formatted_end_time_12hr(self, obj):
        return obj.formatted_end_time_12hr()

    formatted_event_date.short_description = "Event Date"
    formatted_start_time.short_description = "Start Time (24hr)"
    formatted_end_time.short_description = "End Time (24hr)"
    formatted_start_time_12hr.short_description = "Start Time (12hr)"
    formatted_end_time_12hr.short_description = "End Time (12hr)"


admin.site.register(Timeline, TimelineAdmin)

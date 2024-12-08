from django.contrib import admin
from .models import Event, Team, Participant
from import_export.admin import ImportExportModelAdmin


@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):
    list_display = ("name", "event_type", "date", "time", "venue")


@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    list_display = ("visible_name", "event", "captain_email", "registered_at")
    search_fields = ("visible_name", "captain_email", "event__name")
    list_filter = ("event", "registered_at")
    ordering = ("-registered_at",)

@admin.register(Participant)
class ParticipantAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "email",
        "phone_number",
        "registration_number",
        "campus",
        "event",
        "team",
        "isCaptain",
        "registered_at",
    )
    search_fields = ("name", "email", "registration_number", "event__name", "team__visible_name")
    list_filter = ("event", "campus", "isCaptain", "registered_at")
    ordering = ("-registered_at",)

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    College,
    Event,
    Team,
    Participants,
    Hackathon,
    HackathonTeam,
    HackathonParticipants,
)
from import_export.admin import ImportExportModelAdmin


@admin.register(College)
class CollegeAdmin(ImportExportModelAdmin):
    list_display = ("college_id", "name", "abbreviation", "passkey", "tosend", "emails")


@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):
    list_display = (
        "event_id",
        "name",
        "description",
        "event_type",
        "guidelines_url",
        "image",
        "event_time",
        "event_start_date",
        "event_end_date",
        "created_at",
        "no_of_teams",
        "max_univeristy_teams",
        "min_team_size",
        "max_team_size",
    )
    list_filter = ('event_type', 'event_start_date', 'event_end_date')


@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    list_display = (
        "team_id",
        "team_name",
        "visible_name",
        "college",
        "sport",
        "isPaid",
        "isWaiting",
        "registered_at",
        "status",
    )
    list_filter = ('sport', 'isPaid', 'isWaiting', 'status')


@admin.register(Participants)
class ParticipantsAdmin(ImportExportModelAdmin):
    list_display = (
        "participant_id",
        "name",
        "email",
        "phone_number",
        "accomdation",
        "college",
        "sport",
        "team",
        "isCaptain",
        "isPaid",
        "isGitamite",
        "shoreid",
    )
    list_filter = ('sport', 'isPaid', 'isCaptain', 'isGitamite', 'accomdation')


class HackathonAdmin(ImportExportModelAdmin):
    list_display = ["name", "event_type", "min_team_size", "max_team_size"]
    search_fields = ["name", "event_type"]
    list_filter = ('event_type',)


class HackathonTeamAdmin(ImportExportModelAdmin):
    list_display = [
        "team_name",
        "visible_name",
        "college",
        "hackathon",
        "isPaid",
        "isQualified",
        "registered_at",
    ]
    search_fields = ["team_name", "visible_name", "college__name", "hackathon__name"]
    list_filter = ('hackathon', 'isPaid', 'isQualified')


class HackathonParticipantsAdmin(ImportExportModelAdmin):
    list_display = [
        "name",
        "email",
        "phone_number",
        "accomdation",
        "college",
        "hackathon",
        "team",
        "isCaptain",
        "isPaid",
        "isGitamite",
        "shoreid",
    ]
    search_fields = [
        "name",
        "email",
        "phone_number",
        "college__name",
        "hackathon__name",
        "team__team_name",
    ]
    list_filter = ('hackathon', 'isPaid', 'isCaptain', 'isGitamite', 'accomdation')


admin.site.register(Hackathon, HackathonAdmin)
admin.site.register(HackathonTeam, HackathonTeamAdmin)
admin.site.register(HackathonParticipants, HackathonParticipantsAdmin)

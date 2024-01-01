from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import College, Event, Team, Participants, Hackathon, HackathonTeam, HackathonParticipants
from import_export.admin import ImportExportModelAdmin


@admin.register(College)
class CollegeAdmin(ImportExportModelAdmin):
    list_display = ('college_id', 'name', 'abbreviation', 'passkey')

@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):
    list_display = ('event_id', 'name', 'event_type', 'no_of_teams', 'max_univeristy_teams')

@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    list_display = ('team_id', 'team_name', 'visible_name', 'college', 'sport', 'isPaid', 'isWaiting', 'registered_at', 'status')

@admin.register(Participants)
class ParticipantsAdmin(ImportExportModelAdmin):
    list_display = ('participant_id', 'name', 'email', 'phone_number', 'accomdation', 'college', 'sport', 'team', 'isCaptain', 'isPaid', 'isGitamite', 'transaction_id')

admin.site.register(Hackathon)
admin.site.register(HackathonTeam)
admin.site.register(HackathonParticipants)
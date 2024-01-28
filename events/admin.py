from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import College, Event, Team, Participants, Hackathon, HackathonTeam, HackathonParticipants
from import_export.admin import ImportExportModelAdmin


@admin.register(College)
class CollegeAdmin(ImportExportModelAdmin):
    list_display = ('college_id', 'name', 'abbreviation', 'passkey' , 'tosend' , 'emails')

@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):
    list_display = ('event_id', 'name', 'event_type', 'no_of_teams', 'max_univeristy_teams')

@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    list_display = ('team_id', 'team_name', 'visible_name', 'college', 'sport', 'isPaid', 'isWaiting', 'registered_at', 'status')

@admin.register(Participants)
class ParticipantsAdmin(ImportExportModelAdmin):
    list_display = ('participant_id', 'name', 'email', 'phone_number', 'accomdation', 'college', 'sport', 'team', 'isCaptain', 'isPaid', 'isGitamite', 'transaction_id')



class HackathonAdmin(ImportExportModelAdmin):
    list_display = ['name', 'event_type', 'min_team_size', 'max_team_size']
    search_fields = ['name', 'event_type']

class HackathonTeamAdmin(ImportExportModelAdmin):
    list_display = ['team_name', 'visible_name', 'college', 'hackathon', 'isPaid', 'isQualified', 'registered_at']
    search_fields = ['team_name', 'visible_name', 'college__name', 'hackathon__name']

class HackathonParticipantsAdmin(ImportExportModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'accomdation', 'college', 'hackathon', 'team', 'isCaptain', 'isPaid', 'isGitamite']
    search_fields = ['name', 'email', 'phone_number', 'college__name', 'hackathon__name', 'team__team_name']
    list_filter = [ 'college']

admin.site.register(Hackathon, HackathonAdmin)
admin.site.register(HackathonTeam, HackathonTeamAdmin)
admin.site.register(HackathonParticipants, HackathonParticipantsAdmin)

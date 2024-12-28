from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

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


class CollegeResource(resources.ModelResource):
    class Meta:
        model = College
        fields = (
            "name",
            "abbreviation",
            "college_id",
            "passkey",
            "tosend",
            "emails",
        )
        export_order = fields


class EventResource(resources.ModelResource):
    class Meta:
        model = Event
        fields = (
            "name",
            "description",
            "event_type",
            "event_id",
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
        export_order = fields


class TeamResource(resources.ModelResource):
    college = fields.Field(
        column_name="college",
        attribute="college",
        widget=ForeignKeyWidget(College, "name"),
    )
    sport = fields.Field(
        column_name="sport", attribute="sport", widget=ForeignKeyWidget(Event, "name")
    )

    class Meta:
        model = Team
        fields = (
            "team_name",
            "visible_name",
            "college",
            "sport",
            "team_id",
            "isPaid",
            "isWaiting",
            "registered_at",
            "status",
            "team_size",
        )
        export_order = fields


class HackathonResource(resources.ModelResource):
    class Meta:
        model = Hackathon
        fields = (
            "name",
            "event_type",
            "min_team_size",
            "max_team_size",
        )
        export_order = fields


class HackathonTeamResource(resources.ModelResource):
    college = fields.Field(
        column_name="college",
        attribute="college",
        widget=ForeignKeyWidget(College, "name"),
    )
    hackathon = fields.Field(
        column_name="hackathon",
        attribute="hackathon",
        widget=ForeignKeyWidget(Hackathon, "name"),
    )

    class Meta:
        model = HackathonTeam
        fields = (
            "team_name",
            "visible_name",
            "college",
            "hackathon",
            "isPaid",
            "isQualified",
            "registered_at",
        )
        export_order = fields


class HackathonParticipantsResource(resources.ModelResource):
    college = fields.Field(
        column_name="college",
        attribute="college",
        widget=ForeignKeyWidget(College, "name"),
    )
    hackathon = fields.Field(
        column_name="hackathon",
        attribute="hackathon",
        widget=ForeignKeyWidget(Hackathon, "name"),
    )
    team = fields.Field(
        column_name="team",
        attribute="team",
        widget=ForeignKeyWidget(HackathonTeam, "team_name"),
    )

    class Meta:
        model = HackathonParticipants
        fields = (
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
        )
        export_order = fields


@admin.register(College)
class CollegeAdmin(ImportExportModelAdmin):
    resource_class = CollegeResource
    list_display = ("college_id", "name", "abbreviation", "passkey", "tosend", "emails")
    search_fields = ["name", "abbreviation", "college_id", "emails"]


@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):
    resource_class = EventResource
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
    list_filter = ("event_type", "event_start_date", "event_end_date")
    search_fields = ["name", "event_id", "description", "event_type"]


@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    resource_class = TeamResource
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
        "team_size",
    )
    list_filter = ("sport", "isPaid", "isWaiting", "status", "college", "team_size")
    search_fields = ["team_id", "team_name", "visible_name", "college__name", "sport__name"]


class ParticipantsResource(resources.ModelResource):
    college = fields.Field(
        column_name="college",
        attribute="college",
        widget=ForeignKeyWidget(College, "name"),
    )
    sport = fields.Field(
        column_name="sport", attribute="sport", widget=ForeignKeyWidget(Event, "name")
    )
    team = fields.Field(
        column_name="team", attribute="team", widget=ForeignKeyWidget(Team, "team_name")
    )

    class Meta:
        model = Participants
        fields = (
            "name",
            "email",
            "phone_number",
            "participant_id",
            "accomdation",
            "college",
            "sport",
            "team",
            "isCaptain",
            "isPaid",
            "isGitamite",
            "shoreid",
        )
        export_order = fields


@admin.register(Participants)
class ParticipantsAdmin(ImportExportModelAdmin):
    resource_class = ParticipantsResource
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
    list_filter = ("sport", "isPaid", "isCaptain", "isGitamite", "accomdation", "college")
    search_fields = [
        "participant_id",
        "name", 
        "email",
        "phone_number",
        "shoreid",
        "college__name",
        "sport__name",
        "team__team_name"
    ]


class HackathonAdmin(ImportExportModelAdmin):
    resource_class = HackathonResource
    list_display = ["name", "event_type", "min_team_size", "max_team_size"]
    search_fields = ["name", "event_type"]
    list_filter = ("event_type",)


class HackathonTeamAdmin(ImportExportModelAdmin):
    resource_class = HackathonTeamResource
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
    list_filter = ("hackathon", "isPaid", "isQualified", "college")


class HackathonParticipantsAdmin(ImportExportModelAdmin):
    resource_class = HackathonParticipantsResource
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
    list_filter = ("hackathon", "isPaid", "isCaptain", "isGitamite", "accomdation", "college")


admin.site.register(Hackathon, HackathonAdmin)
admin.site.register(HackathonTeam, HackathonTeamAdmin)
admin.site.register(HackathonParticipants, HackathonParticipantsAdmin)

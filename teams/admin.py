from django.contrib import admin
from .models import ParticipantApplication, Domain
from import_export.admin import ImportExportModelAdmin


class ParticipantApplicationAdmin(ImportExportModelAdmin):
    list_display = ("name", "email", "domain", "position", "designation", "verified")
    list_filter = ("domain", "position", "verified")
    search_fields = ("name", "email", "designation")


admin.site.register(ParticipantApplication, ParticipantApplicationAdmin)


class DomainAdmin(ImportExportModelAdmin):
    list_display = ("name", "head_email", "order")
    search_fields = ("name", "head_email")


admin.site.register(Domain, DomainAdmin)

from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import AllowedParticipants, ProfilePicUpdated


class AllowedParticipantsAdmin(ImportExportModelAdmin):
    list_display = ("email", "username", "first_name", "last_name", "otp")
    search_fields = ("email", "username", "first_name", "last_name")


admin.site.register(AllowedParticipants, AllowedParticipantsAdmin)


class ProfilePicUpdatedAdmin(ImportExportModelAdmin):
    list_display = ("email", "updated")
    search_fields = ("email",)
    list_filter = ("updated",)


admin.site.register(ProfilePicUpdated, ProfilePicUpdatedAdmin)

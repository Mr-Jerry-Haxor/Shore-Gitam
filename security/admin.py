from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


class SecurityStaffAdmin(ImportExportModelAdmin):
    list_display = ("email_id", "is_main_gate", "is_fest", "is_open_audi", "is_coke")
    list_filter = ("is_main_gate", "is_fest", "is_open_audi")
    search_fields = ("email_id",)


class MaingateEntriesAdmin(ImportExportModelAdmin):
    list_display = ("fullname", "email", "date", "time", "verifiedby", "status")
    list_filter = ("date", "status")
    search_fields = ("fullname", "email")


class MaingateStatusAdmin(ImportExportModelAdmin):
    list_display = ("fullname", "email", "status")
    list_filter = ("status",)
    search_fields = ("fullname", "email")


class FestEntriesAdmin(ImportExportModelAdmin):
    list_display = ("fullname", "email", "date", "time", "verifiedby", "status")
    list_filter = ("date", "status")
    search_fields = ("fullname", "email")


class FestStatusAdmin(ImportExportModelAdmin):
    list_display = ("fullname", "email", "status", "iscoke")
    list_filter = ("status",)
    search_fields = ("fullname", "email", "iscoke")


class FestEntriesDay2Admin(ImportExportModelAdmin):
    list_display = ("fullname", "email", "date", "time", "verifiedby", "status")
    list_filter = ("date", "status")
    search_fields = ("fullname", "email")


class FestStatusDay2Admin(ImportExportModelAdmin):
    list_display = ("fullname", "email", "status")
    list_filter = ("status",)
    search_fields = ("fullname", "email")


class OpenaudiEntriesAdmin(ImportExportModelAdmin):
    list_display = ("fullname", "email", "date", "time", "verifiedby", "status")
    list_filter = ("date", "status")
    search_fields = ("fullname", "email")


class OpenaudiStatusAdmin(ImportExportModelAdmin):
    list_display = ("fullname", "email", "status")
    list_filter = ("status",)
    search_fields = ("fullname", "email")


admin.site.register(security_staff, SecurityStaffAdmin)
admin.site.register(Maingate_entries, MaingateEntriesAdmin)
admin.site.register(Maingate_status, MaingateStatusAdmin)
admin.site.register(Fest_entries, FestEntriesAdmin)
admin.site.register(Fest_status, FestStatusAdmin)
admin.site.register(Fest_entries_day2, FestEntriesDay2Admin)
admin.site.register(Fest_status_day2, FestStatusDay2Admin)
admin.site.register(Openaudi_entries, OpenaudiEntriesAdmin)
admin.site.register(Openaudi_status, OpenaudiStatusAdmin)


from .models import coke_list


class CokeListAdmin(ImportExportModelAdmin):
    list_display = ("email", "status")
    search_fields = ("email",)


admin.site.register(coke_list, CokeListAdmin)

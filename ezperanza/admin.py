from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import payments_ezperanza, registrations_ezperanza, Fest_entries_ezperanza, Fest_status_ezperanza

class PaymentsAdmin(ImportExportModelAdmin):
    list_display = ('cnf_id', 'txn_id', 'amount', 'participation_type', 'name', 'mobile', 'email')
    search_fields = ('cnf_id', 'txn_id', 'name', 'mobile', 'email')

class RegistrationsAdmin(ImportExportModelAdmin):
    list_display = ('email', 'name', 'mobile', 'participation_type', 'email_sent', 'sent_count', 'email_sent_error')
    search_fields = ('email', 'name', 'mobile')
    list_filter = ('email_sent',)

class FestEntriesAdmin(ImportExportModelAdmin):
    list_display = ('fullname', 'email', 'date', 'time', 'verifiedby', 'status')
    search_fields = ('fullname', 'email')

class FestStatusAdmin(ImportExportModelAdmin):
    list_display = ('fullname', 'email', 'status', 'food')
    search_fields = ('fullname', 'email')
    list_filter = ('status', 'food')



admin.site.register(payments_ezperanza, PaymentsAdmin)
admin.site.register(registrations_ezperanza, RegistrationsAdmin)
admin.site.register(Fest_entries_ezperanza, FestEntriesAdmin)
admin.site.register(Fest_status_ezperanza, FestStatusAdmin)
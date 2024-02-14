from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import payments_samyukta, registrations_samyukta, Fest_entries_samyukta, Fest_status_samyukta, coke_list_samyukta

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

class CokeListAdmin(ImportExportModelAdmin):
    list_display = ('email', 'status')
    search_fields = ('email',)

admin.site.register(payments_samyukta, PaymentsAdmin)
admin.site.register(registrations_samyukta, RegistrationsAdmin)
admin.site.register(Fest_entries_samyukta, FestEntriesAdmin)
admin.site.register(Fest_status_samyukta, FestStatusAdmin)
admin.site.register(coke_list_samyukta, CokeListAdmin)
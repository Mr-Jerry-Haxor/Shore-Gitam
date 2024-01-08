from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import FestPass, Registrations

@admin.register(FestPass)
class FestPassAdmin(ImportExportModelAdmin):
    list_display = ['name', 'mobile', 'email', 'gender', 'posted_date', 'updated_date']

@admin.register(Registrations)
class RegistrationsAdmin(ImportExportModelAdmin):
    list_display = ['name', 'mobile', 'email', 'gender', 'posted_date', 'updated_date']


from import_export import resources
from .models import nongitamite

class nongitamiteResource(resources.ModelResource):
    class Meta:
        model = nongitamite

class nongitamiteAdmin(ImportExportModelAdmin):
    resource_class = nongitamiteResource
    list_display = ('shoreid', 'name', 'mobile', 'email', 'gender', 'college', 'branch', 'accommodation', 'paid')
    list_filter = ('gender', 'college', 'branch', 'accommodation', 'paid')
    search_fields = ('shoreid', 'name', 'email', 'college_roll_number', 'event_name')

admin.site.register(nongitamite, nongitamiteAdmin)
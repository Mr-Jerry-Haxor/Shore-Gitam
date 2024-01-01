from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import FestPass, Registrations

@admin.register(FestPass)
class FestPassAdmin(ImportExportModelAdmin):
    list_display = ['name', 'mobile', 'email', 'gender', 'posted_date', 'updated_date']

@admin.register(Registrations)
class RegistrationsAdmin(ImportExportModelAdmin):
    list_display = ['name', 'mobile', 'email', 'gender', 'posted_date', 'updated_date']

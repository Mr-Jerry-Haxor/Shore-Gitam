from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import FestPass, Registrations

@admin.register(FestPass)
class FestPassAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'payment_status', 'payment_date', 'payment_method')
    search_fields = ('name', 'email', 'registration_number')
    list_filter = ('payment_status', 'payment_date')
    date_hierarchy = 'payment_date'

@admin.register(Registrations)
class RegistrationsAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'payment_status', 'payment_date', 'payment_method')
    search_fields = ('name', 'email', 'registration_number')
    list_filter = ('payment_status', 'payment_date')
    date_hierarchy = 'payment_date'
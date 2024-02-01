from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import *

class StudentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'year_of_study', 'campus', 'hosteler', 'ispaid' ,'isrejected')
    list_filter = ('year_of_study', 'campus', 'hosteler', 'ispaid' , 'isrejected') 
    search_fields = ('name', 'email', 'branch', 'institute', 'department' , 'regno' , 'contact_number')
    date_hierarchy = 'registred_at'  # Replace 'created_at' with the appropriate date field in your model

admin.site.register(Student, StudentAdmin)


class ParticipantsListAdmin(ImportExportModelAdmin):
    list_display = ('emails', 'festpass' , 'notfree')
    list_filter = ('festpass',)
    search_fields = ('emails',)

admin.site.register(participants_list, ParticipantsListAdmin)
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Student

class StudentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'year_of_study', 'campus', 'hosteler', 'ispaid' ,'isrejected')
    list_filter = ('year_of_study', 'campus', 'hosteler', 'ispaid' , 'isrejected') 
    search_fields = ('name', 'email', 'branch', 'institute', 'department' , 'regno' , 'contact_number')
    date_hierarchy = 'registred_at'  # Replace 'created_at' with the appropriate date field in your model

admin.site.register(Student, StudentAdmin)
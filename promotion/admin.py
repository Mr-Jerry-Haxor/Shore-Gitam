from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Volunteer

@admin.register(Volunteer)
class VolunteerAdmin(ImportExportModelAdmin):
    list_display = ['name', 'email',  'profile_pic', 'year_of_study', 'created_at', 'isvolunteer']
    search_fields = ['name', 'email', 'year_of_study', 'regno']
    list_filter = ('ishosteler', 'isvolunteer')
    
    # Optional: Add ordering
    ordering = ('-created_at',)

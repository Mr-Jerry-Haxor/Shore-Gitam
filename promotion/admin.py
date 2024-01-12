from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from django.contrib import admin
from .models import BGMIPlayer

@admin.register(BGMIPlayer)
class BGMIPlayerAdmin(ImportExportModelAdmin):
    list_display = ('name', 'userid', 'email', 'regno', 'yearofstudy', 'campus', 'created_at')
    search_fields = ('name', 'userid', 'email', 'regno', 'campus')
    list_filter = ('yearofstudy', 'campus')
    # Additional configuration as needed
    
    
from django.contrib import admin
from .models import Volunteer

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'year_of_study' , 'created_at']  # Display these fields in the admin list view
    search_fields = ['name', 'email' , 'institute' , 'year_of_study' , 'regno']  # Enable search functionality in the admin
    list_filter = ('Campus' , 'domain_of_interest')

    # Add more configurations as per your requirement


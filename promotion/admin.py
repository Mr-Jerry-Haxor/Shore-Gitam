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

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_technology', 'is_events_cultural', 'is_events_sports', 'is_legal', 'is_operations', 'is_marketing', 'is_sponsorship', 'is_design', 'is_finance', 'is_media', 'is_security', 'is_hospitality')
    list_filter = ('is_technology', 'is_events_cultural', 'is_events_sports', 'is_legal', 'is_operations', 'is_marketing', 'is_sponsorship', 'is_design', 'is_finance', 'is_media', 'is_security', 'is_hospitality')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_technology', 'is_events_cultural', 'is_events_sports', 'is_legal', 'is_operations', 'is_marketing', 'is_sponsorship', 'is_design', 'is_finance', 'is_media', 'is_security', 'is_hospitality')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_technology', 'is_events_cultural', 'is_events_sports', 'is_legal', 'is_operations', 'is_marketing', 'is_sponsorship', 'is_design', 'is_finance', 'is_media', 'is_security', 'is_hospitality')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)






from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Task

class TaskAdmin(ImportExportModelAdmin):
    list_display = ('task_title', 'assigned_to', 'status', 'due_date')
    list_filter = ('status', 'due_date' , 'domain')
    search_fields = ('task_title', 'assigned_to', 'assigned_by')
    date_hierarchy = 'due_date'

admin.site.register(Task, TaskAdmin)

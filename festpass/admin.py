from django.contrib import admin

# Register your models here.
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'year_of_study', 'campus', 'hosteler', 'ispaid')
    list_filter = ('year_of_study', 'campus', 'hosteler', 'ispaid')
    search_fields = ('name', 'email', 'branch', 'institute', 'department')
    date_hierarchy = 'registred_at'  # Replace 'created_at' with the appropriate date field in your model

admin.site.register(Student, StudentAdmin)
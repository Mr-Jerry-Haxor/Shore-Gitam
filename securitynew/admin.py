from django.contrib import admin
from .models import UserIn

@admin.register(UserIn)
class UserInAdmin(admin.ModelAdmin):
    list_display = ('user', 'in_time', 'is_user_in')
    list_filter = ('is_user_in', 'in_time')
    search_fields = ('user__name',)  # Assuming name is a field in CustomUser model

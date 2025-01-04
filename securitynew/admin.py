from django.contrib import admin
from .models import UserIn
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class UserInResource(resources.ModelResource):
    class Meta:
        model = UserIn
        fields = ('user', 'in_time', 'is_user_in', 'email')

@admin.register(UserIn)
class UserInAdmin(ImportExportModelAdmin):
    resource_class = UserInResource
    list_display = ('user', 'in_time', 'is_user_in', 'email')
    list_filter = ('is_user_in', 'in_time')
    search_fields = ('user__name', 'user__email')  # Assuming email is a field in CustomUser model

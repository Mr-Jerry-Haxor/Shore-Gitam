from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from import_export.admin import ImportExportModelAdmin
from .models import CustomUser, DomainLead


class DomainLeadAdmin(admin.ModelAdmin):
    list_display = (
        "domain",
        "leads",
    )
    list_filter = ("domain", "leads")
    search_fields = ("domain", "leads")
    ordering = ("domain",)


admin.site.register(DomainLead, DomainLeadAdmin)


class CustomUserAdmin(ImportExportModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "name",
        "registration_number",
        "profile_picture",
        "aadhar_card",
        "passhash",
        "event_manager",
        "campus_head_hyd",
        "campus_head_blr",
        "coordinator",
        "president",
        "vice_president",
        "technology",
        "events_cultural",
        "events_sports",
        "legal",
        "operations",
        "marketing",
        "sponsorship",
        "design",
        "finance",
        "media",
        "security",
        "hospitality",
        "advisory",
        "hospitality_staff",
        "events_cultural_staff",
        "events_sports_staff",
        "security_staff",
        "isLead",
        "phone_number",
        "age",
        "gender",
        "college",
        "year_of_study",
        "course",
        "branch",
        "campus",
        "is_festpass_purchased",
        "is_gitamite",
        "prebooking",
        "accomdation",
        "grievance_staff",
    )
    list_filter = (
        "event_manager",
        "campus_head_hyd",
        "campus_head_blr",
        "coordinator",
        "president",
        "vice_president",
        "technology",
        "events_cultural",
        "events_sports",
        "legal",
        "operations",
        "marketing",
        "sponsorship",
        "design",
        "finance",
        "media",
        "security",
        "hospitality",
        "advisory",
        "hospitality_staff",
        "events_cultural_staff",
        "events_sports_staff",
        "security_staff",
        "isLead",
        "is_festpass_purchased",
        "is_gitamite",
        "prebooking",
        "accomdation",
        "grievance_staff",
        "gender",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "name",
                    "registration_number",
                    "profile_picture",
                    "aadhar_card",
                    "phone_number",
                    "age",
                    "gender",
                    "college",
                    "year_of_study",
                    "course",
                    "branch",
                    "campus",
                    "is_festpass_purchased",
                    "is_gitamite",
                    "passhash",
                    "prebooking",
                    "accomdation",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "event_manager",
                    "campus_head_hyd",
                    "campus_head_blr",
                    "coordinator",
                    "president",
                    "vice_president",
                    "technology",
                    "events_cultural",
                    "events_sports",
                    "legal",
                    "operations",
                    "marketing",
                    "sponsorship",
                    "design",
                    "finance",
                    "media",
                    "security",
                    "hospitality",
                    "advisory",
                    "hospitality_staff",
                    "events_cultural_staff",
                    "events_sports_staff",
                    "security_staff",
                    "isLead",
                    "grievance_staff",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "profile_picture",
                    "aadhar_card",
                    "phone_number",
                    "age",
                    "gender",
                    "college",
                    "year_of_study",
                    "course",
                    "branch",
                    "is_staff",
                    "is_superuser",
                    "event_manager",
                    "campus_head_hyd",
                    "campus_head_blr",
                    "coordinator",
                    "president",
                    "vice_president",
                    "technology",
                    "events_cultural",
                    "events_sports",
                    "legal",
                    "operations",
                    "marketing",
                    "sponsorship",
                    "design",
                    "finance",
                    "media",
                    "security",
                    "hospitality",
                    "advisory",
                    "hospitality_staff",
                    "events_cultural_staff",
                    "events_sports_staff",
                    "security_staff",
                    "isLead",
                ),
            },
        ),
    )
    search_fields = ("username", "email", "college", "course", "branch")
    ordering = ("-date_joined", "username",)


admin.site.register(CustomUser, CustomUserAdmin)


from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Task


class TaskAdmin(ImportExportModelAdmin):
    list_display = (
        "task_title",
        "domain",
        "assigned_to",
        "assigned_by",
        "status",
        "priority",
        "due_date",
        "coordinator",
        "submitted_by",
    )
    list_filter = (
        "status",
        "priority",
        "due_date",
        "domain",
        "coordinator",
    )
    search_fields = (
        "task_title",
        "assigned_to",
        "assigned_by",
        "description",
        "submitted_by",
    )
    date_hierarchy = "due_date"
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Task, TaskAdmin)


from .models import FileUpload


class FileUploadAdmin(admin.ModelAdmin):
    list_display = ("name", "file", "uploaded_at")


# Register your models here
admin.site.register(FileUpload, FileUploadAdmin)

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import FestPass, Registrations, nongitamite


@admin.register(FestPass)
class FestPassAdmin(ImportExportModelAdmin):
    list_display = [
        "name",
        "mobile",
        "email",
        "gender",
        "posted_date",
        "amount",
        "transaction_status",
        "confirm_id",
    ]
    list_filter = ["transaction_status"]
    search_fields = [
        "name",
        "mobile",
        "email",
        "posted_date",
        "txn_id",
        "confirm_id",
        "order_id",
    ]
    date_hierarchy = "posted_date"


@admin.register(Registrations)
class RegistrationsAdmin(ImportExportModelAdmin):
    list_display = [
        "name",
        "mobile",
        "email",
        "gender",
        "posted_date",
        "amount",
        "transaction_status",
        "confirm_id",
    ]
    list_filter = ["transaction_status"]
    search_fields = [
        "name",
        "mobile",
        "email",
        "posted_date",
        "txn_id",
        "confirm_id",
        "order_id",
    ]
    date_hierarchy = "posted_date"

admin.site.register(nongitamite)

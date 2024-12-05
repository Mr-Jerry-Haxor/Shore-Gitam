from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import FestPass, Registrations


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


from import_export import resources
from .models import nongitamite


class nongitamiteResource(resources.ModelResource):
    class Meta:
        model = nongitamite


class nongitamiteAdmin(ImportExportModelAdmin):
    resource_class = nongitamiteResource
    list_display = (
        "shoreid",
        "name",
        "mobile",
        "email",
        "gender",
        "college",
        "branch",
        "accommodation",
        "paid",
    )
    list_filter = ("gender", "college", "branch", "accommodation", "paid")
    search_fields = ("shoreid", "name", "email", "college_roll_number", "event_name")


admin.site.register(nongitamite, nongitamiteAdmin)

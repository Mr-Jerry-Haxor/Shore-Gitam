from django.contrib import admin

from .models import HospitalityUser, Meal, MealHistory, ParticipantsNOC


from import_export.admin import ImportExportModelAdmin


class HospitalityUserAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "phone_number",
        "isfoodonly",
        "meal_id",
        "qr_hash",
        "otp",
        "checkin",
        "checkout",
        "hostel",
        "room_number",
        "checkin_status",
        "checkout_status",
    )
    list_filter = ("hostel", "checkin_status", "checkout_status")
    search_fields = ("name", "email", "phone_number")


class MealAdmin(ImportExportModelAdmin):
    list_display = ("meal_type", "date", "start_time", "end_time")
    list_filter = ("meal_type",)
    search_fields = ("meal_type", "date")


class MealHistoryAdmin(ImportExportModelAdmin):
    list_display = ("user", "meal_type", "scanned_time")
    list_filter = ("meal_type__meal_type",)
    search_fields = ("user__name", "meal_type__meal_type", "meal_type__date")


admin.site.register(HospitalityUser, HospitalityUserAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(MealHistory, MealHistoryAdmin)


class ParticipantsNOCAdmin(ImportExportModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone_number",
        "regno",
        "gender",
        "yearofstudy",
        "branch",
        "institute",
        "department",
        "campus",
        "hosteler",
        "eventtype",
        "eventname",
        "teamname",
        "tshirt",
        "accomodation",
        "travelling",
        "departure",
        "arrival",
        "departureDatetime",
        "arrivalDatetime",
        "noc_file_input",
        "ticket_file_input",
        "profile_pic",
    )
    search_fields = (
        "full_name",
        "email",
        "phone_number",
        "regno",
        "eventname",
        "teamname",
    )
    list_filter = (
        "gender",
        "campus",
        "hosteler",
        "eventtype",
        "eventname",
        "accomodation",
        "travelling",
        "departure",
        "arrival",
    )


admin.site.register(ParticipantsNOC, ParticipantsNOCAdmin)

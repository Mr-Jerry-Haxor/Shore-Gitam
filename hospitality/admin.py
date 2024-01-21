from django.contrib import admin

from .models import HospitalityUser, Meal, MealHistory , ParticipantsNOC

admin.site.register(HospitalityUser)
admin.site.register(Meal)
admin.site.register(MealHistory)


from import_export.admin import ImportExportModelAdmin

class ParticipantsNOCAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'regno', 'gender', 'yearofstudy', 'branch', 'institute', 'department', 'campus', 'hosteler', 'eventtype', 'eventname', 'teamname', 'tshirt', 'accomodation', 'travelling', 'departure', 'arrival', 'departureDatetime', 'arrivalDatetime' , 'noc_file_input' ,'ticket_file_input' , 'profile_pic' )
    search_fields = ('full_name', 'email', 'phone_number', 'regno', 'eventname', 'teamname')
    list_filter = ('gender','campus', 'hosteler', 'eventtype', 'eventname', 'accomodation', 'travelling', 'departure', 'arrival')

admin.site.register(ParticipantsNOC, ParticipantsNOCAdmin)
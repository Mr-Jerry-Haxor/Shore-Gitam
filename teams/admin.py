from django.contrib import admin
from .models import ParticipantApplication, Domain

class ParticipantApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'domain', 'position', 'designation', 'verified')
    list_filter = ('domain', 'position', 'verified')
    search_fields = ('name', 'email', 'designation')

admin.site.register(ParticipantApplication, ParticipantApplicationAdmin)


class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_email', 'order')
    search_fields = ('name', 'head_email')

admin.site.register(Domain, DomainAdmin)

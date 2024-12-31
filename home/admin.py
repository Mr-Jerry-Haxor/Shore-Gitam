from django.contrib import admin
from .models import PaymentIssueEmail, FreePass

@admin.register(FreePass)
class FreePassAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(PaymentIssueEmail)
class PaymentIssueEmailAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment', 'status', 'added_time')
    search_fields = ('user__email', 'payment__email', 'status')
    list_filter = ('status', 'added_time')
    ordering = ('-added_time',)
    readonly_fields = ('added_time',)

from django.urls import path
from .views import RegistrationListView, send_email_to_particular_email , import_payments_to_registrations , SendEmailsView , ReSendEmailsView , festpass_scan_kalakrithi , festpass_verify_kalakrithi , kalakrithihome

app_name = "kalakrithi"

urlpatterns = [
    path('registrations/', RegistrationListView.as_view(), name='registrations_list'),
    path('registrations/<str:email>/resend/', send_email_to_particular_email, name='resend_email'),
    path('import/' , import_payments_to_registrations , name='import_registrations'),
    path('send_emails/', SendEmailsView.as_view(), name='send_emails'),
    path('resend_emails/', ReSendEmailsView.as_view(), name='resend_emails'),
    path('festpass/' , festpass_scan_kalakrithi , name='festpass_scan'),
    path('festverify/', festpass_verify_kalakrithi, name='festpassverify'),
    path("" , kalakrithihome , name='kalakrithihome')
]
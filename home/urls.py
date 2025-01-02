from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "home"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("shore25/festpass/", views.festpass, name="festpass"),
    path("eticket/", views.eticket, name="eticket"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("prebook/", views.prebooking, name="prebooking"),
    path("update-name/", views.update_name, name="update-name"),
    # path("send-student-emails/", views.send_student_emails),
    path("add-zones/", views.add_zones, name="add_zones"),
]

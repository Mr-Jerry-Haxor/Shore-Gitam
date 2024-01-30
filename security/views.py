import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from festpass.models import *

@login_required(login_url="/auth/login/google-oauth2/")
def security_home(request):
    if security_staff.objects.filter(email_id=request.user.email).exists():
        return render(request, 'securityhome.html')
    else:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('index')
    
    
@login_required(login_url="/auth/login/google-oauth2/")
def festpass_scan(request):
    if security_staff.objects.filter(email_id=request.user.email).exists() and security_staff.objects.get(email_id=request.user.email).is_fest:
        if request.method == 'POST':
            qrhash = request.POST.get('qrhash')
            if Student.objects.filter(passhash=qrhash).exists():
                student = Student.objects.get(passhash=qrhash)
                email = student.email
                entries = Fest_entries.objects.filter(email=email)
                entrycount = len(entries)
                if entrycount % 2 == 0:
                    status = "IN"
                else:
                    status = "OUT"
                insidecount = Fest_status.objects.filter(status="IN").count()
                outsidecount = Fest_status.objects.filter(status="OUT").count()
                return render(request, 'security_fest_verify.html', {'student': student, 'entries': entries ,  'cam' : "cam0"  , "status" : status , "insidecount" : insidecount , "outsidecount" : outsidecount})
            else:
                messages.error(request, 'This student has not registered for the festpass.')
                return redirect('festpass_scan')
        else:
            return render(request, 'securityscan.html')
    else:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('index')
    
    
@login_required(login_url="/auth/login/google-oauth2/")
def festpass_scan1(request):
    if security_staff.objects.filter(email_id=request.user.email).exists() and security_staff.objects.get(email_id=request.user.email).is_fest:
        if request.method == 'POST':
            qrhash = request.POST.get('qrhash')
            if Student.objects.filter(passhash=qrhash).exists():
                student = Student.objects.get(passhash=qrhash)
                email = student.email
                entries = Fest_entries.objects.filter(email=email)
                entrycount = len(entries)
                if entrycount % 2 == 0:
                    status = "IN"
                else:
                    status = "OUT"
                insidecount = Fest_status.objects.filter(status="IN").count()
                outsidecount = Fest_status.objects.filter(status="OUT").count()
                return render(request, 'security_fest_verify.html', {'student': student, 'entries': entries ,  'cam' : "cam0"  , "status" : status , "insidecount" : insidecount , "outsidecount" : outsidecount})
            else:
                messages.error(request, 'This student has not registered for the festpass.')
                return redirect('festpass_scan1')
        else:
            return render(request, 'securityscan1.html')
    else:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('index')
    
    
@login_required(login_url="/auth/login/google-oauth2/") 
def festpass_verify(request):
    if security_staff.objects.filter(email_id=request.user.email).exists() and security_staff.objects.get(email_id=request.user.email).is_fest:
        if request.method == 'POST':
            email = request.POST.get('email')
            cam = request.POST.get('cam')
            if Fest_status.objects.filter(email=email).exists():
                status = Fest_status.objects.get(email=email).status
                if status == 'IN':
                    Fest_status.objects.filter(email=email).update(status='OUT')
                    adding = Fest_entries(email=email, fullname=Fest_status.objects.get(email=email).fullname, verifiedby=request.user.email , status="OUT")
                    adding.save()
                    messages.success(request, "You have successfully exited.")
                elif status == 'OUT': 
                    Fest_status.objects.filter(email=email).update(status='IN')
                    adding = Fest_entries(email=email, fullname=Fest_status.objects.get(email=email).fullname, verifiedby=request.user.email , status="IN") 
                    adding.save()
                    messages.success(request, "You have successfully entered.")
            else:
                student = Student.objects.get(email=email)
                studentname = student.name
                Feststatus = Fest_status(email=email, fullname=studentname, status="IN")
                Feststatus.save()
                adding = Fest_entries(email=email, fullname=studentname, verifiedby=request.user.email , status="IN")
                adding.save()
                messages.success(request, "You have successfully entered.")
            if cam == "cam0":
                return redirect('festpass_scan')
            elif cam == "cam1":
                return redirect('festpass_scan1')
            else:
                return redirect('festpass_scan')
    else:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('index')
    
    
# main gate
from hospitality.models import *
 
@login_required(login_url="/auth/login/google-oauth2/")
def maingate_scan(request):
    if security_staff.objects.filter(email_id=request.user.email).exists() and security_staff.objects.get(email_id=request.user.email).is_main_gate:
        if request.method == 'POST':
            qrhash = request.POST.get('qrhash')
            if HospitalityUser.objects.filter(email=qrhash).exists():
                student = HospitalityUser.objects.get(email=qrhash)
                email = student.email
                entries = Maingate_entries.objects.filter(email=email)
                entrycount = len(entries)
                if entrycount % 2 == 0:
                    status = "IN"
                else:
                    status = "OUT"
                insidecount = Maingate_status.objects.filter(status="IN").count()
                outsidecount = Maingate_status.objects.filter(status="OUT").count()
                return render(request, 'security_maingate_verify.html', {'student': student, 'entries': entries ,  'cam' : "cam0"  , "status" : status  , "insidecount" : insidecount , "outsidecount" : outsidecount})
            else:
                messages.error(request, 'This student has not registered for the festpass.')
                return redirect('maingate_scan')
        else:
            return render(request, 'securityscan.html')
    else:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('index')
    
    
@login_required(login_url="/auth/login/google-oauth2/")
def maingate_scan1(request):
    if security_staff.objects.filter(email_id=request.user.email).exists() and security_staff.objects.get(email_id=request.user.email).is_main_gate:
        if request.method == 'POST':
            qrhash = request.POST.get('qrhash')
            if HospitalityUser.objects.filter(email=qrhash).exists():
                student = HospitalityUser.objects.get(email=qrhash)
                email = student.email
                entries = Maingate_entries.objects.filter(email=email)
                entrycount = len(entries)
                if entrycount % 2 == 0:
                    status = "IN"
                else:
                    status = "OUT"
                insidecount = Maingate_status.objects.filter(status="IN").count()
                outsidecount = Maingate_status.objects.filter(status="OUT").count()
                return render(request, 'security_maingate_verify.html', {'student': student, 'entries': entries , 'cam' : "cam1" , "status" : status  , "insidecount" : insidecount , "outsidecount" : outsidecount})
            else:
                messages.error(request, 'This student has not registered for the festpass.')
                return redirect('maingate_scan1')
        else:
            return render(request, 'securityscan1.html')
    else:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('index')
    
    
@login_required(login_url="/auth/login/google-oauth2/") 
def maingate_verify(request):
    if security_staff.objects.filter(email_id=request.user.email).exists() and security_staff.objects.get(email_id=request.user.email).is_main_gate:
        if request.method == 'POST':
            email = request.POST.get('email')
            cam = request.POST.get('cam')
            if Maingate_status.objects.filter(email=email).exists():
                status = Maingate_status.objects.get(email=email).status
                if status == 'IN':
                    Maingate_status.objects.filter(email=email).update(status='OUT')
                    adding = Maingate_entries(email=email, fullname=Maingate_status.objects.get(email=email).fullname, verifiedby=request.user.email , status="OUT")
                    adding.save()
                    messages.success(request, "You have successfully exited.")
                elif status == 'OUT': 
                    Maingate_status.objects.filter(email=email).update(status='IN')
                    adding = Maingate_entries(email=email, fullname=Maingate_status.objects.get(email=email).fullname, verifiedby=request.user.email , status="IN") 
                    adding.save()
                    messages.success(request, "You have successfully entered.")
            else:
                student = HospitalityUser.objects.get(email=email)
                studentname = student.name
                Feststatus = Maingate_status(email=email, fullname=studentname, status="IN")
                Feststatus.save()
                adding = Maingate_entries(email=email, fullname=studentname, verifiedby=request.user.email , status="IN")
                adding.save()
                messages.success(request, "You have successfully entered.")
            if cam == "cam0":
                return redirect('maingate_scan')
            elif cam == "cam1":
                return redirect('maingate_scan1')
            else:
                return redirect('maingate_scan')
    else:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('index')
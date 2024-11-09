from django.shortcuts import render, redirect
from .models import Student, participants_list
import re
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from payments.models import FestPass

import hashlib
import requests
import json
import datetime


def generate_md5(user_string):
    hashed_string = hashlib.md5(user_string.encode("UTF-8"))
    return hashed_string.hexdigest()


@login_required(login_url="/auth/login/google-oauth2/")
def passhome(request):
    if Student.objects.filter(email=request.user.email).exists():
        if Student.objects.get(email=request.user.email).isrejected:
            reason = Student.objects.get(email=request.user.email).rejected_reason
            return render(request, "passreject.html", {"reason": reason})
        if Student.objects.get(email=request.user.email).ispaid:
            student = Student.objects.get(email=request.user.email)
            # hashtext = str(student.regno) +  str(student.registred_at) + str(student.email) + str(datetime.datetime.now())
            # hash = generate_md5(hashtext)
            # student.passhash = hash
            # student.save()
            return render(request, "passes.html", {"student": student})
        else:
            student = Student.objects.get(email=request.user.email)
            entries = FestPass.objects.filter(email=request.user.email)
            y_count = entries.filter(transaction_status="Y").count()

            if y_count > 0:
                student.ispaid = True
                hashtext = (
                    str(student.regno)
                    + str(student.registred_at)
                    + str(student.email)
                    + str(datetime.datetime.now())
                )
                hash = generate_md5(hashtext)
                student.passhash = hash
                student.save()
                return redirect("passhome")
            elif (
                participants_list.objects.filter(emails=request.user.email).exists()
                and not participants_list.objects.get(emails=request.user.email).notfree
            ):
                student.ispaid = True
                hashtext = (
                    str(student.regno)
                    + str(student.registred_at)
                    + str(student.email)
                    + str(datetime.datetime.now())
                )
                hash = generate_md5(hashtext)
                student.passhash = hash
                student.save()
                participantpass = participants_list.objects.get(
                    emails=request.user.email
                )
                participantpass.festpass = True
                participantpass.save()
                return redirect("passhome")
            elif (
                participants_list.objects.filter(emails=request.user.email).exists()
                and participants_list.objects.get(emails=request.user.email).notfree
            ):
                if participants_list.objects.filter(emails=request.user.email).exists():
                    notfreepass = True
                    return render(
                        request,
                        "passhome.html",
                        {"student": student, "notfreepass": notfreepass},
                    )
            else:
                return render(request, "passhome.html", {"student": student})

    else:
        if not participants_list.objects.filter(emails=request.user.email).exists():
            return render(request, "passes_sold_out.html")
        elif participants_list.objects.filter(emails=request.user.email).exists():
            if request.method == "POST":
                name = request.POST.get("name")
                regno = request.POST.get("regno")
                email = request.POST.get("email")
                contact_number = request.POST.get("contact_number")
                gender = request.POST.get(
                    "gender"
                )  # Assuming gender field is present in the HTML form
                year_of_study = request.POST.get("yearofstudy")
                branch = request.POST.get("branch")
                institute = request.POST.get("institute")
                department = request.POST.get("department")
                campus = request.POST.get("campus")
                hosteler = request.POST.get("hosteler")
                profile_pic = request.FILES.get("profile_pic")

                # Check if email ends with @gitam.edu or @gitam.in
                # if not re.match(r'.+@(?:gitam\.edu|gitam\.in)$', email):
                #     messages.error(request, "Invalid email domain. Please use a Gitam email.")
                #     return redirect('passhome')
                regno = regno.upper()

                # Perform any other data validations or integrity checks here
                if Student.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists.")
                    return redirect("passhome")

                # Create Student object and save to database
                student = Student(
                    name=name,
                    regno=regno,
                    email=email,
                    contact_number=contact_number,
                    gender=gender,
                    year_of_study=year_of_study,
                    branch=branch,
                    institute=institute,
                    department=department,
                    campus=campus,
                    hosteler=hosteler,
                    profile_picture=profile_pic,
                )
                student.save()

                # Optionally, return a success message or redirect to another page
                # return HttpResponse("Student details saved successfully!")
                return redirect("passhome")
            else:
                data = {
                    "mail": str(request.user.email),
                }
                try:
                    response = requests.post(
                        "https://gevents.gitam.edu/registration/data/checkmail",
                        data=data,
                    )
                    if response.status_code == 200:
                        studentdata = json.loads(response.text)
                        if studentdata["status"] == "success":
                            return render(
                                request,
                                "userdetails.html",
                                {"studentdata": studentdata["data"]},
                            )
                        else:
                            return render(request, "userdetails.html")
                    else:
                        return render(request, "userdetails.html")
                except:
                    return render(request, "userdetails.html")


@login_required(login_url="/auth/login/google-oauth2/")
def shoreidcard(request):
    if Student.objects.filter(email=request.user.email).exists():
        student = Student.objects.get(email=request.user.email)
        return render(request, "passhome.html", {"student": student})
    else:
        return redirect("passhome")

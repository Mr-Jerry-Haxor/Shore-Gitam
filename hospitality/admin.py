from django.contrib import admin

from .models import HospitalityUser, Meal, MealHistory

admin.site.register(HospitalityUser)
admin.site.register(Meal)
admin.site.register(MealHistory)

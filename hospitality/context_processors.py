from .models import Meal


def formatted_dates(request):
    meals = Meal.objects.all()
    unique_dates = set(meal.date for meal in meals)
    formatted_dates = list(unique_dates)
    return {"formatted_dates": formatted_dates}

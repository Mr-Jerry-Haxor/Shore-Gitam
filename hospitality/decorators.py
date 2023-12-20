from functools import wraps
from django.http import HttpResponseForbidden


def email_check_required(model):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_email = request.user.email

            if model.objects.filter(email=user_email).exists():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("Access denied: Invalid email.")

        return _wrapped_view

    return decorator

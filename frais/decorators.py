from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect


def user_is_staff(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        elif request.user.is_authenticated and not request.user.is_staff:
            messages.error(request, "Vous n'avez pas les droits suffisants pour accéder à cette page")
            return redirect('frais')
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
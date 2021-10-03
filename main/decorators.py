from django.core.exceptions import PermissionDenied
from .models import GameGroup

def verify_entry_to_group(function):
    def wrap(request, *args, **kwargs):
        count = GameGroup.objects.filter(users__in=[request.user]).count()
        if count > 0:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
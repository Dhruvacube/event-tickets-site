from django.core.exceptions import PermissionDenied
from functools import lru_cache

from .models import GameGroup

@lru_cache(maxsize=5)
def verify_entry_to_group(function):
    def wrap(request, *args, **kwargs):
        count = GameGroup.objects.filter(users__in=[request.user]).count()
        if count > 0:
            return function(request, *args, **kwargs)
        raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

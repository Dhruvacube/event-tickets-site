from functools import lru_cache, wraps

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied

from .models import GameGroup, Games


@lru_cache(maxsize=5)
def verify_entry_to_group(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        count = GameGroup.objects.filter(users__in=[request.user]).count()
        if count > 0:
            return function(request, *args, **kwargs)
        raise PermissionDenied

    return wrap


def new_session_message(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.session.get("first_session") is None or Games.objects.filter(registrations_closed=False).count() != 0:
            current_site = get_current_site(request)
            messages.info(
                request,
                f'If you are facing any issue then please try the payment here <a href="https://tinyurl.com/tanzagaming" target="_blank">tinyurl.com/tanzagaming</a><br/>Also <a href="http://{current_site.domain}/announcements/7463e610-faec-49ea-8149-8268fc02ac1c">please read this announcement</a>',
            )
            request.session["first_session"] = True
        return function(request, *args, **kwargs)

    return wrap

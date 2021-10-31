from functools import wraps

from django.core.exceptions import PermissionDenied


def verify_entry_for_orders(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        count = request.user.orders.filter(payment_status="S").count()
        if count > 0:
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return wrap


def verify_entry_for_payments_history(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        count = request.user.orders.count()
        if count > 0:
            return function(request, *args, **kwargs)
        raise PermissionDenied

    return wrap

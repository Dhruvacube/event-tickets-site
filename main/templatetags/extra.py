import uuid

from django import template

from accounts.models import User

from ..models import GameGroup

register = template.Library()


@register.filter(name="range")
def _range(value: int):
    return range(value)


@register.filter(name="filter_users")
def filter_users(queryset, value: int):
    length = queryset.count()
    if value > length:
        return False
    return list(queryset)[value - 1]


@register.filter(name="filter_users_id")
def filter_users_id(queryset, value: int):
    length = queryset.count()
    if value > length:
        return False
    queryset1 = list(queryset)
    return queryset1[value - 1].unique_id


@register.filter(name="check_success")
def check_success(queryset):
    payments_list = queryset.filter(payment_status="S").count()
    if payments_list >= 1:
        return False
    return True


@register.filter(name="if_groups")
def if_groups(user):
    groups = GameGroup.objects.filter(
        users__in=[
            user,
        ]
    ).count()
    if groups >= 1:
        return True
    return False


@register.filter(name="if_user_payed")
def if_user_payed(payment_obj, user):
    if payment_obj[0].payment_id in user.orders.all():
        return False
    return True

from django import template
register = template.Library()

@register.filter(name='range')
def _range(value: int):
    return range(value)

@register.filter(name='filter_users')
def filter_users(queryset, value: int):
    length = queryset.count()
    if value > length:
        return False
    return queryset[value-1]

@register.filter(name='filter_users_id')
def filter_users_id(queryset, value: int):
    length = queryset.count()
    if value > length:
        return False
    return queryset[value-1].unique_id

@register.filter(name='check_success')
def check_success(queryset):
    payments_list = queryset.filter(payment_status='S').count()
    if payments_list >= 1:
        return False
    return True
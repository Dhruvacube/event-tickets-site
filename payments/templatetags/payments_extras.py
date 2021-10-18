from django import template

register = template.Library()


@register.filter(name="payment_stats")
def payment_stats(stat: str):
    if stat == "P":
        return '<strong class="text-warning><i class="bx bx-time-five text-warning"></i> Pending</strong>'
    if stat == "F":
        return '<strong class="text-danger"><i class="bx bx-x text-danger"></i> Failed</strong>'
    return '<strong class="text-success"><i class="bx bx-check-double text-success"></i> Success</strong>'

from django import template
register = template.Library()

@register.filter(name='range')
def _range(value: int):
    return range(value)
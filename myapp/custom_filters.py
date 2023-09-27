# custom_filters.py
from django import template


register = template.Library()

@register.filter
def is_even(value):
    return value % 2 == 0

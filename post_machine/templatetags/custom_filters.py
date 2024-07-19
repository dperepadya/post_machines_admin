import datetime
from django import template


register = template.Library()


@register.filter
def timestamp_to_date(value):
    try:
        return datetime.datetime.fromtimestamp(int(value) / 1000).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return value

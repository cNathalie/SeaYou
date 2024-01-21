from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='parse_and_format_date')
def parse_and_format_date(date_str):
    try:
        parsed_date = datetime.fromisoformat(date_str)
        return parsed_date.strftime("%d %b %Y, %H:%M" )
    except ValueError:
        return 'Date unknown' 
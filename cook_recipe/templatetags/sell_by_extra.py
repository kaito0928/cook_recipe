from django import template
import datetime

register = template.Library()

@register.filter(expects_localtime=True)
def is_three_days_later(value):
    if type(value) is datetime.datetime:
        value = value.date()
        today = value.today()
        three_days_later = today + datetime.timedelta(days=3)
    return today <= value <= three_days_later

@register.filter(expects_localtime=True)
def is_expired(value):
    if type(value) is datetime.datetime:
        value = value.date()
        today = value.today()
    return today > value
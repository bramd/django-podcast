from django.template import Library
from django.conf import settings
from podcast.utils.dateformat import format, time_format

register = Library()

def fixed_date(value, arg=None):
    """Formats a date according to the given format."""
    if not value:
        return u''
    if arg is None:
        arg = settings.DATE_FORMAT
    try:
        return format(value, arg)
    except AttributeError:
        return ''
fixed_date.is_safe = False

def fixed_time(value, arg=None):
    """Formats a time according to the given format."""
    if value in (None, u''):
        return u''
    if arg is None:
        arg = settings.TIME_FORMAT
    try:
        return time_format(value, arg)
    except AttributeError:
        return ''
fixed_time.is_safe = False

register.filter(fixed_date)
register.filter(fixed_time)

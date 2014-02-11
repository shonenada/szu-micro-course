import time
from datetime import datetime

from flask import g
from flask.ext.babel import gettext, lazy_gettext as _


def setup_request_timer():
    g.request_start_time = time.time()


def format_datetime(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime(gettext('%%Y-%%m-%%d'))


def friendly_time(time):
    now = datetime.utcnow()
    if type(time) is datetime:
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days
    if day_diff < 0:
        return ''
    if day_diff == 0:
        if second_diff < 10:
            return _('Just now')
        if second_diff < 60:
            return _('%(secdiff)s seconds ago', secdiff=str(second_diff))
        if second_diff < 120:
            return _('1 minute ago')
        if second_diff < 3600:
            return _('%(secdiff)s minutes ago', secdiff=str(second_diff / 60))
        if second_diff < 7200:
            return _('1 hour ago')
        if second_diff < 86400:
            return _('%(secdiff)s hours ago', secdiff=str(second_diff / 3600))
    if day_diff == 1:
        return _('Yesterday')
    if day_diff < 7:
        return _('%(secdiff)s day(s) ago', secdiff=str(day_diff))
    if day_diff < 31:
        return _('%(secdiff)s week(s) ago', secdiff=str(day_diff / 7))
    if day_diff < 365:
        return _('%(secdiff)s month(s) ago', secdiff=str(day_diff / 30))
    return _('%(secdiff)s year(s) ago', secdiff=str(day_diff / 365))

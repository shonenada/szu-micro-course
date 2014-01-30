#-*- coding: utf-8 -*-
from datetime import datetime

from speaklater import is_lazy_string
from flask.ext.babel import lazy_gettext as _

from flask import flash as f


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


def enumdef(attr_name, attr_values):
    descriptor = property(lambda self: getattr(self, attr_name))

    @descriptor.setter
    def descriptor(self, value):
        assert(value in attr_values)
        setattr(self, attr_name, value)

    return descriptor


def flash(message, category='message', form_errors=False):
    def form_errors_parse(form_errors_message):
        for v in form_errors_message.values():
            yield ", ".join(v)

    if isinstance(message, (str, unicode)):
        f(message=message, category=category)

    if isinstance(message, dict):
        if form_errors:
            f(message=', '.join([v for v in form_errors_parse(message)]),
              category=category)
        else:
            f(message=', '.join(message.values()), category=category)

    if isinstance(message, list):
        f(message=', '.join(message), category=category)

    if isinstance(message, tuple):
        f(message=', '.join([v for v in message]), category=category)

    if is_lazy_string(message):
        f(message=unicode(message), category=category)

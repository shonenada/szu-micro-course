#-*- coding: utf-8 -*-
from speaklater import is_lazy_string

from flask import flash as f, jsonify as jify


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
            v = [unicode(v) for v in v]
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


def jsonify(**kwargs):

    def _validate(var):
        if isinstance(var, (tuple, list)):
            for i, v in enumerate(var):
                var[i] = _validate(v)
        elif isinstance(var, dict):
            for k in var:
                var[k] = _validate[k]
        else:
            if is_lazy_string(var):
                return unicode(var)
            else:
                return var
        return var

    for k in kwargs:
        kwargs[k] = _validate(kwargs[k])

    return jify(**kwargs)

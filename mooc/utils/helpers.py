#-*- coding: utf-8 -*-
import hashlib, urllib

from speaklater import is_lazy_string

from flask import flash as f


def get_avatar_url(email, size=70):
    if not email:
        email = 'None'
    URL_PATTERN = "http://www.gravatar.com/avatar/%s?%s"
    gravatar_url = URL_PATTERN % (hashlib.md5(email.lower()).hexdigest(),
                                  urllib.urlencode({'s': str(size)}))
    return gravatar_url


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

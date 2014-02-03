#-*-coding: utf-8 -*-
from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import InputRequired


class AskForm(Form):
    title = StringField(
        _('Title'), validators=[InputRequired(message=_('Title is required'))])
    content = TextAreaField(
        _('Content'),
        validators=[InputRequired(message=_("Content is required"))])
    tags = StringField(label=_('Tags'))

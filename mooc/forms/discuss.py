#-*-coding: utf-8 -*-
from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import InputRequired


class AskForm(Form):
    title = StringField(
        label=_('Title'),
        validators=[
            InputRequired(),
        ]
    )
    content = TextAreaField(
        label=_('Content'),
        validators=[
            InputRequired(),
        ]
    )
    tags = StringField(label=_('Tags'))

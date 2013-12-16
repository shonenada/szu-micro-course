#-*-coding: utf-8 -*-
from flask_wtf import Form
from wtforms import (StringField, SelectField, DateTimeField, PasswordField,
                     TextAreaField)
from wtforms.validators import InputRequired, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField


subject_state_texts =  ('Normal', 'Deleted')
subject_state_values =  ('normal', 'deleted')


class SubjectForm(Form):
    name = StringField(label=u'Name', validators=[InputRequired()])
    description = TextAreaField(label=u'Description')
    state = SelectField(
        label=u'State', default=subject_state_values[0],
        choices=[(subject_state_values[i], subject_state_texts[i])
                 for i in range(0, 2)])

#-*-coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SelectField, DateTimeField
from wtforms.validators import InputRequired

from mooc.account.model import User


state_values = User.USER_STATE_VALUES
state_texts = User.USER_STATE_TEXTS


class MasterUserForm(Form):
    username = StringField(label=u'Username')
    is_male = SelectField(
        label=u'Gender', choices=[('1', u'Male'), ('0', u'Female')])
    name = StringField(label=u'Name')
    email = StringField(label=u'Email')
    phone = StringField(label=u'Phone')
    qq = StringField(label=u'QQ')
    created = DateTimeField(label=u'Joined at')
    last_login = DateTimeField(label=u'Last-log at')
    last_ip = StringField(label=u'Last-log ip')
    state = SelectField(
        label=u'State',
        choices=[(state_values[i], state_texts[i]) for i in range(0, 4)],
        validators=[InputRequired(message="Failed!")])


class MasterSzuAccountForm(Form):
    card_id = StringField(label=u'Card ID')
    stu_number = StringField(label=u'Student Number')
    short_phone = StringField(label=u'Short Phone')

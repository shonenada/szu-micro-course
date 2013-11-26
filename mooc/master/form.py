#-*-coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SelectField, DateTimeField, PasswordField
from wtforms.validators import InputRequired, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from mooc.account.model import User, SzuAccount, College


state_values = User.USER_STATE_VALUES
state_texts = User.USER_STATE_TEXTS
type_values = SzuAccount.TYPE_VALUES
type_texts = SzuAccount.TYPE_TEXTS


class MasterUserForm(Form):
    username = StringField(label=u'Username')
    is_male = SelectField(
        label=u'Gender', choices=[('True', u'Male'), ('False', u'Female')])
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
        validators=[InputRequired(message="Please choose the state.")])


class MasterSzuAccountForm(Form):
    card_id = StringField(label=u'Card ID')
    stu_number = StringField(label=u'Student Number')
    short_phone = StringField(label=u'Short Phone')


class MasterNewUserForm(Form):

    def get_colleges():
        return College.query.all()

    username = StringField(label=u'Username', validators=[InputRequired()])
    raw_passwd = PasswordField(label=u'Password', validators=[InputRequired()])
    name = StringField(label=u'Name', validators=[InputRequired()])
    nickname = StringField(label=u'Nickname', validators=[InputRequired()])
    is_male = SelectField(label=u'Gender',
                          choices=[('True', u'Male'), ('False', u'Female')])
    email = StringField(label=u'Email', validators=[Email()])
    phone = StringField(label=u'Phone')
    short_phone = StringField(label=u'Short Phone')
    qq = StringField(label=u'QQ')
    card_id = StringField(label=u'Card ID')
    stu_number = StringField(label=u'Student Number')
    college = QuerySelectField(query_factory=get_colleges, allow_blank=False)
    szu_account_type = SelectField(
        label=u'Type',
        choices=[(type_values[i], type_texts[i]) for i in range(0, 4)])
    state = SelectField(
        label=u'State', default=state_values[3],
        choices=[(state_values[i], state_texts[i]) for i in range(0, 4)])

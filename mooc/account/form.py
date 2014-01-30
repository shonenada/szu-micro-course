#-*-coding: utf-8 -*-
from flask_wtf import Form
from wtforms import (StringField, BooleanField, PasswordField,
                     SelectField, DateTimeField, TextAreaField)
from wtforms.validators import InputRequired, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask.ext.babel import lazy_gettext as _

from mooc.account.model import User, SzuAccount, College


state_values = User.USER_STATE_VALUES
state_texts = User.USER_STATE_TEXTS
type_values = SzuAccount.TYPE_VALUES
type_texts = SzuAccount.TYPE_TEXTS


class SignInForm(Form):
    """User sign in form"""
    username = StringField(
        _('Username'),
        validators=[InputRequired(message=_('Username is required'))]
    )
    password = PasswordField(
        _('Password'),
        validators=[InputRequired(message=_('Password is required'))]
    )
    remember_me = BooleanField(_('Remember Me'))


class UserForm(Form):
    class Meta:
        model = User

    username = StringField(label=_('Username'))
    is_male = SelectField(
        label=_('Gender'),
        choices=[('True', _('Male')), ('False', _('Female'))]
        )
    name = StringField(label=_('Real Name'))
    email = StringField(label=_('Email'))
    phone = StringField(label=_('Phone Number'))
    qq = StringField(label=_('QQ'))
    created = DateTimeField(label=_('Joined at'))
    last_login = DateTimeField(label=_('Last-log at'))
    last_ip = StringField(label=_('Last-log ip'))
    state = SelectField(
        label=_('State'),
        choices=[
            (state_values[i], state_texts[i]) for i in xrange(len(state_texts))
        ],
        validators=[InputRequired(message=_("Please choose the state."))])


class SzuAccountForm(Form):
    class Meta:
        model = SzuAccount

    card_id = StringField(label=_('Card ID'))
    stu_number = StringField(label=_('Student Number'))
    short_phone = StringField(label=_('Short Phone Number'))


class NewUserForm(Form):

    def get_colleges():
        return College.query.all()

    username = StringField(label=_('Username'), validators=[InputRequired()])
    raw_passwd = PasswordField(label=_('Password'), validators=[InputRequired()])
    name = StringField(label=_('Real Name'), validators=[InputRequired()])
    nickname = StringField(label=_('Nickname'), validators=[InputRequired()])
    is_male = SelectField(label=_('Gender'),
                          choices=[('True', _('Male')), ('False', _('Female'))])
    email = StringField(label=_('Email'), validators=[Email()])
    phone = StringField(label=_('Phone Number'))
    short_phone = StringField(label=_('Short Phone Number'))
    qq = StringField(label=_('QQ'))
    card_id = StringField(label=_('Card ID'))
    stu_number = StringField(label=_('Student Number'))
    college = QuerySelectField(query_factory=get_colleges, allow_blank=False)
    szu_account_type = SelectField(
        label=_('Type'),
        choices=[
            (type_values[i], type_texts[i]) for i in xrange(len(type_texts))
        ]
    )
    state = SelectField(
        label=u'State', default=state_values[3],
        choices=[
            (state_values[i], state_texts[i]) for i in xrange(len(state_texts))
        ]
    )


class SettingForm(Form):

    def get_colleges():
        return College.query.all()

    name = StringField(label=_('Real Name'))
    nickname = StringField(label=_('Nickname'))
    is_male = SelectField(
        label=_('Gender'),
        choices=[
            ('True', _('Male')),
            ('False', _('Female'))
        ]
    )
    college = QuerySelectField(
        label=_('College'),
        query_factory=get_colleges,
        allow_blank=False
    )
    card_id = StringField(label=_('Card ID'))
    stu_number = StringField(label=_('Student Number'))
    email = StringField(label=_('Email'))
    phone = StringField(label=_('Phone Number'))
    short_phone = StringField(label=_('Short Phone Number'))

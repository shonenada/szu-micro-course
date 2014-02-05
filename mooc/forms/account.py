#-*-coding: utf-8 -*-
from flask_wtf import Form
from wtforms import (StringField, BooleanField, PasswordField,
                     SelectField, DateTimeField, IntegerField)
from wtforms.validators import InputRequired, Email, Length, Regexp, EqualTo
from wtforms.validators import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask.ext.babel import lazy_gettext as _

from mooc.models.account import User, SzuAccount, College


state_values = User.USER_STATE_VALUES
state_texts = User.USER_STATE_TEXTS
type_values = SzuAccount.TYPE_VALUES
type_texts = SzuAccount.TYPE_TEXTS

STU_NUMER_RE = '^\d{10}$'
STU_NUMER_ME = _('Student Number must be length of 10 digitals')
EMAIL_RE = '(?:^[a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+$)|(?:^$)'
EMAIL_ME = _('Invalid Email.')
PHONE_RE = '(?:^\d{11}$)|(?:^$)'
PHONE_ME = _('Phone must be length of 11 digitals')
SPHONE_RE = '(?:^\d{3,6}$)|(?:^$)'
SPHONE_ME = _('Short Phone must be length from 3 to 6 digitals')
QQ_RE = '(?:^\d{6,12}$)|(?:^$)'
QQ_ME = _('QQ must be length from 6 to 12 digitals')
CARD_ID_RE = '(?:^\d{5,6}$)|(?:^$)'
CARD_ID_ME = _('Card ID must be length of 5 or 6 digitals')

USER_EXISTED = _('Username is existed')
NICKNAME_EXISTED = _('Nickname is existed')
STU_NUMBER_EXISTED = _('Student Number is existed')


class SignInForm(Form):
    """User sign in form"""
    username = StringField(
        label=_('Username'),
        description=_('6~30 characters'),
        validators=[
            InputRequired(),
            Length(min=6, max=30),
        ]
    )
    password = PasswordField(
        label=_('Password'),
        description=_('6~20 characters'),
        validators=[
            InputRequired(),
            Length(min=6, max=20),
        ]
    )
    remember_me = BooleanField(_('Remember Me'))


class SignUpForm(Form):

    def get_colleges():
        return College.query.all()

    username = StringField(
        label=_('Username'),
        description=_('6~30 characters'),
        validators=[
            InputRequired(),
            Length(min=6, max=30),
        ]
    )
    password = PasswordField(
        label=_('Password'),
        description=_('6~20 characters'),
        validators=[
            InputRequired(),
            Length(min=6, max=20),
        ]
    )
    name = StringField(
        label=_('Real Name'),
        description=_('Your real name'),
        validators=[
            InputRequired(),
            Length(max=20),
        ]
    )
    is_male = SelectField(
        label=_('Gender'),
        choices=[
            ('True', _('Male')),
            ('False', _('Female'))
        ],
        validators=[
            InputRequired(),
        ]
    )
    stu_number = StringField(
        label=_('Student Number'),
        validators=[
            Length(min=10, max=10),
        ],
    )
    college = QuerySelectField(
        label=_('College'),
        query_factory=get_colleges,
        allow_blank=False
    )
    nickname = StringField(
        label=_('Nickname'),
        validators=[
            InputRequired(),
            Length(max=20),
        ]
    )

    def validate_username(form, field):
        find_user = User.query.filter(User.username==field.data)
        if find_user.count() > 0:
            raise ValidationError(USER_EXISTED)

    def validate_nickname(form, field):
        find_user = User.query.filter(User.nickname==field.data)
        if find_user.count() > 0:
            raise ValidationError(USER_EXISTED)

    def validate_stu_number(form, field):
        find_szu_account = SzuAccount.query.filter_by(stu_number=field.data)
        if find_szu_account.count() > 0:
            raise ValidationError(STU_NUMBER_EXISTED)


class ManageUserForm(Form):
    username = StringField(label=_('Username'))
    is_male = SelectField(
        label=_('Gender'),
        choices=[
            ('True', _('Male')),
            ('False', _('Female'))
        ],
    )
    name = StringField(label=_('Real Name'))
    email = StringField(label=_('Email'))
    phone = StringField(label=_('Phone Number'))
    qq = StringField(label=_('QQ'))
    created = DateTimeField(label=_('Joined at'))
    last_login = DateTimeField(label=_('Last-log at'))
    last_ip = StringField(label=_('Last-log ip'))
    card_id = StringField(label=_('Card ID'))
    stu_number = StringField(label=_('Student Number'))
    short_phone = StringField(label=_('Short Phone Number'))
    state = SelectField(
        label=_('State'),
        choices=[
            (state_values[i], state_texts[i]) for i in xrange(len(state_texts))
        ],
        validators=[
            InputRequired(),
        ]
    )


class CreateUserForm(Form):

    def get_colleges():
        return College.query.all()

    username = StringField(
        label=_('Username'),
        description=_('6~30 characters'),
        validators=[
            InputRequired(),
            Length(min=6, max=20)
        ]
    )
    raw_passwd = PasswordField(
        label=_('Password'),
        description=_('6~20 characters'),
        validators=[
            InputRequired(),
            Length(min=6, max=20),
        ]
    )
    name = StringField(
        label=_('Real Name'),
        validators=[
            InputRequired(),
            Length(max=20),
        ]
    )
    nickname = StringField(
        label=_('Nickname'),
        validators=[
            InputRequired(),
            Length(max=20),
        ]
    )
    is_male = SelectField(
        label=_('Gender'),
        choices=[
            ('True', _('Male')),
            ('False', _('Female'))
        ]
    )
    email = StringField(
        label=_('Email'),
        validators=[
            Regexp(regex=EMAIL_RE, message=EMAIL_ME),
        ],
    )
    phone = StringField(
        label=_('Phone Number'),
        validators=[
            Regexp(regex=PHONE_RE, message=PHONE_ME),
        ],
    )
    short_phone = StringField(
        label=_('Short Phone Number'),
        validators=[
            Regexp(regex=SPHONE_RE, message=SPHONE_ME),
        ],
    )
    qq = StringField(
        label=_('QQ'),
        validators=[
            Regexp(regex=QQ_RE, message=QQ_ME),
        ],
    )
    card_id = StringField(
        label=_('Card ID'),
        validators=[
            Regexp(regex=CARD_ID_RE, message=CARD_ID_ME),
        ],
    )
    stu_number = StringField(
        label=_('Student Number'),
        validators=[
            Regexp(regex=STU_NUMER_RE, message=STU_NUMER_ME),
        ],
    )
    college = QuerySelectField(
        label=_('College'),
        query_factory=get_colleges,
        allow_blank=False
    )
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

    name = StringField(
        label=_('Real Name'),
    )
    nickname = StringField(
        label=_('Nickname'),
    )
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
    card_id = StringField(
        label=_('Card ID'),
        validators=[
            Regexp(regex=CARD_ID_RE, message=CARD_ID_ME),
        ],
    )
    stu_number = StringField(
        label=_('Student Number'),
        validators=[
            Regexp(regex=STU_NUMER_RE, message=STU_NUMER_ME),
        ],
    )
    email = StringField(
        label=_('Email'),
        validators=[
            Regexp(regex=EMAIL_RE, message=EMAIL_ME)
        ],
    )
    phone = StringField(
        label=_('Phone Number'),
        validators=[
            Regexp(regex=PHONE_RE, message=PHONE_ME),
        ],
    )
    short_phone = StringField(
        label=_('Short Phone Number'),
        validators=[
            Regexp(regex=SPHONE_RE, message=SPHONE_ME),
        ],
    )


class PasswordForm(Form):

    old_password = PasswordField(
        label=_('Old Password'),
        description=_('6~30 characters'),
        validators=[
            InputRequired(),
            Length(min=6, max=20),
        ]
    )
    new_password = PasswordField(
        label=_('New Password'),
        description=_('6~30 characters'),
        validators=[
            InputRequired(),
            Length(min=6, max=20),
        ]
    )
    comfirm = PasswordField(
        label=_('Confirm Password'),
        description=_('6~30 characters'),
        validators=[
            EqualTo('new_password'),
        ]
    )

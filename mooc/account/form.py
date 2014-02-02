#-*-coding: utf-8 -*-
from flask_wtf import Form
from wtforms import (StringField, BooleanField, PasswordField,
                     SelectField, DateTimeField, IntegerField)
from wtforms.validators import InputRequired, Email, Length, NumberRange, EqualTo
from wtforms.validators import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask.ext.babel import lazy_gettext as _

from mooc.account.model import User, SzuAccount, College


state_values = User.USER_STATE_VALUES
state_texts = User.USER_STATE_TEXTS
type_values = SzuAccount.TYPE_VALUES
type_texts = SzuAccount.TYPE_TEXTS

USER_EXISTED = _('Username is existed')
NICKNAME_EXISTED = _('Nickname is existed')
STU_NUMBER_EXISTED = _('Student Number is existed')
MUST_BE_11_DIGITAL = _('This field must be 11 digitals')
MUST_BE_10_DIGITAL = _('This field must be 10 digitals')
MUST_BE_4_6_DIGITAL = _('This field must be 4~6 digitals')


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
    stu_number = IntegerField(
        label=_('Student Number'),
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
        if len(str(field.data)) != 10:
            raise ValidationError(MUST_BE_10_DIGITAL)

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
    state = SelectField(
        label=_('State'),
        choices=[
            (state_values[i], state_texts[i]) for i in xrange(len(state_texts))
        ],
        validators=[
            InputRequired(),
        ]
    )
    card_id = StringField(label=_('Card ID'))
    stu_number = StringField(label=_('Student Number'))
    short_phone = StringField(label=_('Short Phone Number'))


class NewUserForm(Form):

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
        ]
    )
    nickname = StringField(
        label=_('Nickname'),
        validators=[
            InputRequired(),
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
            Email(),
        ],
    )
    phone = IntegerField(
        label=_('Phone Number'),
        validators=[
        ],
    )
    short_phone = IntegerField(
        label=_('Short Phone Number'),
        validators=[
        ],
    )
    qq = IntegerField(
        label=_('QQ'),
    )
    card_id = IntegerField(
        label=_('Card ID'),
        validators=[
        ],
    )
    stu_number = IntegerField(
        label=_('Student Number'),
        validators=[
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

    def validate_phone(form, field):
        if len(str(field.data)) != 11:
            raise ValidationError(MUST_BE_11_DIGITAL)

    def validate_card_id(form, field):
        if len(str(field.data)) in range(4, 6):
            raise ValidationError(MUST_BE_4_6_DIGITAL)

    def validate_stu_number(form, field):
        if len(str(field.data)) != 10:
            raise ValidationError(MUST_BE_10_DIGITAL)

    def validate_short_phone(form, field):
        if len(str(field.data)) in range(4, 6):
            raise ValidationError(MUST_BE_4_6_DIGITAL)


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
    card_id = IntegerField(
        label=_('Card ID'),
        validators=[
        ],
    )
    stu_number = IntegerField(
        label=_('Student Number'),
        validators=[
        ],
    )
    email = StringField(
        label=_('Email'),
        validators=[
            Email(),
        ],
    )
    phone = IntegerField(
        label=_('Phone Number'),
        validators=[
        ],
    )
    short_phone = IntegerField(
        label=_('Short Phone Number'),
        validators=[
        ],
    )

    def validate_phone(form, field):
        if len(str(field.data)) != 11:
            raise ValidationError(MUST_BE_11_DIGITAL)

    def validate_card_id(form, field):
        if len(str(field.data)) in range(4, 6):
            raise ValidationError(MUST_BE_4_6_DIGITAL)

    def validate_stu_number(form, field):
        if len(str(field.data)) != 10:
            raise ValidationError(MUST_BE_10_DIGITAL)

    def validate_short_phone(form, field):
        if len(str(field.data)) in range(4, 6):
            raise ValidationError(MUST_BE_4_6_DIGITAL)


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

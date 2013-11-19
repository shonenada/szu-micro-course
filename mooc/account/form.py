#-*-coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Email


class SignInForm(Form):
    username = TextField(
        u'用户名',
        validators=[InputRequired(message=u'用户名不能为空'), Email(message=u'邮箱')])
    password = PasswordField(
        u'密码',
        validators=[InputRequired(message=u'密码不能为空')])
    remember_me = BooleanField(u'记住我')

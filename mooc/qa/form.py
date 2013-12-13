#-*-coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import InputRequired


class AskForm(Form):
    title = StringField(
        u'标题', validators=[InputRequired(message=u'标题不能为空')])
    content = TextAreaField(
        u'内容',
        validators=[InputRequired(message=u'内容不能为空')])
    tags = StringField(u'标签')

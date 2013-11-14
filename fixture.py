#-*- coding: utf-8 -*-
from mooc.app import db
from mooc.account.model import User, SzuAccount, College, Teacher
from mooc.course.model import Subject, Category, Course, Clip


def _init_college():
    global csse
    csse = College(name=u'计算机与软件学院', order=13)
    db.session.add(csse)


def _init_user():
    global shonenada, key
    shonenada = User('shonenad', '000000', 'shonenada', True)
    key = User('key', '123456', 'key', True)
    db.session.add(shonenada)
    db.session.add(key)


def _init_szu_account():
    global shonenada_account, key_account
    shonenada_account = SzuAccount(shonenada, 123456, 20111150000, csse, 'undergrade')
    key_account = SzuAccount(key, 654321, 20111150999, csse, 'teacher')
    db.session.add(shonenada_account)
    db.session.add(key_account)


def _init_teacher():
    global mr_key
    mr_key = Teacher('teacher', 'KEY', key_account)
    db.session.add(mr_key)


def _init_subject():
    global subject
    subject = Subject(name='Linux', description='Courses of Linux')
    db.session.add(subject)


def _init_category():
    global category
    category = Category('Basic Usage', 'Basic Usage', subject)
    db.session.add(category)


def _init_course():
    global course
    course = Course(
        u'Linux基本操作',
        u'课程包含Linux图形界面下的日常操作维护及命令行（CLI）下的日常操作维护。',
        key, category, '/'
    )
    db.session.add(course)


def _init_clip():
    global clip
    clip = Clip(
        u'GNOME图形界面基本操作',
        u'本课程为您讲解Linux系统主流图形界面GNOME的基本操作使用',
        shonenada, course, 1, True
    )


def init_db():
    _init_college()
    _init_user()
    _init_szu_account()
    _init_teacher()
    _init_subject()
    _init_category()
    _init_course()
    _init_clip()
    db.session.commit()

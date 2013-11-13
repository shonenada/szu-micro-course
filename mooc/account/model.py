from datetime import datetime

from mooc.app import db


class Account(db.Model):
    """Model of account."""

    __tablename__ = 'account'

    TYPE_UNDERGRADE = 0
    TYPE_RE = 1
    TYPE_TEACHER = 2
    TYPE_OTHER = 3

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(6), unique=True)
    password = db.Column(db.String(128))
    stu_number = db.Column(db.String(10), unique=True)
    nickname = db.Column(db.String(16), unique=True)
    name = db.Column(db.String(20))
    gender = db.Column(db.Boolean, default=True)
    account_type = db.Column(db.Integer)
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(11), unique=True)
    short_phone = db.Column(db.String(6), unique=True)
    qq = db.Column(db.String(15), unique=True)
    avatar = db.Column(db.String(250))
    created = db.Column(db.DateTime, default=datetime.now)
    last_ip = db.Column(db.String(40))
    last_login = db.Column(db.DateTime, default=datetime.now)
    college = db.relationship("College", backref='account', uselist=False)
    teacher = db.relationship("Teacher", backref='account', uselist=False)
    learn_record = db.relationship('LearnRecord', backref='author',
                                   uselist=True)
    question = db.relationship('Question', backref='author',
                               uselist=True, lazy='dynamic')
    answer = db.relationship('Answer', backref='author',
                             uselist=True, lazy='dynamic')
    course = db.relationship("Course", backref='author',
                             uselist=True, lazy='dynamic')
    up_down_record = db.relationship('UpDownRecord', backref='author',
                                     uselist=True, lazy='dynamic')

    def __init__(self, card_id, stu_number):
        self.card_id = card_id
        self.stu_number = stu_number


class College(db.Model):
    """Model of College"""

    __tablename__ = 'college'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    order = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    clip = db.relationship('Clip', backref='college', 
                           lazy='dynamic', uselist=True)


class Teacher(db.Model):
    """Model of Teacher"""

    __tablename__ = 'teacher'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    description = db.Column(db.Text)
    clip = db.relationship('Clip', backref='teacher', lazy='dynamic')
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

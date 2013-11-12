from datetime import datetime

from mooc.app import db


class College(db.Model):
    """Model of College"""

    __tablename__ = 'college'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    order = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey('college.id'))
    clip_id = db.Column(db.Integer, db.ForeignKey('clip.id'))


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
    number = db.Column(db.String(10), unique=True)
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
    learn_record_id = db.Column(db.Integer, db.ForeignKey('learn_record.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    up_down_record_id = db.Column(db.Integer,
                                  db.ForeignKey('up_down_record.id'))
    college = db.relationship("College", backref=db.backref('account'),
                              uselist=False)
    teacher_id = db.relationship("Teacher", backref=db.backref('account'),
                                 uselist=False)


class Teacher(db.Model):
    """Model of Teacher"""

    __tablename__ = 'teacher'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    title = db.Column(db.String(10))
    description = db.Column(db.Text)
    clip_id = db.Column(db.Integer, db.ForeignKey('clip.id'))

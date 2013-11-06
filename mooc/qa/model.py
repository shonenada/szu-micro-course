from datetime import datetime

from mooc.app import db


class Question(db.Model):

    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    edit_time = db.Column(db.DateTime, default=datetime.now)
    read_count = db.Column(db.Integer, default=0)
    up_count = db.Column(db.Integer, default=0)
    author = db.relationship('Account', backref=db.backref('question'),
                             uselist=False, lazy='dynamic')
    clip = db.relationship('Clip', backref=db.backref('question'),
                           uselist=False, lazy='dynamic')


class Answer(db.Model):

    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    up_count = db.Column(db.Integer, default=0)
    down_count = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)
    edit_time = db.Column(db.DateTime, default=datetime.now)
    up_down_record_id = db.Column(db.Integer,
                                  db.ForeignKey('up_down_record.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    parent = db.relationship('Answer', backref=db.backref('answer'),
                            uselist=False, lazy='dynamic')
    author = db.relationship('Account', backref=db.backref('answer'),
                             uselist=False, lazy='dynamic')
    clip = db.relationship('Clip', backref=db.backref('answer'),
                           uselist=False, lazy='dynamic')


class UpDownRecord(db.Model):

    __tablename__ = 'up_down_record'

    TYPE_UP = 1
    TYPE_DOWN = 0

    id = db.Column(db.Integer, primary_key=True)
    up_down = db.Column(db.Integer, default=TYPE_UP)
    craeted = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    author = db.relationship('Account', backref=db.backref('up_down_record'),
                             uselist=False, lazy='dynamic')
    answer = db.relationship('Answer', backref=db.backref('up_down_record'),
                             uselist=False, lazy='dynamic')

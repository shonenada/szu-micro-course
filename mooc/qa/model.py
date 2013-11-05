from datetime import datetime

from mooc.app import db


class Question(db.Model):

    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    author = db.relationship('Account', backref=db.backref('question'))
    clip_id = db.Column(db.Integer, db.ForeignKey('clip.id'))
    clip = db.relationship('Clip', backref=db.backref('question'))
    title = db.Column(db.String(20))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    edit_time = db.Column(db.DateTime, default=datetime.now)
    read_count = db.Column(db.Integer, default=0)
    up_count = db.Column(db.Integer, default=0)


class Answer(db.Model):

    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    author = db.relationship('Account', backref=db.backref('answer'))
    clip_id = db.Column(db.Integer, db.ForeignKey('clip.id'))
    clip = db.relationship('Clip', backref=db.backref('answer'))
    parent_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    parent = db.relationship('Answer', backref=db.backref('answer'))
    content = db.Column(db.Text)
    up_count = db.Column(db.Integer, default=0)
    down_count = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)
    edit_time = db.Column(db.DateTime, default=datetime.now)


class UpDownRecord(db.Model):

    __tablename__ = 'up_down_record'

    TYPE_UP = 1
    TYPE_DOWN = 0

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    author = db.relationship('Account', backref=db.backref('up_down_record'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    answer = db.relationship('Answer', backref=db.backref('up_down_record'))
    up_down = db.Column(db.Integer, default=TYPE_UP)
    craeted = db.Column(db.DateTime, default=datetime.now)

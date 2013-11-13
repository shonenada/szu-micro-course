from datetime import datetime

from mooc.app import db


class UpDownRecord(db.Model):

    __tablename__ = 'up_down_record'

    TYPE_UP = 1
    TYPE_DOWN = 0

    id = db.Column(db.Integer, primary_key=True)
    up_down = db.Column(db.Integer, default=TYPE_UP)
    craeted = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    answer = db.relationship('Answer', backref=db.backref('up_down_record'),
                             uselist=False)


class Answer(db.Model):

    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    up_count = db.Column(db.Integer, default=0)
    down_count = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)
    edit_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    cilp_id = db.Column(db.Integer, db.ForeignKey('clip.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    parent_id = db.Column(db.Integer)
    up_down_record_id = db.Column(db.Integer,
                                  db.ForeignKey('up_down_record.id'))


class Question(db.Model):

    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    edit_time = db.Column(db.DateTime, default=datetime.now)
    read_count = db.Column(db.Integer, default=0)
    up_count = db.Column(db.Integer, default=0)
    clip_id = db.Column(db.Integer, db.ForeignKey('clip.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    answer = db.relationship('Answer', backref='question', lazy='dynamic')

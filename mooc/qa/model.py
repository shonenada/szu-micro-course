from datetime import datetime

from mooc.app import db


class UpDownRecord(db.Model):

    __tablename__ = 'up_down_record'

    TYPE_UP = 1
    TYPE_DOWN = 0

    id = db.Column(db.Integer, primary_key=True)
    up_or_down = db.Column(db.Integer, nullable=False)
    craeted = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer = db.relationship('Answer', backref=db.backref('up_down_record'),
                             uselist=False)

    def __init__(self, user, up_or_down):
        self.created = datetime.utcnow()
        self.user = user
        if up_or_down in (TYPE_UP, TYPE_DOWN):
            self.up_or_down = up_or_down
        else:
            self.up_or_down = self.TYPE_UP


class Answer(db.Model):

    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    up_count = db.Column(db.Integer, default=0)
    down_count = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    edit_time = db.Column(db.DateTime, default=datetime.utcnow())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    clip_id = db.Column(db.Integer, db.ForeignKey('clip.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent_id = db.Column(db.Integer)
    up_down_record_id = db.Column(db.Integer,
                                  db.ForeignKey('up_down_record.id'))

    def __init__(self, content, question, clip, author, parent=None):
        self.content = content
        self.question = question
        self.clip = clip
        self.author = author
        self.parent = parent
        self.up_count = 0
        self.down_count = 0
        self.created = datetime.utcnow()
        edit_time = datetime.utcnow()


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
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    def __init__(self, title, content, clip, author):
        self.title = title
        self.content = content
        self.clip = clip
        self.author = author
        self.up_count = 0
        self.read_count = 0
        self.created = datetime.utcnow()
        self.edit_time = datetime.utcnow()

from datetime import datetime

from mooc.app import db
from mooc.account.model import Account
from mooc.qa.model import Question
from mooc.utils import enumdef


clip_tags = db.Table(
    'clip_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('clip_tag.id')),
    db.Column('clip_id', db.Integer, db.ForeignKey('clip.id'))
)

course_tags = db.Table(
    'course_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('course_tag.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


class Subject(db.Model):

    __tablename__ = 'subject'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.Text)
    category = db.relationship('Category', backref='subject', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<Subject %s>" % self.name


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    course = db.relationship('Course', backref='category', lazy='dynamcic')

    def __init__(self, name, description, subject_id):
        self.name = name
        self.description = description
        self.subject_id = subject_id

    def __repr__(self):
        return "<Category %s>" % self.name


class Course(db.Model):
    """Model of Course"""

    __tablename__ = 'course'

    COURSE_STATE_VALUES = ('finished', 'updating', 'coming')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)
    _state = db.Column('state', db.Enum(name='course_state',
                                        *COURSE_STATE_VALUES))
    state = enumdef('_state', COURSE_STATE_VALUES)
    logo_url = db.Column(db.String(50))
    created = db.Column(db.DateTime, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    clip = db.relationship('Clip', backref=db.backref('course'), uselist=True)
    tags = db.relationship('CourseTag', secondary=course_tags,
                           backref=db.backref('course', lazy='dynamic'))

    def __init__(self, name, description, author_id, logo_url, state=None):
        self.name = name
        self.description = description
        self.author_id = author_id
        self.created = datetime.utcnow()
        self.logo_url = logo_url
        self.state = state if state else 'coming'

    def __repr__(self):
        return "<Course %s>" % self.name


class Clip(db.Model):
    """Model of Course"""

    __tablename__ = 'clip'

    CLIP_STATE_VALUES = ('published', 'unpublished', 'recording')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    created = db.Column(db.DateTime, default=datetime.utcnow())
    knowledge_point = db.Column(db.Text)
    prepare_knowledge = db.Column(db.Text)
    chapter = db.Column(db.String(512))
    term = db.Column(db.String(512))
    description = db.Column(db.Text)
    record_time = db.Column(db.DateTime)
    record_address = db.Column(db.String(256))
    upload_time = db.Column(db.DateTime)
    clip_url = db.Column(db.String(150))
    clip_last = db.Column(db.String(30))
    _state = db.Column('state', db.Enum(name='clip_state', *CLIP_STATE_VALUES))
    state = enumdef('_state', CLIP_STATE_VALUES)
    read_count = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, default=1)
    play_count = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    learn_record = db.relationship('LearnRecord', backref=db.backref('clip'),
                                   uselist=True, lazy='dynamic')
    question = db.relationship('Question', backref=db.backref('clip'),
                             uselist=True, lazy='dynamic')
    answer = db.relationship('Answer', backref=db.backref('clip'),
                             uselist=True, lazy='dynamic')
    tags = db.relationship('ClipTag', secondary=clip_tags,
                           backref=db.backref('clip'))

    def __init__(self, name, description, order=None, published=False):
        self.name = name
        self.description = description
        self.created = datetime.utcnow()
        self.read_count = 0
        self.play_count = 0
        self.published = published
        self.order = order if order else 9999

    def __repr__(self):
        return "<Clip %s>" % self.name


class LearnRecord(db.Model):

    __tablename__ = 'learn_record'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    star_count = db.Column(db.Integer, default=0)
    clip_id = db.Column(db.Integer, db.ForeignKey('clip.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __init__(self, clip_id, account_id):
        self.clip_id = clip_id
        self.account_id = account_id
        self.star_count = 0
        self.created = datetime.utcnow()


class ClipTag(db.Model):
    __tablename__ = 'clip_tag'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))


class CourseTag(db.Model):

    __tablename__ = 'course_tag'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))

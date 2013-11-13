from datetime import datetime

from mooc.app import db
from mooc.account.model import Account
from mooc.qa.model import Question


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


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    course = db.relationship('Course', backref='category', lazy='dynamcic')


class Course(db.Model):
    """Model of Course"""

    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)
    status = db.Column(db.Integer)
    logo_url = db.Column(db.String(50))
    created = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    clip = db.relationship('Clip', backref=db.backref('course'), uselist=True)
    tags = db.relationship('CourseTag', secondary=course_tags,
                           backref=db.backref('course', lazy='dynamic'))


class Clip(db.Model):
    """Model of Course"""

    __tablename__ = 'clip'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
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
    published = db.Column(db.Boolean, default=False)
    read_count = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, default=1)
    play_count = db.Column(db.Integer, default=0)
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


class LearnRecord(db.Model):

    __tablename__ = 'learn_record'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    star_count = db.Column(db.Integer, default=0)
    clip_id = db.Column(db.Integer, db.ForeignKey('clip.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))


class ClipTag(db.Model):
    __tablename__ = 'clip_tag'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))


class CourseTag(db.Model):

    __tablename__ = 'course_tag'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))

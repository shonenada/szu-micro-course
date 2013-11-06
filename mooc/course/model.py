from datetime import datetime

from mooc.app import db


clip_tags = db.Table('clip_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('clip_tag.id')),
    db.Column('clip_id', db.Integer, db.ForeignKey('clip.id'))
)

course_tags = db.Table('course_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('course_tag.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


class Subject(db.Model):

    __tablename__ = 'subject'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.Text)
    subject = db.relationship('Subject', uselist=True, lazy='dynamic',
                              backref=db.backref('category'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))


class Course(db.Model):
    """Model of Course"""

    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)
    status = db.Column(db.Integer)
    logo_url = db.Column(db.String(50))
    created = db.Column(db.DateTime, default=datetime.now)
    clip_id = db.Column(db.Integer, db.ForeignKey('clip.id'))
    author = db.relationship("Account", backref=db.backref('course'),
                             uselist=False, lazy='dynamic')
    category = db.relationship('Category', backref=db.backref('course.id'),
                               uselist=False, lazy='dynamic')
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
    play_count = db.Column(db.Integer, default=0)
    learn_record_id = db.Column(db.Integer, db.ForeignKey('learn_record.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    course = db.relationship('Course', backref=db.backref('clip'),
                             uselist=False, lazy='dynamic')
    college = db.relationship('College', backref=db.backref('clip'),
                              uselist=False, lazy='dynamic')
    teacher = db.relationship("Teacher", backref=db.backref('clip'),
                              uselist=False, lazy='dynamic')
    tags = db.relationship('ClipTag', secondary=clip_tags,
                           backref=db.backref('clip', lazy='dynamic'))


class LearnRecord(db.Model):

    __tablename__ = 'learn_record'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now)
    star_count = db.Column(db.Integer, default=0)
    account = db.relationship('Account', backref=db.backref('learn_record'),
                              uselist=False, lazy='dynamic')
    clip = db.relationship('Clip', backref=db.backref('learn_record'),
                           uselist=False, lazy='dynamic')

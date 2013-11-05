from datetime import datetime

from mooc.app import db


class Course(db.Model):
    """Model of Course"""
    
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(50))
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    author = db.relationship("Account", backref=db.backref('course'))
    created = db.Column(db.DateTime, default=datetime.now)


class Clip(db.Model):
    """Model of Course"""

    __tablename__ = 'clip'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course = db.relationship('Course', backref=db.backref('clip'))
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'))
    college = db.relationship('College', backref=db.backref('clip'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    teacher = db.relationship("Teacher", backref=db.backref('clip'))
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


class LearnRecord(db.Model):

    __tablename__ = 'learn_record'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    account = db.relationship('Account', backref=db.backref('learn_record'))
    clip_id = db.Column(db.Integer, db.ForeignKey('clip.id'))
    clip = db.relationship('Clip', backref=db.backref('learn_record'))
    created = db.Column(db.DateTime, default=datetime.now)
    star_count = db.Column(db.Integer, default=0)

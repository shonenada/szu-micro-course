from datetime import datetime

from flask import url_for
from sqlalchemy import func, select
from sqlalchemy.ext.hybrid import hybrid_property

from mooc.app import db
from mooc.account.model import SzuAccount
from mooc.qa.model import Question
from mooc.utils import enumdef


lecture_tags = db.Table(
    'lecture_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('lecture_id', db.Integer, db.ForeignKey('lecture.id'))
)

course_tags = db.Table(
    'course_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)


class Subject(db.Model):

    __tablename__ = 'subject'

    SUBJECT_STATE_VALUES = ('normal', 'deleted')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.Text)
    categories = db.relationship('Category', backref='subject')
    _state = db.Column('state', db.Enum(name='course_state',
                                        *SUBJECT_STATE_VALUES))
    state = enumdef('_state', SUBJECT_STATE_VALUES)

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.state = 'normal'

    def __str__(self):
        return ("%s" % self.name)

    def __repr__(self):
        return "<Subject %s>" % self.name

    @hybrid_property
    def courses(self):
        courses = set()
        for c in self.categories:
            courses.update([course for course in c.courses])
        return list(courses)

    def delete(self, commit=True):
        for category in self.categories:
            category.delete(False)
        self.state = 'deleted'
        db.session.add(self)
        if commit:
            db.session.commit()


class Category(db.Model):

    __tablename__ = 'category'
    CATEGORY_STATE_VALUES = ('normal', 'deleted')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    courses = db.relationship('Course', backref='category')
    _state = db.Column('state', db.Enum(name='course_state',
                                        *CATEGORY_STATE_VALUES))
    state = enumdef('_state', CATEGORY_STATE_VALUES)

    def __init__(self, name, subject):
        self.name = name
        self.subject = subject
        self.state = 'normal'

    def __str__(self):
        return ("%s" % self.name)

    def __repr__(self):
        return "<Category %s>" % self.name

    def delete(self, commit=True):
        for course in self.courses:
            course.delete(False)
        self.subject = None
        self.state = 'deleted'
        db.session.add(self)
        if commit:
            db.session.commit()


class Course(db.Model):
    """Model of Course"""

    __tablename__ = 'course'

    COURSE_STATE_VALUES = ('finished', 'updating', 'coming', 'deleted')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)
    _state = db.Column('state', db.Enum(name='course_state',
                                        *COURSE_STATE_VALUES))
    state = enumdef('_state', COURSE_STATE_VALUES)
    logo_url = db.Column(db.String(50))
    created = db.Column(db.DateTime, default=datetime.utcnow())
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'))
    lectures = db.relationship('Lecture',
                               backref=db.backref('course'), uselist=True)
    tags = db.relationship('Tag', secondary=course_tags,
                           backref=db.backref('courses'))

    def __init__(self, name, description, teacher, category):
        self.name = name
        self.description = description
        self.teacher = teacher
        self.category = category
        self.created = datetime.utcnow()
        self._state = 'updating'
        self.logo_url = url_for('static',
                                filename='images/default_course_logo.png')

    def set_finished(self):
        self.state = 'finished'

    def set_updating(self):
        self.state = 'updating'

    def set_coming(self):
        self.state = 'coming'

    def delete(self, commit=True):
        for lecture in self.lectures:
            lecture.delete(False)
        for tag in self.tags:
            tag.courses.remove(self)
            db.session.add(tag)
        self.category = None
        self.teacher = None
        self.college = None
        self.state = 'deleted'
        db.session.add(self)
        if commit:
            db.session.commit()

    def __str__(self):
        return ("%s" % self.name)

    def __repr__(self):
        return "<Course %s>" % self.name


class Lecture(db.Model):
    """Model of Course"""

    __tablename__ = 'lecture'

    LECTURE_STATE_VALUES = ('published', 'recording', 'coming', 'deleted')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    knowledge_point = db.Column(db.Text)
    prepare_knowledge = db.Column(db.Text)
    term = db.Column(db.String(512))
    chapter = db.Column(db.String(512))
    record_time = db.Column(db.DateTime)
    record_address = db.Column(db.String(256))
    upload_time = db.Column(db.DateTime)
    video_url = db.Column(db.String(150))
    video_length = db.Column(db.Integer)
    logo_url = db.Column(db.String(100))
    _state = db.Column('state', db.Enum(name='lecture_state',
                                        *LECTURE_STATE_VALUES))
    state = enumdef('_state', LECTURE_STATE_VALUES)
    watch_count = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, default=1)
    play_count = db.Column(db.Integer, default=0)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    learn_records = db.relationship('LearnRecord',
                                    backref=db.backref('lecture'),
                                    uselist=True, lazy='dynamic')
    questions = db.relationship('Question', backref=db.backref('lecture'),
                                uselist=True, lazy='dynamic')
    answers = db.relationship('Answer', backref=db.backref('lecture'),
                              uselist=True, lazy='dynamic')
    tags = db.relationship('Tag', secondary=lecture_tags,
                           backref=db.backref('lectures'))

    def __init__(self, name, description, teacher, course, order=None,
                 published=False):
        self.name = name
        self.description = description
        self.teacher = teacher
        self.course = course
        self.published = published
        self.video_url = ''
        self.read_count = 0
        self.play_count = 0
        self.video_length = 0
        self.order = order if order else 9999
        self.created = datetime.utcnow()
        self.upload_time = datetime.utcnow()
        self.state = 'published'

    def set_published(self):
        self.state = 'published'

    def set_recording(self):
        self.state = 'recording'

    def set_comming(self):
        self.state = 'coming'

    def delete(self, commit=True):
        """Clean data in all relationships"""
        for q in self.questions:
            self.questions.remove(q)
        for a in self.answers:
            self.answers.remove(a)
        for t in self.tags:
            self.tags.remove(t)
        for lr in self.learn_records:
            lr.delete()
        self.course = None
        self.teacher = None
        self.state = 'deleted'
        db.session.add(self)
        if commit:
            db.session.commit()

    def __str__(self):
        return self.name
        
    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<Lecture %s>" % self.name


class Quiz(db.Model):

    __tablename__ = 'quiz'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100))
    time_at = db.Column(db.Integer)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))
    order = db.Column(db.Integer, default=100)
    lecture = db.relationship(
        'Lecture',
        backref=db.backref('quizs', uselist=True), uselist=False)
    options = db.relationship('QuizOption', backref='quiz', uselist=True)

    def __init__(self, question):
        self.question = question


class QuizOption(db.Model):

    __tablename__ = 'quiz_option'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    content = db.Column(db.String(100))
    is_answer = db.Column(db.Boolean(), default=False)

    def __init__(self, content, is_answer=False):
        self.content = content
        self.is_answer = is_answer


class LearnRecord(db.Model):

    __tablename__ = 'learn_record'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    star_count = db.Column(db.Integer, default=0)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, lecture, user):
        self.lecture = lecture
        self.user = user
        self.star_count = 0
        self.created = datetime.utcnow()

    def delete(self):
        pass


class Resource(db.Model):

    __tablename__ = 'resource'

    RESOURCE_CATEGORY = ('ppt', 'doc', 'pdf', 'video', 'other')
    RESOURCE_STATE = ('normal', 'deleted')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='resources', uselist=False)
    resource_url = db.Column(db.String(250))
    category = db.Column(db.Enum(name='lecture_state', *RESOURCE_CATEGORY))
    created = db.Column(db.DateTime)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))
    lecture = db.relationship('Lecture', backref='resources', uselist=False)
    _state = db.Column('state', db.Enum(name='resource_state',
                                        *RESOURCE_STATE))
    state = enumdef('_state', RESOURCE_STATE)

    def __init__(self, name):
        self.name = name
        self.created = datetime.utcnow()
        self.category = 'other'
        self.state = 'normal'

    def __repr__(self):
        return "<CourseResource %s>" % self.name

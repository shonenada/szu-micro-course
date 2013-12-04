from datetime import datetime

from flask import url_for

from mooc.app import db
from mooc.account.model import SzuAccount
from mooc.qa.model import Question
from mooc.utils import enumdef


lecture_tags = db.Table(
    'lecture_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('lecture_tag.id')),
    db.Column('lecture_id', db.Integer, db.ForeignKey('lecture.id'))
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
    categorys = db.relationship('Category', backref='subject', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<Subject %s>" % self.name


class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    courses = db.relationship('Course', backref='category', lazy='dynamcic')

    def __init__(self, name, subject):
        self.name = name
        self.subject = subject

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
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    lectures = db.relationship('Lecture',
                               backref=db.backref('course'), uselist=True)
    tags = db.relationship('CourseTag', secondary=course_tags,
                           backref=db.backref('course', lazy='dynamic'))

    def __init__(self, name, description, author, category):
        self.name = name
        self.description = description
        self.author = author
        self.category = category
        self.created = datetime.utcnow()
        self.logo_url = url_for('static',
                                filename='images/default_course_logo.png')

    def set_finished(self):
        self.state = 'finished'

    def set_updating(self):
        self.state = 'updating'

    def set_coming(self):
        self.state = 'coming'

    def __repr__(self):
        return "<Course %s>" % self.name


class Lecture(db.Model):
    """Model of Course"""

    __tablename__ = 'lecture'

    LECTURE_STATE_VALUES = ('published', 'unpublished', 'recording')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    knowledge_point = db.Column(db.Text)
    prepare_knowledge = db.Column(db.Text)
    chapter = db.Column(db.String(512))
    term = db.Column(db.String(512))
    record_time = db.Column(db.DateTime)
    record_address = db.Column(db.String(256))
    upload_time = db.Column(db.DateTime)
    video_url = db.Column(db.String(150))
    video_length = db.Column(db.Integer)
    _state = db.Column('state', db.Enum(name='lecture_state',
                                        *LECTURE_STATE_VALUES))
    state = enumdef('_state', LECTURE_STATE_VALUES)
    read_count = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, default=1)
    play_count = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    learn_records = db.relationship('LearnRecord', backref=db.backref('lecture'),
                                    uselist=True, lazy='dynamic')
    questions = db.relationship('Question', backref=db.backref('lecture'),
                                uselist=True, lazy='dynamic')
    answers = db.relationship('Answer', backref=db.backref('lecture'),
                              uselist=True, lazy='dynamic')
    tags = db.relationship('LectureTag', secondary=lecture_tags,
                           backref=db.backref('lecture'))

    def __init__(self, name, description, author, course, order=None,
                 published=False):
        self.name = name
        self.description = description
        self.author = author
        self.course = course
        self.published = published
        self.video_url = ''
        self.read_count = 0
        self.play_count = 0
        self.video_length = 0
        self.order = order if order else 9999
        self.created = datetime.utcnow()
        self.upload_time = datetime.utcnow()

    def __repr__(self):
        return "<Lecture %s>" % self.name


class Quiz(db.Model):

    __tablename__ = 'quiz'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100))
    time_at = db.Column(db.Integer)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))
    lecture = db.relationship('Lecture',
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


class LectureTag(db.Model):
    __tablename__ = 'lecture_tag'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))


class CourseTag(db.Model):

    __tablename__ = 'course_tag'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))

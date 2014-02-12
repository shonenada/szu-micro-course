from datetime import datetime

from flask import url_for
from sqlalchemy import func, select
from sqlalchemy.ext.hybrid import hybrid_property

from mooc.extensions import db
from mooc.utils.helpers import enumdef
from mooc.models.master import ModelMixin
from mooc.models.account import SzuAccount
from mooc.models.discuss import Question


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


class Subject(db.Model, ModelMixin):

    __tablename__ = 'subject'

    SUBJECT_STATE_VALUES = ('normal', 'deleted')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.Text)
    categories = db.relationship('Category', backref='subject')
    state = db.Column(db.Enum(*SUBJECT_STATE_VALUES), default='normal')

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


class Category(db.Model, ModelMixin):

    __tablename__ = 'category'
    CATEGORY_STATE_VALUES = ('normal', 'deleted')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    courses = db.relationship('Course', backref='category')
    state = db.Column(db.Enum(*CATEGORY_STATE_VALUES), default='normal')

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


class Course(db.Model, ModelMixin):
    """Model of Course"""

    __tablename__ = 'course'

    COURSE_STATE_VALUES = ('finished', 'updating', 'coming', 'deleted')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)
    state = db.Column(db.Enum(*COURSE_STATE_VALUES), default='updating')
    logo_url = db.Column(
        db.String(50),
        default=lambda: url_for('static',
                                filename='images/default_course_logo.png'))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'))
    lectures = db.relationship('Lecture',
                               backref=db.backref('course'), uselist=True)
    tags = db.relationship('Tag', secondary=course_tags,
                           backref=db.backref('courses'))

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


class Lecture(db.Model, ModelMixin):
    """Model of Course"""

    __tablename__ = 'lecture'

    LECTURE_STATE_VALUES = ('published', 'recording', 'coming', 'deleted')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    knowledge_point = db.Column(db.Text)
    prepare_knowledge = db.Column(db.Text)
    term = db.Column(db.String(512))
    chapter = db.Column(db.String(512))
    record_time = db.Column(db.DateTime)
    record_location = db.Column(db.String(256))
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    video_url = db.Column(db.String(150))
    video_length = db.Column(db.Integer)
    logo_url = db.Column(db.String(100))
    state = db.Column(db.Enum(*LECTURE_STATE_VALUES), default='published')
    watch_count = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, default=9999)
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


class Quiz(db.Model, ModelMixin):

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


class QuizOption(db.Model, ModelMixin):

    __tablename__ = 'quiz_option'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    content = db.Column(db.String(100))
    is_answer = db.Column(db.Boolean(), default=False)


class LearnRecord(db.Model, ModelMixin):

    __tablename__ = 'learn_record'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    star_count = db.Column(db.Integer, default=0)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def delete(self):
        pass # Cannot delete.


class Note(db.Model, ModelMixin):

    STATE_VALUES = ('normal', 'deleted')

    __tablename__ = 'note'

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='notes', uselist=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))
    lecture = db.relationship('Lecture', backref='notes', uselist=False)    
    created = db.Column(db.DateTime, default=datetime.utcnow)
    star_count = db.Column(db.Integer, default=0)
    state = db.Column(db.Enum(*STATE_VALUES), default='normal')


class Comment(db.Model, ModelMixin):

    STATE_VALUES = ('normal', 'unverified', 'delete')

    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='comments', uselist=False)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))
    lecture = db.relationship(
        'Lecture',
        backref=db.backref(
            'comments',
            order_by=lambda: Comment.id.desc(),
            lazy='dynamic',
        ),
        uselist=False)
    star_count = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    state = db.Column(db.Enum(*STATE_VALUES), default='normal')

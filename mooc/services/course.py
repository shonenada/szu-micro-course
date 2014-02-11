#-*-coding: utf-8 -*-
from flask import current_app as app

from mooc.extensions import db
from mooc.models.master import Tag
from mooc.models.course import LearnRecord, Lecture
from mooc.models.course import Subject, Category, Course


def get_learn_records():
    app.jinja_env.globals['learn_records'] = \
        LearnRecord.query.order_by(LearnRecord.id.desc()).limit(10).all()


def get_last_lecture():
    app.jinja_env.globals['last_lectures'] = \
        Lecture.query.order_by(Lecture.upload_time.desc()).limit(10).all()


def learn_count(course):
    learn_count = 0
    for lecture in course.lectures:
        learn_count = learn_count + lecture.learn_records.count()
    return learn_count


def quiz_to_json(quizs):
    json_quizs = []
    for q in quizs:
        _q = {}
        _q['id'], _q['question'], _q['time_at'] = q.id, q.question, q.time_at
        _q['options'] = []
        for op in q.options:
            _op = {}
            _op['id'], _op['content'] = op.id, op.content
            _q['options'].append(_op)
        json_quizs.append(_q)
    return json_quizs


def create_subject(data):
    subject = Subject(name=data['name'], description=data['description']).save()


def create_category(data):
    category = Category(name=data['name'], subject=data['subject']).save()


def create_course(data):
    course = Course(
        name=data['name'],
        description=data['description'],
        teacher=data['teacher'],
        category=data['category'],
        college = data['college'],
        logo_url = data['logo_url'],
        tags = data['tags'],
    ).save()


def create_lecture(data):
    lecture = Lecture(
        name=data['name'],
        description=data['description'],
        teacher=data['teacher'],
        course=data['course'],
        order=data['order'],
        prepare_knowledge=data['prepare_knowledge'],
        knowledge_point=data['knowledge_point'],
        chapter=data['chapter'],
        term=data['term'],
        record_time=data['record_time'],
        record_location=data['record_address'],
        video_url=data['video_url'],
        video_length=data['video_length'],
        tags=data['tags'],

    ).save()

#-*-coding: utf-8 -*-
from flask import current_app as app

from mooc.app import db
from mooc.master.model import Tag
from mooc.course.model import LearnRecord, Lecture
from mooc.course.model import Subject, Category, Course, Lecture


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
    subject = Subject(data['name'], data['description'])
    db.session.add(subject)
    db.session.commit()


def create_category(data):
    category = Category(data['name'], data['subject'])
    db.session.add(category)
    db.session.commit()


def create_course(data):
    course = Course(
        data['name'],
        data['description'],
        data['teacher'],
        data['category']
    )
    course.logo_url = data['logo_url']
    course.tags = data['tags']
    db.session.add(course)
    db.session.commit()


def create_lecture(data):
    lecture = Lecture(
        data['name'],
        data['description'],
        data['teacher'],
        data['course'],
        data['order'],
    )
    lecture.prepare_knowledge = data['prepare_knowledge']
    lecture.knowledge_point = data['knowledge_point']
    lecture.chapter = data['chapter']
    lecture.term = data['term']
    lecture.record_time = data['record_time']
    lecture.record_address = data['record_address']
    lecture.video_url = data['video_url']
    lecture.video_length = data['video_length']
    lecture.tags = data['tags']
    db.session.add(lecture)
    db.session.commit()


def friendly_resource_category(category):
    RESOURCE_CATEGORY = {'ppt': '演示文稿',
                         'doc': '文档',
                         'pdf': 'PDF',
                         'video': '视频',
                         'other': '其他'}
    if category in RESOURCE_CATEGORY.keys():
        return RESOURCE_CATEGORY[category]
    else:
        return '其他'

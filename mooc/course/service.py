from flask import current_app as app

from mooc.course.model import LearnRecord, Lecture


def get_learn_records():
    app.jinja_env.globals['learn_records'] = LearnRecord.query.limit(10).all()


def get_last_lecture():
    app.jinja_env.globals['last_lecutres'] = \
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

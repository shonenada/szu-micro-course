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

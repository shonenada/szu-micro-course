from flask import current_app as app

from mooc.course.model import LearnRecord, Clip


def get_learn_records():
    app.jinja_env.globals['learn_records'] = LearnRecord.query.limit(10).all()


def get_last_clip():
    app.jinja_env.globals['last_clips'] = \
        Clip.query.order_by(Clip.upload_time.desc()).limit(10).all()


def learn_count(course):
    learn_count = 0
    for clip in course.clips:
        learn_count = learn_count + clip.learn_records.count()
    return learn_count

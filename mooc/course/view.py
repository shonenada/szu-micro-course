from flask import Blueprint, render_template, abort

from mooc.course.model import Subject, Category, Course, Clip, LearnRecord


course_app = Blueprint('course', __name__, template_folder='../templates')


@course_app.route('/courses')
def courses():
    subjects = Subject.query.all()
    return render_template('courses.html', subjects=subjects)


@course_app.route('/courses/subject/<sid>')
def subject(sid):
    this_subject = Subject.query.get(sid)
    return render_template('subject.html', this_subject=this_subject)


@course_app.route('/courses/subject/<sid>/category/<cid>')
def category(sid, cid):
    this_category = Category.query.get(cid)
    if int(this_category.subject.id) != int(sid):
        abort(404)
    return render_template('category.html', this_category=this_category)


@course_app.route('/course/<course_id>')
def course(course_id):
    this_course = Course.query.get(course_id)
    return render_template('course_list.html', this_course=this_course)


@course_app.route('/lecture/<clip_id>')
def clip(clip_id):
    clip = Clip.query.get(clip_id)
    who_is_learning = LearnRecord.query.filter_by(clip_id=clip_id).limit(10).all()
    return render_template('clip.html', clip=clip, learning=who_is_learning)

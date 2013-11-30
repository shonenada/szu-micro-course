from flask import Blueprint, render_template, abort

from mooc.app import rbac
from mooc.course.model import Subject, Category, Course, Lecture, LearnRecord


course_app = Blueprint('course', __name__, template_folder='../templates')


@course_app.route('/courses')
@rbac.allow(['everyone'], ['GET'])
def courses():
    subjects = Subject.query.all()
    return render_template('courses.html', subjects=subjects)


@course_app.route('/courses/subject/<sid>')
@rbac.allow(['everyone'], ['GET'])
def subject(sid):
    this_subject = Subject.query.get(sid)
    return render_template('subject.html', this_subject=this_subject)


@course_app.route('/courses/subject/<sid>/category/<cid>')
@rbac.allow(['everyone'], ['GET'])
def category(sid, cid):
    this_category = Category.query.get(cid)
    if int(this_category.subject.id) != int(sid):
        abort(404)
    return render_template('category.html', this_category=this_category)


@course_app.route('/course/<course_id>')
@rbac.allow(['everyone'], ['GET'])
def course(course_id):
    this_course = Course.query.get(course_id)
    lectures = (Lecture.query.filter_by(course_id=course_id)
                 .order_by(Lecture.order).all())
    return render_template('course_list.html',
                           this_course=this_course, lectures=lectures)


@course_app.route('/lecture/<lecture_id>')
@rbac.allow(['everyone'], ['GET'])
def lecture(lecture_id):
    lecture = Lecture.query.get(lecture_id)
    who_is_learning = (LearnRecord.query.filter_by(lecture_id=lecture_id)
                                  .limit(10).all())
    return render_template('lecture.html',
                           lecture=lecture, learning=who_is_learning)

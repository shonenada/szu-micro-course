from flask import Blueprint, render_template


course_app = Blueprint('course', __name__, template_folder='../templates')


@course_app.route('/courses')
def courses():
    return render_template('courses.html')


@course_app.route('/courses/subject/<sid>')
def subject(sid):
    return render_template('subject.html')


@course_app.route('/courses/subject/<sid>/category/<cid>')
def category(sid, cid):
    return render_template('category.html');


@course_app.route('/course/<course_id>')
def course(course_id):
    return render_template('course_list.html')


@course_app.route('/lecture/<clip_id>')
def clip(clip_id):
    return render_template('clip.html')

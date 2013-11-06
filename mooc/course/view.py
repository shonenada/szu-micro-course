from flask import Blueprint, render_template


course_app = Blueprint('course', __name__, template_folder='../templates')


@course_app.route('/courses')
def courses():
    return render_template('courses.html')


@course_app.route('/courses/category/<id>')
def category(id):
    return render_template('category.html');

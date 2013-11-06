from flask import Blueprint, render_template


course_app = Blueprint('course', __name__, template_folder='../templates')


@course_app.route('/courses')
def courses():
    return render_template("course_list.html")

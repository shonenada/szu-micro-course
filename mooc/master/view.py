from flask import Blueprint, render_template

from mooc.course.model import Subject


master_app = Blueprint('master', __name__, template_folder='../templates')


@master_app.route('/')
def index():
    subjects = Subject.query.all()
    return render_template("index.html", subjects=subjects)

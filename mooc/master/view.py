from flask import Blueprint, render_template, flash

from mooc.app import rbac
from mooc.course.model import Subject


master_app = Blueprint('master', __name__, template_folder='../templates')


@master_app.route('/')
@rbac.allow(['everyone'], ['GET'])
def index():
    subjects = Subject.query.all()
    return render_template('index.html', subjects=subjects)


@master_app.route('/master')
@rbac.allow(['super_admin'], ['GET'])
def master_index():
    return render_template('admin/index.html')

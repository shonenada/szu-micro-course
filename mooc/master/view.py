from flask import Blueprint, render_template, flash, request

from mooc.app import rbac
from mooc.account.model import User
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


@master_app.route('/master/account')
@rbac.allow(['super_admin'], ['GET'])
def master_account_list():
    page_num = int(request.args.get('page', 1))
    user_query = User.query.filter(User.state!='deleted')
    user_pagination = user_query.paginate(page_num, per_page=20)
    return render_template('admin/account_list.html', user_pagination=user_pagination)

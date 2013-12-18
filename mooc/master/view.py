from flask import Blueprint, render_template, current_app
from flask import request, redirect, url_for, jsonify

from mooc.app import rbac, db
from mooc.utils import flash
from mooc.account.model import User, SzuAccount, College
from mooc.course.model import Subject, Category, Course, Lecture
from mooc.course.form import SubjectForm, CategoryForm, CourseForm, LectureForm
from mooc.account.form import UserForm, SzuAccountForm, NewUserForm
from mooc.master.utils import generate_all_controller
from mooc.master.service import common_paginate, common_delete
from mooc.account.service import update_user_state,\
                                 change_user_password,\
                                 create_user
from mooc.course.service import create_subject, create_category,\
                                create_course, create_lecture


master_app = Blueprint('master', __name__, template_folder='../templates')


generate_all_controller(master_app, Subject, SubjectForm, create_subject)
generate_all_controller(master_app, Category, CategoryForm, create_category)
generate_all_controller(master_app, Course, CourseForm, create_course)
generate_all_controller(master_app, Lecture, LectureForm, create_lecture)


@master_app.route('/')
@rbac.allow(['everyone'], ['GET'])
def index():
    subjects = Subject.query.filter(Subject._state != 'deleted').all()
    return render_template('index.html', subjects=subjects)


@master_app.route('/master')
@rbac.allow(['super_admin'], ['GET'])
def master_index():
    return render_template('admin/index.html')


@master_app.route('/master/account')
@rbac.allow(['super_admin'], ['GET'])
def master_account_list():
    page_num = int(request.args.get('page', 1))
    pagination = common_paginate(
        model = User,
        page = page_num,
        per_page = current_app.config.get('ADMIN_PAGESIZE')
    )
    return render_template('admin/account_list.html', pagination=pagination)


@master_app.route('/master/account/<int:uid>/edit', methods=['GET', 'PUT'])
@rbac.allow(['super_admin'], ['GET', 'PUT'])
def master_account_edit(uid):
    user = User.query.get(uid)
    user_form = UserForm(request.form, user)
    szu_account_form = SzuAccountForm(request.form, user.szu_account)
    if user_form.validate_on_submit():
        update_user_state(uid, user_form.data['state'])
        flash('Operated successfully!', 'notice')
        return jsonify(success=True)
    if user_form.errors:
        flash(message=user_form.errors, category='error', form_errors=True)
        return jsonify(success=False)
    return render_template('admin/account_edit.html', uid=uid,
                           user_form=user_form,
                           szu_account_form=szu_account_form)


@master_app.route('/master/account/<int:uid>', methods=['DELETE'])
@rbac.allow(['super_admin'], ['DELETE'])
def master_account_delete(uid):
    common_delete(User, uid)
    flash(message='Operated successfully!', category='notice')
    return jsonify(success=True)


@master_app.route('/master/account/<int:uid>/password', methods=['PUT'])
@rbac.allow(['super_admin'], ['PUT'])
def master_account_password(uid):
    raw_passwd = request.form['password']
    change_user_password(uid, raw_passwd)
    flash(message='Operated successfully', category='notice')
    return jsonify(success=True)


@master_app.route('/master/account/new_user', methods=['GET', 'POST'])
@rbac.allow(['super_admin'], ['GET', 'POST'])
def master_account_new():
    new_user_form = NewUserForm(request.form)
    if new_user_form.validate_on_submit():
        data = new_user_form.data
        create_user(data)
        flash(message='Operated successfully', category='notice')
        return jsonify(success=True)
    return render_template('admin/account_new.html', form=new_user_form)

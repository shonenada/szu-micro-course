from flask import Blueprint, render_template
from flask import request, redirect, url_for, jsonify

from mooc.app import rbac, db, csrf
from mooc.utils import flash
from mooc.account.model import User
from mooc.course.model import Subject
from mooc.master.form import MasterUserForm, MasterSzuAccountForm


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
    return render_template('admin/account_list.html',
                           user_pagination=user_pagination)


@master_app.route('/master/account/<int:uid>/edit', methods=['GET', 'PUT'])
@rbac.allow(['super_admin'], ['GET', 'PUT'])
def master_account_edit(uid):
    user = User.query.get(uid)
    user_form = MasterUserForm(request.form, user)
    szu_account_form = MasterSzuAccountForm(request.form, user.szu_account)
    if user_form.validate_on_submit():
        user.state = user_form.data['state']
        db.session.add(user)
        db.session.commit()
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
    user = User.query.get(uid)
    user.state = 'deleted'
    db.session.add(user)
    db.session.commit()
    flash(message='Operated successfully!', category='notice')
    return jsonify(success=True)

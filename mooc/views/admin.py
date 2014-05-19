from flask import Blueprint, render_template
from flask import request, jsonify
from flask.ext.babel import lazy_gettext as _

from mooc.extensions import rbac
from mooc.utils.helpers import flash
from mooc.utils.admin import generate_all_controller
from mooc.models.master import Feedback
from mooc.models.account import User
from mooc.models.course import Subject, Category, Course, Lecture
from mooc.models.resource import Resource
from mooc.forms.course import SubjectForm, CategoryForm, CourseForm, LectureForm
from mooc.forms.resource import ResourceForm
from mooc.forms.account import ManageUserForm, CreateUserForm
from mooc.services.account import (update_user_state,
                                    change_user_password,
                                    create_user)
from mooc.services.course import (create_subject, create_category,
                                  create_course, create_lecture)
from mooc.services.resource import create_resource


admin_app = Blueprint('admin', __name__, url_prefix='/admin')

controllers_args = [
    {'model': Subject,
     'form_model': SubjectForm,
     'create_method': create_subject,
    },
    {'model': Category,
     'form_model': CategoryForm,
     'create_method':create_category,
    },
    {'model': Course,
     'form_model': CourseForm,
     'create_method':create_course,
    },
    {'model': Lecture,
     'form_model': LectureForm,
     'create_method':create_lecture,
    },
    {'model': Resource,
     'form_model': ResourceForm,
     'create_method':create_resource,
    },
]

for args in controllers_args:
    generate_all_controller(
        blueprint=admin_app,
        model=args.get('model'),
        form_model=args.get('form_model'),
        create_method=args.get('create_method')
    )


@admin_app.route('')
@rbac.allow(['super_admin'], ['GET'])
def index():
    return render_template('admin/index.html')


@admin_app.route('/account')
@rbac.allow(['super_admin'], ['GET'])
def list_account():
    page_num = int(request.args.get('page', 1))
    pagination = User.paginate(page=page_num)
    return render_template('admin/account/list.html', pagination=pagination)


@admin_app.route('/account/<int:uid>/edit', methods=['GET', 'PUT'])
@rbac.allow(['super_admin'], ['GET', 'PUT'])
def edit_account(uid):
    user = User.query.get(uid)
    data = {
        'card_num': user.szu_account.card_num,
        'stu_number': user.szu_account.stu_number,
        'short_phone': user.szu_account.short_phone,
    }
    user_form = ManageUserForm(request.form, user, **data)

    if user_form.validate_on_submit():
        update_user_state(uid, user_form.data['state'])
        flash(_('Operated successfully'), 'notice')
        return jsonify(success=True)

    if user_form.errors:
        flash(message=user_form.errors, category='error', form_errors=True)
        return jsonify(success=False)

    return render_template(
        'admin/account/edit.html',
        uid=uid, 
        user_form=user_form)


@admin_app.route('/account/<int:uid>', methods=['DELETE'])
@rbac.allow(['super_admin'], ['DELETE'])
def delete_account(uid):
    user = User.query.get(uid)
    user.delete()
    flash(message=_('Operated successfully'), category='notice')
    return jsonify(success=True)


@admin_app.route('/account/<int:uid>/password', methods=['PUT'])
@rbac.allow(['super_admin'], ['PUT'])
def account_password(uid):
    raw_passwd = request.form['password']
    change_user_password(uid, raw_passwd)
    flash(message=_('Operated successfully'), category='notice')
    return jsonify(success=True)


@admin_app.route('/account/create_user', methods=['GET', 'POST'])
@rbac.allow(['super_admin'], ['GET', 'POST'])
def create_account():
    new_user_form = CreateUserForm(request.form)
    if new_user_form.validate_on_submit():
        data = new_user_form.data
        create_user(data)
        flash(message=_('Operated successfully'), category='notice')
        return jsonify(success=True)
    return render_template('admin/account/create.html', form=new_user_form)


@admin_app.route('/feedback', methods=['GET'])
@rbac.allow(['super_admin'], ['GET'])
def list_feedback():
    page = int(request.args.get('page', 1))
    pagination = Feedback.paginate(page=page)
    return render_template('admin/feedback/list.html',
                           pagination=pagination)


@admin_app.route('/feedback/<mid>/delete', methods=['DELETE'])
@rbac.allow(['super_admin'], ['DELETE'])
def delete_feedback(mid):
    feedback = Feedback.query.get_or_404(mid)
    feedback.delete()
    flash(message=_('Operated successfully'), category='notice')
    return jsonify(success=True)

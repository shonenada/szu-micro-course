#-*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template, request, url_for, redirect
from flask.ext.login import login_user, logout_user, current_user

from mooc.app import rbac, csrf, db
from mooc.utils import flash
from mooc.account.model import User
from mooc.account.form import SignInForm, SettingForm
from mooc.account.service import load_user


account_app = Blueprint('account', __name__, template_folder='../templates')


@csrf.exempt
@account_app.route('/signin', methods=['GET', 'POST'])
@rbac.allow(['everyone'], ['GET', 'POST'])
def signin():
    if not current_user.is_anonymous():
        return redirect(url_for('master.index'))
    form = SignInForm()
    if form.validate_on_submit():
        username = request.form['username'].strip()
        raw_passwd = request.form['password'].strip()
        is_remember_me = request.form.get('remember_me', 'f') == 'y'
        user = User.query.authenticate(username, raw_passwd)
        if user:
            login_user(user, force=True, remember=is_remember_me)
            flash(u'登录成功, %s 欢迎' % user.username, 'notice')
            return redirect(url_for('master.index'))
        else:
            flash(u'帐号或密码错误', 'warn')
            return redirect(url_for('account.signin'))
    if form.errors:
        flash(message=form.errors, category='warn', form_errors=True)
    return render_template('account/sign-in.html', form=form)


@account_app.route('/forgot')
def forgot_password():
    return render_template('account/forgot.html')


@account_app.route('/logout')
@rbac.allow(['everyone'], ['GET'])
def signout():
    logout_user()
    flash(u'退出成功', 'notice')
    return redirect(url_for('master.index'))


@account_app.route('/people/<username>')
@rbac.allow(['local_user'], ['GET'])
def people(username):
    pass


@csrf.exempt
@account_app.route('/account/setting', methods=['GET', 'POST'])
@rbac.allow(['local_user'], ['GET', 'POST'])
def setting():
    user = current_user
    form = SettingForm(request.form, user)
    if form.validate_on_submit():
        form.populate_obj(user)
        user.is_male = user.is_male == 'True'
        db.session.add(user)
        db.session.commit()
        flash(message=u'修改成功', category='notice')
    if form.errors:
        flash(message=form.errors, category='warn', form_errors=True)
    return render_template('account/setting.html', user=user, form=form)

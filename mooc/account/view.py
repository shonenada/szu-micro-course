#-*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template, request, url_for, redirect
from flask.ext.login import login_user, logout_user, current_user

from mooc.utils import flash
from mooc.account.model import User
from mooc.account.form import SignInForm
from mooc.account.service import load_user


account_app = Blueprint('account', __name__, template_folder='../templates')


@account_app.route('/signin', methods=['GET', 'POST'])
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
def signout():
    logout_user()
    flash(u'退出成功', 'notice')
    return redirect(url_for('master.index'))


@account_app.route('/people/<int:uid>')
def people(uid):
    pass


@account_app.route('/setting/account')
def setting():
    pass

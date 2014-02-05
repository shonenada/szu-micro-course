#-*- coding: utf-8 -*-
from flask import Blueprint, abort
from flask import render_template, request, url_for, redirect
from flask.ext.babel import lazy_gettext as _, gettext
from flask.ext.login import login_user, logout_user, current_user

from mooc.extensions import rbac, csrf, db
from mooc.utils.helpers import flash, get_avatar_url, jsonify
from mooc.models.account import User, SzuAccount, Role
from mooc.forms.account import SignInForm, SettingForm, PasswordForm, SignUpForm


account_app = Blueprint('account', __name__, url_prefix='/account')


@csrf.exempt
@account_app.route('/signin', methods=['GET', 'POST'])
@rbac.allow(['anonymous'], ['GET', 'POST'])
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
            return jsonify(
                success=True,
                messages=[
                    gettext('Logged in successfully, Welcome %(username)s',
                    username=user.nickname or user.username)
                ]
            )

        else:
            return jsonify(
                success=False,
                messages=[gettext('Wrong username or password')]
            )

    if form.errors:
        return jsonify(success=False, errors=True, messages=form.errors)

    return render_template('account/signin.html', form=form)


@csrf.exempt
@account_app.route('/signup', methods=['GET', 'POST'])
@rbac.allow(['anonymous'], methods=['GET', 'POST'])
def signup():
    if not current_user.is_anonymous():
        return redirect(url_for('master.index'))

    form = SignUpForm(request.form)

    if form.validate_on_submit():
        username = form.data['username']
        stu_number = form.data['stu_number']
        nickname = form.data['nickname']

        local_user = Role.query.filter_by(name='local_user').first()

        user = User(
            username=username,
            passwd=form.data['password'],
            is_male=(form.data['is_male']=='True'),
            name=form.data['name'],
            nickname=nickname,
        )
        user.roles.append(local_user)

        szu_account = SzuAccount(stu_number=stu_number)
        user.szu_account = szu_account

        szu_account.save()
        user.save()

        return jsonify(
                success=True,
                messages=[
                    gettext('Sign up successfully')
                ]
            )

    if form.errors:
        return jsonify(success=False, errors=True, messages=form.errors)

    return render_template('account/signup.html', form=form)


@account_app.route('/forgot')
def forgot_password():
    return render_template('account/forgot.html')


@account_app.route('/logout')
@rbac.allow(['anonymous'], ['GET'])
def signout():
    logout_user()
    flash(_('Logged out successfully.'), 'notice')
    return redirect(url_for('master.index'))


@account_app.route('/<username>')
@rbac.allow(['anonymous'], ['GET'])
def people(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    else:
        avatar = get_avatar_url(user.email)
        get_type = SzuAccount.get_type
        return render_template('account/people.html',
                               user=user, avatar=avatar, get_type=get_type)


@csrf.exempt
@account_app.route('/setting', methods=['GET', 'POST'])
@rbac.allow(['local_user'], ['GET', 'POST'])
def setting():
    user = current_user
    data = {'college': user.szu_account.college,
            'card_id': user.szu_account.card_id,
            'stu_number': user.szu_account.stu_number,
            'short_phone': user.szu_account.short_phone}
    form = SettingForm(
        formdata=request.form,
        obj=user,
        **data
    )

    if form.validate_on_submit():
        form.populate_obj(user)
        form.populate_obj(user.szu_account)
        user.is_male = user.is_male == 'True'
        user.save()
        user.szu_account.save()

        return jsonify(
                success=True,
                messages=[
                    gettext('Modified successfully.')
                ],
                next=url_for('account.setting')
            )

    if form.errors:
        return jsonify(success=False, errors=True, messages=form.errors)

    return render_template('account/setting.html', user=user, form=form)


@csrf.exempt
@account_app.route('/password', methods=['GET', 'POST'])
@rbac.allow(['local_user'], ['GET', 'POST'])
def change_password():
    form = PasswordForm(formdata=request.form)

    if form.validate_on_submit():
        user = current_user
        if not user.check_password(form.data.get('old_password')):

            return jsonify(
                    success=False,
                    messages=[
                        gettext('Wrong old password')
                    ]
                )

        user.change_password(form.data.get('new_password'))
        user.save()

        return jsonify(
                success=True,
                messages=[
                    gettext('Modified successfully.')
                ],
                next=url_for('account.change_password')
            )

    if form.errors:
        return jsonify(success=False, errors=True, messages=form.errors)

    return render_template('account/change_password.html', form=form)

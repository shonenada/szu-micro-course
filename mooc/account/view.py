from flask import Blueprint
from flask import render_template, request, url_for, redirect, jsonify
from flask.ext.login import login_user, current_user

from mooc.account.model import User


account_app = Blueprint('account', __name__, template_folder='../templates')


@account_app.route('/signin', methods=['GET'])
def signin():
    if current_user:
        return redirect(url_for('master.index'))
    return render_template('account/sign-in.html')


@account_app.route('/signin', methods=['POST'])
def do_signin():
    username = request.form['username']
    raw_passwd = request.form['password']
    user = User.query.authenticate(username, raw_passwd)
    if user:
        login_user(user)
        return redirect(url_for('master.index'))
    else:
        return 'Wrong'


@account_app.route('/forgot')
def forgot_password():
    return render_template('account/forgot.html')

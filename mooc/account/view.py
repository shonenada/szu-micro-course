from flask import Blueprint
from flask import render_template, request, url_for, redirect, jsonify

from mooc.account.model import User
from mooc.account.service import login


account_app = Blueprint('account', __name__, template_folder='../templates')


@account_app.route('/signin', methods=['GET'])
def signin():
    return render_template('account/sign-in.html')


@account_app.route('/signin', methods=['POST'])
def do_signin():
    username = request.form['username']
    raw_passwd = request.form['password']
    user = User.query.authenticate(username, raw_passwd)
    if user:
        login(user)
        return redirect(url_for('master.index'))
    else:
        return 'Wrong'


@account_app.route('/forgot')
def forgot_password():
    return render_template('account/forgot.html')

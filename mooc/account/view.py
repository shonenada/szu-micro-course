from flask import Blueprint, render_template, request

from mooc.account.service import do_signin


account_app = Blueprint('account', __name__, template_folder='../templates')


@account_app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('account/sign-in.html')
    elif request.method == 'POST':
        do_signin()


@account_app.route('/forgot')
def forgot_password():
    return render_template('account/forgot.html')

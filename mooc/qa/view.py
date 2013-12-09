from flask import Blueprint, render_template

from mooc.app import db, rbac


qa_app = Blueprint('qa', __name__, template_folder='../templates')


@qa_app.route('/question')
@rbac.allow(['everyone'], ['GET'])
def question():
    return render_template('qa/index.html')

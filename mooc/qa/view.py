from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import Pagination

from mooc.app import db, rbac
from mooc.qa.model import Question, Answer


qa_app = Blueprint('qa', __name__, template_folder='../templates')


@qa_app.route('/question')
@rbac.allow(['everyone'], ['GET'])
def question():
    return redirect(url_for('qa.lastest'))


@qa_app.route('/question/lastest')
@rbac.allow(['everyone'], ['GET'])
def lastest():
    page_num = int(request.args.get('page', 1))
    question_query = (Question.query.filter(Question._state != 'DELETED')
                              .order_by(Question.created.desc()))
    questions = question_query.paginate(page_num, per_page=20)
    return render_template('qa/question_list.html',
                           question_pagination=questions, type='lastest')


@qa_app.route('/question/hotest')
@rbac.allow(['everyone'], ['GET'])
def hotest():
    page_num = int(request.args.get('page', 1))
    question_query = (Question.query.filter(Question._state != 'DELETED')
                              .order_by(Question.rank.desc()))
    questions = question_query.paginate(page_num, per_page=20)
    return render_template('qa/question_list.html',
                           question_pagination=questions, type='hotest')

from sqlalchemy import func, select
from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import Pagination

from mooc.app import db, rbac
from mooc.qa.model import Question, Answer, QuestionTag


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
    hotest_tags = QuestionTag.query.order_by(QuestionTag.count.desc()).all()
    return render_template('qa/question_list.html', hotest_tags=hotest_tags,
                           question_pagination=questions, type='lastest')


@qa_app.route('/question/hotest')
@rbac.allow(['everyone'], ['GET'])
def hotest():
    page_num = int(request.args.get('page', 1))
    question_query = (Question.query.filter(Question._state != 'DELETED')
                              .order_by(Question.hotest.desc()))
    questions = question_query.paginate(page_num, per_page=20)
    return render_template('qa/question_list.html',
                           question_pagination=questions, type='hotest')


@qa_app.route('/question/noanswer')
@rbac.allow(['everyone'], ['GET'])
def noanswer():
    page_num = int(request.args.get('page', 1))
    question_query = (Question.query.filter(Question._state != 'DELETED')
                              .filter(Question.answer_count == 0))
    questions = question_query.paginate(page_num, per_page=20)
    return render_template('qa/question_list.html',
                           question_pagination=questions, type='noanswer')


@qa_app.route('/question/<int:qid>')
@rbac.allow(['everyone'], ['GET'])
def view_question(qid):
    question = Question.query.get(qid)
    return render_template('qa/question.html', question=question)

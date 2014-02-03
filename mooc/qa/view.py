from sqlalchemy import func, select
from flask import Blueprint, render_template, request
from flask import jsonify, redirect, url_for
from flask.ext.babel import lazy_gettext as _
from flask.ext.sqlalchemy import Pagination
from flask.ext.login import current_user

from mooc.app import db, rbac
from mooc.course.model import Lecture
from mooc.qa.model import Question, Answer, QuestionTag, UpDownRecord
from mooc.qa.form import AskForm


qa_app = Blueprint('qa', __name__, url_prefix='/discuss')


@qa_app.route('/question')
@rbac.allow(['anonymous'], ['GET'])
def question():
    return redirect(url_for('qa.lastest'))


@qa_app.route('/question/lastest')
@rbac.allow(['anonymous'], ['GET'])
def lastest():
    page_num = int(request.args.get('page', 1))
    question_query = (Question.query.filter(Question._state != 'DELETED')
                              .order_by(Question.created.desc()))
    questions = question_query.paginate(page_num, per_page=20)
    hotest_tags = QuestionTag.query.order_by(QuestionTag.count.desc()).all()
    return render_template('qa/question_list.html', hotest_tags=hotest_tags,
                           question_pagination=questions, type='lastest')


@qa_app.route('/question/hotest')
@rbac.allow(['anonymous'], ['GET'])
def hotest():
    page_num = int(request.args.get('page', 1))
    question_query = (Question.query.filter(Question._state != 'DELETED')
                              .order_by(Question.hotest.desc()))
    questions = question_query.paginate(page_num, per_page=20)
    hotest_tags = QuestionTag.query.order_by(QuestionTag.count.desc()).all()
    return render_template('qa/question_list.html', hotest_tags=hotest_tags,
                           question_pagination=questions, type='hotest')


@qa_app.route('/question/noanswer')
@rbac.allow(['anonymous'], ['GET'])
def noanswer():
    page_num = int(request.args.get('page', 1))
    question_query = (Question.query.filter(Question._state != 'DELETED')
                              .filter(Question.answer_count == 0))
    questions = question_query.paginate(page_num, per_page=20)
    hotest_tags = QuestionTag.query.order_by(QuestionTag.count.desc()).all()
    return render_template('qa/question_list.html', hotest_tags=hotest_tags,
                           question_pagination=questions, type='noanswer')


@qa_app.route('/question/<int:qid>')
@rbac.allow(['anonymous'], ['GET'])
def view_question(qid):
    question = Question.query.get(qid)
    question.read_count += 1
    db.session.add(question)
    db.session.commit()
    return render_template('qa/question.html', question=question)


@qa_app.route('/question/vote', methods=['POST'])
@rbac.allow(['local_user'], ['POST'])
def vote_answer():
    VALID_ACTION = ('up', 'down')
    aid = int(request.form.get('aid', None))
    action = request.form.get('action', None)
    if not (aid or action in VALID_ACTION):
        return jsonify(success=False, message=_('Error params'))

    answer = Answer.query.get(aid)
    if not answer:
        return jsonify(success=False, message=_('Error params'))

    record = (UpDownRecord.query
              .filter(UpDownRecord.user_id == current_user.id)
              .filter(UpDownRecord.answer == answer).first())

    if record:
        return jsonify(success=False, message=_('You have voted!'))

    vote_type = (UpDownRecord.TYPE_DOWN
                 if action == 'down' else UpDownRecord.TYPE_UP)
    vote_record = UpDownRecord(current_user, vote_type)
    vote_record.answer = answer
    answer.up_count += (1 if action == 'down' else -1)
    db.session.add(answer)
    db.session.add(vote_record)
    db.session.commit()
    return jsonify(success=True, message=_('Success'))


@qa_app.route('/question/<int:qid>/answer', methods=['POST'])
@rbac.allow(['local_user'], ['POST'])
def answer(qid):
    question = Question.query.get(qid)
    answer_text = request.form.get('answer', None)
    if not answer_text:
        return jsonify(success=False, message=_('Please answer the question'))
    answer = Answer(answer_text, question, current_user)
    db.session.add(answer)
    db.session.commit()
    return jsonify(success=True)


@qa_app.route('/question/ask', methods=['GET', 'POST'])
@rbac.allow(['local_user'], ['GET', 'POST'])
def ask():
    form = AskForm()
    if request.method == 'GET':
        return render_template('qa/ask.html', form=form)

    if form.validate_on_submit():
        title = form.data.get('title')
        content = form.data.get('content')
        tags = form.data.get('tags')
        new_question = Question(title, content, None, current_user)
        lecture_id = request.args.get('lecture_id', None)
        if lecture_id:
            lecture = Lecture.query.get(lecture_id)
            new_question.lecture = lecture
        db.session.add(new_question)
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False, message=form.errors.values())


@qa_app.route('/tag/<tag>')
@rbac.allow(['anonymous'], ['GET'])
def tag(tag):
    hotest_tags = QuestionTag.query.order_by(QuestionTag.count.desc()).all()
    tags = tag.split(' ')
    questions = set()
    for t in tags:
        this_tags = QuestionTag.query.filter_by(tag=t).all()
        for l_tag in this_tags:
            questions.update(l_tag.questions)
    return render_template('qa/tag_view.html', hotest_tags=hotest_tags,
                           questions=questions, tag=tag)

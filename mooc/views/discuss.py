from sqlalchemy import func, select
from flask import Blueprint, render_template, request
from flask import jsonify, redirect, url_for
from flask.ext.babel import lazy_gettext as _, gettext
from flask.ext.sqlalchemy import Pagination
from flask.ext.login import current_user

from mooc.extensions import rbac, db
from mooc.models.course import Lecture
from mooc.models.discuss import Question, Answer, QuestionTag, UpDownRecord
from mooc.forms.discuss import AskForm


discuss_app = Blueprint('discuss', __name__, url_prefix='/discuss')


@discuss_app.route('/question')
@rbac.allow(['anonymous'], ['GET'])
def question():
    return redirect(url_for('discuss.lastest'))


@discuss_app.route('/question/lastest')
@rbac.allow(['anonymous'], ['GET'])
def lastest():
    page_num = int(request.args.get('page', 1))
    question_query = (Question.query.filter(Question.state != 'DELETED')
                              .order_by(Question.created.desc()))
    questions = question_query.paginate(page_num, per_page=20)
    hotest_tags = QuestionTag.query.order_by(QuestionTag.count.desc()).all()
    return render_template(
        'discuss/question_list.html',
        hotest_tags=hotest_tags,
        question_pagination=questions,
        type='lastest'
    )


@discuss_app.route('/question/hotest')
@rbac.allow(['anonymous'], ['GET'])
def hotest():
    page_num = int(request.args.get('page', 1))
    question_query = (Question.query.filter(Question.state != 'DELETED')
                              .order_by(Question.hotest.desc()))
    questions = question_query.paginate(page_num, per_page=20)
    hotest_tags = QuestionTag.query.order_by(QuestionTag.count.desc()).all()
    return render_template(
        'discuss/question_list.html',
        hotest_tags=hotest_tags,
        question_pagination=questions,
        type='hotest'
    )


@discuss_app.route('/question/noanswer')
@rbac.allow(['anonymous'], ['GET'])
def noanswer():
    page_num = int(request.args.get('page', 1))
    question_query = (Question.query.filter(Question.state != 'DELETED')
                              .filter(Question.answer_count == 0))
    questions = question_query.paginate(page_num, per_page=20)
    hotest_tags = QuestionTag.query.order_by(QuestionTag.count.desc()).all()
    return render_template(
        'discuss/question_list.html',
        hotest_tags=hotest_tags,
        question_pagination=questions,
        type='noanswer',
    )


@discuss_app.route('/question/<int:qid>')
@rbac.allow(['anonymous'], ['GET'])
def view_question(qid):
    question = Question.query.get(qid)
    hotest_tags = QuestionTag.query.order_by(QuestionTag.count.desc()).all()
    answers = (Answer.query.filter(Answer.question==question)
                           .order_by(Answer.like_count.desc())
                           .order_by(Answer.created.desc())
                           .all())
    question.read_count += 1
    question.save()

    if not current_user.is_anonymous():
        records = current_user.up_down_records
        ups = [up.answer for up in records if up.up_or_down == UpDownRecord.TYPE_UP]
        downs = [d.answer for d in records if d.up_or_down == UpDownRecord.TYPE_DOWN]
    else:
        ups = []
        downs = []

    return render_template(
        'discuss/question.html',
        hotest_tags=hotest_tags,
        question=question,
        answers=answers,
        ups=ups,
        downs=downs,
    )


@discuss_app.route('/question/vote', methods=['POST'])
@rbac.allow(['local_user'], ['POST'])
def vote_answer():
    VALID_ACTION = ('up', 'down')
    aid = int(request.form.get('aid', None))
    action = request.form.get('action', None)
    if not (aid or action in VALID_ACTION):
        return jsonify(success=False, message=gettext('Error params'))

    answer = Answer.query.get(aid)
    if not answer:
        return jsonify(success=False, message=gettext('Error params'))

    record = (UpDownRecord.query
              .filter(UpDownRecord.user_id == current_user.id)
              .filter(UpDownRecord.answer == answer).first())

    if record:
        return jsonify(success=False, message=gettext('You have voted!'))

    vote_type = (UpDownRecord.TYPE_DOWN
                 if action == 'down' else UpDownRecord.TYPE_UP)
    vote_record = UpDownRecord(current_user, vote_type)
    vote_record.answer = answer
    if action == 'up':
        answer.up_count += 1
    elif action == 'down':
        answer.down_count += 1

    answer.save(commit=False)
    vote_record.save(commit=False)
    db.session.commit()
    return jsonify(success=True, message=gettext('Success'))


@discuss_app.route('/question/<int:qid>/answer', methods=['POST'])
@rbac.allow(['local_user'], ['POST'])
def answer(qid):
    question = Question.query.get(qid)
    answer_text = request.form.get('answer', None)
    if not answer_text:
        return jsonify(success=False, message=_('Please answer the question'))
    answer = Answer(
        content=answer_text,
        question=question,
        author=current_user)
    db.session.add(answer)
    db.session.commit()
    return jsonify(success=True)


@discuss_app.route('/post', methods=['GET', 'POST'])
@rbac.allow(['local_user'], ['GET', 'POST'])
def post():
    form = AskForm()

    lecture_id = int(request.args.get('lid', 0))
    lecture = Lecture.query.get(lecture_id)

    if form.validate_on_submit():
        title = form.data.get('title')
        content = form.data.get('content')
        tags = form.data.get('tags')
        new_question = Question(
            title=title,
            content=content,
            author=current_user
        )

        if lecture:
            new_question.lecture = lecture

        new_question.save()

        return jsonify(
            success=True,
            messages=[gettext('Submited successfully')],
            next=url_for('discuss.view_question', qid=new_question.id) if new_question.id else '',
        )
    
    if form.errors:
        return jsonify(success=False, errors=True, messages=form.errors)
    
    hotest_tags = QuestionTag.query.order_by(QuestionTag.count.desc()).all()
    return render_template('discuss/post.html', lecture=lecture,
                           form=form, hotest_tags=hotest_tags)


@discuss_app.route('/tag/<tag>')
@rbac.allow(['anonymous'], ['GET'])
def tag(tag):
    hotest_tags = QuestionTag.query.order_by(QuestionTag.count.desc()).all()
    tags = tag.split(' ')
    questions = set()
    for t in tags:
        this_tags = QuestionTag.query.filter_by(tag=t).all()
        for l_tag in this_tags:
            questions.update(l_tag.questions)
    return render_template('discuss/tag_view.html', hotest_tags=hotest_tags,
                           questions=questions, tag=tag)

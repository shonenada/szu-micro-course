#-*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, json, request, jsonify

from mooc.app import rbac, csrf
from mooc.master.model import Tag
from mooc.course.model import Subject, Category, Course, Lecture, LearnRecord
from mooc.course.model import Quiz, QuizOption
from mooc.course.service import quiz_to_json


course_app = Blueprint('course', __name__, template_folder='../templates')


@course_app.route('/courses')
@rbac.allow(['everyone'], ['GET'])
def courses():
    subjects = Subject.query.all()
    return render_template('course/courses.html', subjects=subjects)


@course_app.route('/courses/subject/<sid>')
@rbac.allow(['everyone'], ['GET'])
def subject(sid):
    this_subject = Subject.query.get(sid)
    return render_template('course/subject.html', this_subject=this_subject)


@course_app.route('/courses/subject/<sid>/category/<cid>')
@rbac.allow(['everyone'], ['GET'])
def category(sid, cid):
    this_category = Category.query.get(cid)
    if int(this_category.subject.id) != int(sid):
        abort(404)
    return render_template('course/category.html', this_category=this_category)


@course_app.route('/course/<course_id>')
@rbac.allow(['everyone'], ['GET'])
def course(course_id):
    this_course = Course.query.get(course_id)
    lectures = (Lecture.query.filter_by(course_id=course_id)
                 .order_by(Lecture.order).all())
    return render_template('course/course_list.html',
                           this_course=this_course, lectures=lectures)


@course_app.route('/lecture/<lecture_id>')
@rbac.allow(['everyone'], ['GET'])
def lecture(lecture_id):
    lecture = Lecture.query.get(lecture_id)
    who_is_learning = (LearnRecord.query.filter_by(lecture_id=lecture_id)
                                  .limit(10).all())
    quizs = (Quiz.query.filter_by(lecture_id=lecture_id)
                 .order_by(Quiz.order.desc()).order_by(Quiz.id.desc()))
    return render_template('course/lecture.html', quizs=quizs,
                           lecture=lecture, learning=who_is_learning)


@course_app.route('/lecture/<lecture_id>/questions')
@rbac.allow(['everyone'], ['GET'])
def lecture_quretions(lecture_id):
    _quizs = (Quiz.query.filter_by(lecture_id=lecture_id)
                  .filter(Quiz.time_at != 0).all())
    quizs = quiz_to_json(_quizs)
    return json.dumps(quizs)


@course_app.route('/lecture/<lecture_id>/check', methods=['POST'])
@rbac.allow(['everyone'], ['POST'])
@csrf.exempt
def lecture_check(lecture_id):
    quiz_id = request.form.get('quiz_id', None)
    answer_id = request.form.get('answer_id', None)
    if answer_id:
        option = QuizOption.query.get(answer_id)
        if option.is_answer and int(option.quiz_id) == int(quiz_id):
            return jsonify(success=True)
    return jsonify(success=False)

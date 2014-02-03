from flask import Blueprint, render_template, current_app
from flask import request, redirect, url_for
from flask.ext.login import current_user
from flask.ext.babel import lazy_gettext as _

from mooc.app import rbac, db, csrf
from mooc.helpers import flash
from mooc.master.model import Tag, Feedback
from mooc.course.model import Subject
from mooc.resource.model import Resource
from mooc.master.form import FeedbackForm


master_app = Blueprint('master', __name__, template_folder='../templates')


@master_app.route('/')
@rbac.allow(['anonymous'], ['GET'])
def index():
    subjects = Subject.query.filter(Subject._state != 'deleted').all()
    return render_template('index.html', subjects=subjects)


@master_app.route('/about')
@rbac.allow(['anonymous'], ['GET'])
def about():
    return render_template('about.html')


@master_app.route('/privacy')
@rbac.allow(['anonymous'], ['GET'])
def privacy():
    return render_template('privacy.html')


@csrf.exempt
@master_app.route('/feedback', methods=['GET', 'POST'])
@rbac.allow(['anonymous'], ['GET', 'POST'])
def feedback():
    form = FeedbackForm(request.form)
    if form.validate_on_submit():
        feedback = Feedback(title=form.data['title'],
                            feedback=form.data['feedback'])
        
        if not current_user.is_anonymous():
            feedback.user = current_user

        feedback.save()
        flash(message=_('Submited successfully'), category='notice')
        return redirect(url_for('master.index'))

    if form.errors:
        flash(message=form.errors, category='warn', form_errors=True)

    return render_template('feedback.html', form=form)


@master_app.route('/tag/<tag>', methods=['GET'])
@rbac.allow(['anonymous'], ['GET'])
def tag(tag):
    tags = tag.split(' ')
    things = set()
    for t in tags:
        this_tags = Tag.query.filter_by(tag=t).all()
        for l_tag in this_tags:
            if hasattr(l_tag, 'lectures'):
                [setattr(x, 'type', 'lecture') for x in l_tag.lectures]
                things.update(l_tag.lectures)

            if hasattr(l_tag, 'courses'):
                [setattr(x, 'type', 'course') for x in l_tag.courses]
                things.update(l_tag.courses)

    return render_template('tag_view.html', things=things, tag=tag)

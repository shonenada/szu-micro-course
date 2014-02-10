from flask import Blueprint, render_template, current_app, jsonify
from flask import request, redirect, url_for
from flask.ext.login import current_user
from flask.ext.babel import lazy_gettext as _, gettext

from mooc.extensions import rbac, db, csrf
from mooc.utils.helpers import flash
from mooc.models.master import Tag, Feedback
from mooc.models.course import Subject
from mooc.forms.master import FeedbackForm


master_app = Blueprint('master', __name__)


@master_app.route('/')
@rbac.allow(['anonymous'], ['GET'])
def index():
    subjects = Subject.query.filter(Subject.state != 'deleted').all()
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

        return jsonify(
            success=True,
            messages=[gettext('Submited successfully')],
            next=url_for('master.index'),
        )

    if form.errors:
        return jsonify(success=False, errors=True, messages=form.errors)

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

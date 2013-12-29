import time

from flask import current_app as app, request, render_template, g

from mooc.app import db, rbac
from mooc.master.model import Tag


def common_paginate(model, page, per_page, filte=True):
    query = model.query.filter(model._state != 'deleted').filter(filte)
    pagination = query.paginate(page=page, per_page=per_page)
    return pagination


def common_delete(model, mid):
    obj = model.query.get(mid)
    if not obj:
        raise RuntimeError('Model is not found')
    if hasattr(obj, 'delete'):
        obj.delete()
    else:
        obj.state = 'deleted'
    db.session.add(obj)
    db.session.commit()


def common_edit(obj, form_data, **kwargs):
    assignment = kwargs.pop('assignment', {})
    for key, value in form_data.iteritems():
        setattr(obj, key, value)
    for key, value in assignment.iteritems():
        setattr(obj, key, value)
    db.session.add(obj)
    db.session.commit()


def common_create(model, data):
    pass


def get_tags():
    app.jinja_env.globals['tags'] = \
        Tag.query.order_by(Tag.count.desc()).all()


def setup_request_timer():
    g.request_start_time = time.time()

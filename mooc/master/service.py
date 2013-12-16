from mooc.app import db


def common_paginate(model, page, per_page, filte=True):
    query = model.query.filter(model._state != 'deleted').filter(filte)
    pagination = query.paginate(page=page, per_page=per_page)
    return pagination


def common_delete(model, mid):
    obj = model.query.get(mid)
    if not obj:
        raise RuntimeError('User is not found')
    if hasattr(model, 'delete'):
        obj.delete()
    else:
        obj.state = 'deleted'
    db.session.add(obj)
    db.session.commit()


def common_edit(obj, form_data, exceptions=()):
    for key, value in form_data.iteritems():
        if not key in exceptions:
            setattr(obj, key, value)
    db.session.add(obj)
    db.session.commit()

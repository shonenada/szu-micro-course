import time

from flask import g

from mooc.app import rbac
from mooc.utils import friendly_time
from mooc.course.service import learn_count, friendly_resource_category


_filters = {
    'friendly_time': friendly_time,
    'learn_count': learn_count,
    'enumerate': (lambda x: enumerate(x)),
    'ellipsis': (lambda x, l, f='...': "%s%s" %
                 (x[:l], f if len(x) > l else '')),
    'friendly_resource_category': friendly_resource_category,
}


_functions = {
    'has_perm': rbac.has_permission,
    'request_time': lambda: "%.5fs" % (time.time() - g.request_start_time),
}


def setup_filter(app):
    for _fname, _ffunc in _filters.iteritems():
        app.add_template_filter(_ffunc, _fname)


def setup_func(app):
    for _fname, _ffunc in _functions.iteritems():
        app.jinja_env.globals[_fname] = _ffunc

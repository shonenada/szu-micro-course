from mooc.utils import friendly_time
from mooc.course.service import learn_count


_filters = {
    'friendly_time': friendly_time,
    'learn_count': learn_count,
    'enumerate': (lambda x: enumerate(x)),
}


def setup_filter(app):
    for _fname, _ffunc in _filters.iteritems():
        app.jinja_env.filters[_fname] = _ffunc

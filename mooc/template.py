from mooc.utils import friendly_date
from mooc.course.service import learn_count


_filters = {
    'friendly_date': friendly_date,
    'learn_count': learn_count,
}


def setup_filter(app):
    for _fname, _ffunc in _filters.iteritems():
        app.jinja_env.filters[_fname] = _ffunc

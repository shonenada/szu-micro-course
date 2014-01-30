import os
import time

from flask import Flask, g, render_template, current_app

from mooc.extensions import gears, setup_compilers, setup_compressors
from mooc.extensions import setup_gears_environment
from mooc.extensions import db
from mooc.extensions import login_manager
from mooc.extensions import rbac, setup_rbac
from mooc.extensions import csrf
from mooc.master.view import master_app
from mooc.account.view import account_app
from mooc.course.view import course_app
from mooc.resource.view import resource_app
from mooc.qa.view import qa_app
from mooc.helpers import friendly_time
from mooc.course.service import (get_learn_records, get_last_lecture,
                                 learn_count)
from mooc.resource.service import friendly_resource_category


__all__ = ['create_app', 'rbac', 'db', 'csrf', 'login_manager']


def create_app(import_name=None, config=None):
    app = Flask(import_name or __name__)

    app.config.from_object('mooc.settings')

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.abspath(config))

    if app.config.get('SENTRY_ON', False):
        from raven.contrib.flask import Sentry
        sentry = Sentry(app)

    gears.init_app(app)
    setup_gears_environment(app)
    setup_compressors(app)
    setup_compilers(app)

    db.init_app(app)

    login_manager.init_app(app)

    rbac.init_app(app)
    setup_rbac(app)

    csrf.init_app(app)

    app.before_request(setup_request_timer)
    app.before_request(get_learn_records)
    app.before_request(get_last_lecture)

    setup_error_pages(app)

    setup_jinja(app)

    app.register_blueprint(master_app)
    app.register_blueprint(account_app)
    app.register_blueprint(course_app)
    app.register_blueprint(resource_app)
    app.register_blueprint(qa_app)

    return app


def setup_jinja(app):
    _jinja_filters = {
        'friendly_time': friendly_time,
        'learn_count': learn_count,
        'enumerate': (lambda x: enumerate(x)),
        'ellipsis': (lambda x, l, f='...': "%s%s" %
                     (x[:l], f if len(x) > l else '')),
        'friendly_resource_category': friendly_resource_category,
    }

    _jinja_global = {
        'site_title': app.config.get('SITE_TITLE'),
        'site_keyword': app.config.get('SITE_KEYWORD'),    
        'site_description': app.config.get('SITE_DESCRIPTION'),
        'has_perm': rbac.has_permission,
        'request_time': lambda: "%.5fs" % (time.time() - g.request_start_time),
    }

    def setup_filter(app):
        for _fname, _ffunc in _jinja_filters.iteritems():
            app.add_template_filter(_ffunc, _fname)

    def setup_global(app):
        for _fname, _ffunc in _jinja_global.iteritems():
            app.jinja_env.globals[_fname] = _ffunc

    setup_filter(app)
    setup_global(app)


def setup_request_timer():
    g.request_start_time = time.time()


def setup_error_pages(app):
    @app.errorhandler(403)
    def page_not_found(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(405)
    def method_not_allow(error):
        return render_template('errors/405.html'), 405

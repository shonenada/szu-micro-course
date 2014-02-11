import os
import time

from flask import Flask, g, render_template, current_app, request

from mooc.extensions import setup_babel
from mooc.extensions import setup_gears
from mooc.extensions import setup_database
from mooc.extensions import setup_login_manager
from mooc.extensions import setup_rbac, rbac
from mooc.extensions import setup_csrf
from mooc.views.master import master_app
from mooc.views.account import account_app
from mooc.views.admin import admin_app
from mooc.views.course import course_app
from mooc.views.resource import resource_app
from mooc.views.discuss import discuss_app
from mooc.utils._time import setup_request_timer, friendly_time, format_datetime
from mooc.services.course import (get_learn_records, get_last_lecture,
                                  learn_count)
from mooc.services.resource import friendly_resource_category


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

    setup_gears(app)
    setup_database(app)
    setup_login_manager(app)
    setup_rbac(app)
    setup_csrf(app)
    setup_babel(app)

    app.before_request(setup_request_timer)
    app.before_request(get_learn_records)
    app.before_request(get_last_lecture)

    setup_error_pages(app)
    setup_jinja(app)

    app.register_blueprint(master_app)
    app.register_blueprint(account_app)
    app.register_blueprint(admin_app)
    app.register_blueprint(course_app)
    app.register_blueprint(resource_app)
    app.register_blueprint(discuss_app)

    return app


def setup_jinja(app):
    _jinja_filters = {
        'date': format_datetime,
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

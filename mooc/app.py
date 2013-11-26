from flask import Flask


from mooc.extensions import gears, setup_compilers, setup_compressors
from mooc.extensions import db, setup_database
from mooc.extensions import login_manager
from mooc.extensions import rbac, setup_rbac
from mooc.extensions import csrf
from mooc.template import setup_filter, setup_func
from mooc.master.view import master_app
from mooc.account.view import account_app
from mooc.course.view import course_app
from mooc.course.service import get_learn_records, get_last_clip


def create_app(import_name=None, config=None):
    app = Flask(import_name or __name__)

    app.config.from_object('mooc.settings')

    if config:
        app.config.from_pyfile(config)

    if app.config.get('SENTRY_ON', False):
        from raven.contrib.flask import Sentry
        sentry = Sentry(app)

    gears.init_app(app)
    setup_compressors(app)
    setup_compilers(app)

    db.init_app(app)
    setup_database(app)

    login_manager.init_app(app)

    rbac.init_app(app)
    setup_rbac(app)

    csrf.init_app(app)

    app.register_blueprint(master_app)
    app.register_blueprint(account_app)
    app.register_blueprint(course_app)

    app.before_request(get_learn_records)
    app.before_request(get_last_clip)

    setup_filter(app)
    setup_func(app)

    return app

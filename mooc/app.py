from flask import Flask

from mooc.extensions import gears, db
from mooc.extensions import setup_compilers, setup_compressors, setup_database
from mooc.master.view import master_app
from mooc.course.view import course_app


def create_app(import_name=None, config=None):
    app = Flask(import_name or __name__)

    app.config.from_object('mooc.settings')
    app.config.from_pyfile(config)

    if app.config['SENTRY_ON']:
        from raven.contrib.flask import Sentry
        sentry = Sentry(app)

    gears.init_app(app)
    setup_compressors(app)
    setup_compilers(app)

    db.init_app(app)
    setup_database(app)

    app.register_blueprint(master_app)
    app.register_blueprint(course_app)

    return app

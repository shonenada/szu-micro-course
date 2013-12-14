from flask import redirect, url_for, render_template
from flask.ext.gears import Gears
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, current_user
from flask.ext.seasurf import SeaSurf
from flask_rbac import RBAC
from gears.compressors import SlimItCompressor
from gears_stylus import StylusCompiler
from gears_clean_css import CleanCSSCompressor
from gears_coffeescript import CoffeeScriptCompiler


gears = Gears()
db = SQLAlchemy()
login_manager = LoginManager()
rbac = RBAC()
csrf = SeaSurf()

_compilers = {
    '.styl': StylusCompiler.as_handler(),
    '.coffee': CoffeeScriptCompiler.as_handler()
}

_compressors = {
    "text/css": CleanCSSCompressor.as_handler(),
    "application/javascript": SlimItCompressor.as_handler()
}


def gears_environment(app):
    return app.extensions['gears']['environment']


def setup_gears_environment(app):
    env = gears_environment(app)
    env.fingerprinting = app.config.get('GEARS_FINGERPRINTING', True)


def setup_compilers(app):
    env = gears_environment(app)
    for extension, compiler in _compilers.iteritems():
        env.compilers.register(extension, compiler)


def setup_compressors(app):
    env = gears_environment(app)
    if not app.config["DEBUG"] or app.config["TESTING"]:
        for mimetype, compressor in _compressors.iteritems():
            env.compressors.register(mimetype, compressor)


def setup_database(app):
    db = app.extensions["sqlalchemy"].db

    @app.before_first_request
    def create_database_for_development():
        is_sqlite_memory = (db.engine.url.drivername == "sqlite" and
                            db.engine.url.host in ("", ":memory:"))
        if app.config["DEBUG"] and is_sqlite_memory:
            db.create_all()


def setup_rbac(app):
    from mooc.account.model import User, Role
    _rbac = app.extensions['rbac'].rbac
    _rbac.set_role_model(Role)
    _rbac.set_user_model(User)
    _rbac.set_user_loader(lambda *args: current_user)


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

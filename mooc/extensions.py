from flask.ext.gears import Gears
from flask.ext.sqlalchemy import SQLAlchemy
from gears.compressors import SlimItCompressor
from gears_stylus import StylusCompiler
from gears_clean_css import CleanCSSCompressor
from gears_coffeescript import CoffeeScriptCompiler


gears = Gears()
db = SQLAlchemy()

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

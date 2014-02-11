from flask.ext.gears import Gears
from gears.compressors import SlimItCompressor
from gears_stylus import StylusCompiler
from gears_clean_css import CleanCSSCompressor
from gears_coffeescript import CoffeeScriptCompiler


gears = Gears()


_compilers = {
    '.styl': StylusCompiler.as_handler(),
    '.coffee': CoffeeScriptCompiler.as_handler()
}

_compressors = {
    "text/css": CleanCSSCompressor.as_handler(),
    "application/javascript": SlimItCompressor.as_handler()
}


def setup_gears(app):
    gears.init_app(app)
    setup_gears_environment(app)
    setup_compressors(app)
    setup_compilers(app)


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

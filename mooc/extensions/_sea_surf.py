from flask.ext.seasurf import SeaSurf


csrf = SeaSurf()


def setup_csrf(app):
    csrf.init_app(app)

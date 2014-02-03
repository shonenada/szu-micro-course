from flask import request
from flask.ext.babel import Babel

babel = Babel()


def setup_babel(app):
    babel.init_app(app)
    default = app.config.get('BABEL_DEFAULT_LOCALE', 'en')
    supported = app.config.get('BABEL_SUPPORTED_LOCALES', ['en', 'zh'])

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(supported, default)

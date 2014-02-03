from flask.ext.login import LoginManager, current_user

from mooc.models.account import User


login_manager = LoginManager()


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


def setup_login_manager(app):
    login_manager.init_app(app)

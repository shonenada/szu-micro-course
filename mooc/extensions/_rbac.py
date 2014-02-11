from flask.ext.login import current_user
from flask.ext.rbac import RBAC


rbac = RBAC()


def setup_rbac(app):
    rbac.init_app(app)
    from mooc.models.account import User, Role
    rbac.set_role_model(Role)
    rbac.set_user_model(User)
    rbac.set_user_loader(lambda *args: current_user)

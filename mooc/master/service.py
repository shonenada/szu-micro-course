from flask import current_app
from flask.ext.login import current_user

from mooc.app import rbac


def has_perm(method, endpoint):
    view_func = current_app.view_functions[endpoint]
    is_allowed = False
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            is_allowed = is_allowed and rbac.check_permission(role, method, view_func)
    return is_allowed

from time import time

from mooc.extensions import login_manager
from mooc.account.model import User


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

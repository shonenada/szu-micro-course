from time import time

from flask import g, session

from mooc.account.model import User, SzuAccount


def login(user, expires=129600):
    if type(user) is User:
        g.current_user = user
        expires += time()
        session['uid'] = (user.id, expires)
        return user
    return None


def logout():
    del session['uid']
    g.current_user = None

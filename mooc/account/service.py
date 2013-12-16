from time import time

from mooc.app import db
from mooc.extensions import login_manager
from mooc.account.model import User, SzuAccount


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


def update_user_state(user_id, state):
    if not state in User.USER_STATE_VALUES:
        raise ValueError('State is invalid.')
    user = User.query.get(user_id)
    if not user:
        raise RuntimeError('User is not found')
    if state == 'frozen':
        user.freeze()
    elif state == 'active':
        user.active()
    db.session.add(user)
    db.session.commit()


def change_user_password(user_id, new_password):
    user = User.query.get(user_id)
    if not user:
        raise RuntimeError('User is not found')
    user.change_password(new_password)
    db.session.add(user)
    db.session.commit()


def create_user(data):
    college = data.get('college', None)
    user = User(data['username'], data['raw_passwd'],
                data['nickname'], data['is_male'] is 'True')
    user.name = data['name']
    user.email = data['email']
    user.phone = data['phone']
    user.qq = data['qq']
    user.state = data['state']
    szu_account = SzuAccount(user, data['card_id'], data['stu_number'],
                             college, data['szu_account_type'])
    szu_account.short_phone = data['short_phone']
    db.session.add(user)
    db.session.add(szu_account)
    db.session.commit()

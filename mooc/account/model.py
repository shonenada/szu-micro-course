from uuid import uuid4
from hashlib import sha256
from datetime import datetime

from mooc.app import db
from mooc.utils import enumdef
from mooc.exception import UserStateException


class User(db.Model):
    """Model of user."""

    __tablename__ = 'user'

    USER_STATE_VALUES = ('normal', 'frozen', 'deleted', 'unactivated')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=True)
    hashed_password = db.Column(db.String(128))
    nickname = db.Column(db.String(16), unique=True)
    name = db.Column(db.String(20))
    is_male = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(11), unique=True)
    qq = db.Column(db.String(15), unique=True)
    avatar = db.Column(db.String(250))
    created = db.Column(db.DateTime, default=datetime.utcnow())
    last_login = db.Column(db.DateTime, default=datetime.utcnow())
    last_ip = db.Column(db.String(40))
    salt = db.Column(db.String(32), nullable=False)
    _state = db.Column('state', db.Enum(name='user_state', *USER_STATE_VALUES))
    state = enumdef('_state', USER_STATE_VALUES)
    learn_records = db.relationship('LearnRecord', backref='user',
                                    uselist=True)
    questions = db.relationship('Question', backref='author',
                                uselist=True, lazy='dynamic')
    answers = db.relationship('Answer', backref='author',
                              uselist=True, lazy='dynamic')
    courses = db.relationship("Course", backref='author',
                              uselist=True, lazy='dynamic')
    clips = db.relationship("Clip", backref='author',
                            uselist=True, lazy='dynamic')
    up_down_records = db.relationship('UpDownRecord', backref='user',
                                      uselist=True, lazy='dynamic')

    def __init__(self, username, raw_passwd, nickname, is_male=True):
        self.username = username
        self.set_passwd(raw_passwd)
        self.nickname = nickname
        self.is_male = is_male
        self.created = datetime.utcnow()
        self.last_login = datetime.utcnow()
        self.state = 'unactivated'

    def __unicode__(self):
        return self.nickname

    def __repr__(self):
        return "<User:%s(%s)>" % (self.username, self.nickname)

    def set_passwd(self, raw_passwd):
        self.salt = uuid4().hex
        self.hashed_password = self._hash_password(self.salt, raw_passwd)

    def active(self):
        self._transform_state(from_state='unactivated', to_state='normal')

    def freeze(self):
        self._transform_state(from_state='normal', to_state='frozen')

    def unfrozen(self):
        self._transform_state(from_state='frozen', to_state='normal')

    @staticmethod
    def _hash_password(salt, password):
        hashed = sha256()
        hashed.update("<%s|%s>" % (salt, password))
        return hashed.hexdigest()

    def _transform_state(self, from_state, to_state):
        if self.state == from_state:
            self.state = to_state
        else:
            raise UserStateException("The state of user is mismatched!")


class SzuAccount(db.Model):

    __tablename__ = 'szu_account'

    TYPE_VALUES = ('undergrade', 'graduate', 'teacher', 'other')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='user', uselist=False)
    card_id = db.Column(db.String(6), unique=True)
    stu_number = db.Column(db.String(10), unique=True)
    short_phone = db.Column(db.String(6), unique=True)
    szu_account_type = enumdef('_szu_account_type', TYPE_VALUES)
    _szu_account_type = db.Column('szu_account_tpye',
                                  db.Enum(name='szu_account_type',
                                  *TYPE_VALUES))
    college = db.relationship("College", backref='szu_account', uselist=False)
    teacher = db.relationship("Teacher", backref='szu_account', uselist=False)


    def __init__(self, user, card_id, stu_number, college, szu_account_type):
        self.user = user
        self.card_id = card_id
        self.stu_number = stu_number
        self.college = college
        self.set_account_type(szu_account_type)

    def __repr__(self):
        return "<SzuAccount %s>" % (self.stu_number)

    def set_account_type(self, szu_account_type):
        if szu_account_type in self.TYPE_VALUES:
            self.szu_account_type = szu_account_type
        else:
            self.szu_account_type = 'other'


class College(db.Model):
    """Model of College"""

    __tablename__ = 'college'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=True)
    order = db.Column(db.Integer)
    szu_account_id = db.Column(db.Integer, db.ForeignKey('szu_account.id'))
    clips = db.relationship('Clip', backref='college',
                            lazy='dynamic', uselist=True)

    def __init__(self, name, order=None):
        self.name = name
        self.order = order if order else 9999

    def __repr__(self):
        return "<College %s, %d>" % (self.name, self.order)


class Teacher(db.Model):
    """Model of Teacher"""

    __tablename__ = 'teacher'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    description = db.Column(db.Text)
    clips = db.relationship('Clip', backref='teacher', lazy='dynamic')
    szu_account_id = db.Column(db.Integer, db.ForeignKey('szu_account.id'))

    def __init__(self, title, description, szu_account):
        self.title = title
        self.description = description
        self.szu_account = szu_account

    def __repr__(self):
        return "<Teacher %s>" % (self.szu_account_id)

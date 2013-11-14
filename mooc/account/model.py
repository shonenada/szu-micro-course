from uuid import uuid4
from hashlib import sha256
from datetime import datetime

from mooc.app import db
from mooc.utils import enumdef
from mooc.exception import UserStateException


class Account(db.Model):
    """Model of account."""

    __tablename__ = 'account'

    TYPE_VALUES = ('undergrade', 'graduate', 'teacher', 'other')
    STATE_VALUES = ('normal', 'frozen', 'deleted', 'unactivated')

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.String(6), unique=True)
    hashed_password = db.Column(db.String(128))
    stu_number = db.Column(db.String(10), unique=True)
    nickname = db.Column(db.String(16), unique=True)
    name = db.Column(db.String(20))
    gender = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(11), unique=True)
    short_phone = db.Column(db.String(6), unique=hashed_True)
    qq = db.Column(db.String(15), unique=True)
    avatar = db.Column(db.String(250))
    created = db.Column(db.DateTime, default=datetime.now)
    last_ip = db.Column(db.String(40))
    last_login = db.Column(db.DateTime, default=datetime.now)
    salt = db.Column(db.String(32), nullable=False)
    _account_type = db.Column('account_tpye',
                              db.Enum(name='account_type', *TYPE_VALUES))
    _state = db.Column('state', db.Enum(name='account_state', *STATE_VALUES))
    account_type = enumdef('_account_type', TYPE_VALUES)
    state = enumdef('_state', STATE_VALUES)
    college = db.relationship("College", backref='account', uselist=False)
    teacher = db.relationship("Teacher", backref='account', uselist=False)
    learn_record = db.relationship('LearnRecord', backref='author',
                                   uselist=True)
    question = db.relationship('Question', backref='author',
                               uselist=True, lazy='dynamic')
    answer = db.relationship('Answer', backref='author',
                             uselist=True, lazy='dynamic')
    course = db.relationship("Course", backref='author',
                             uselist=True, lazy='dynamic')
    up_down_record = db.relationship('UpDownRecord', backref='author',
                                     uselist=True, lazy='dynamic')

    def __init__(self, card_id, stu_number, raw_password,
                nickname, account_type):
        self.card_id = card_id
        self.stu_number = stu_number
        self.hashed_password = set_passwd(raw_password)
        self.nickname = nickname
        self.set_account_type(user_type)
        self.state = 'unactivated'

    def __unicode__(self):
        return self.nickname

    def __repr__(self):
        return "<Account:%s(%s)>" % (self.stu_number, self.nickname)

    def set_passwd(self, raw_passwd):
        self.salt = uuid4.hex
        self.hashed_password = hash_password(self.salt, raw_passwd)

    def set_account_type(self, account_type):
        if account_type in self.TYPE_VALUES:
            self.account_type = account_type
        else:
            self.account_type = 'other'

    def active(self):
        self._transform_state(from_state='unactivated', to_state='normal')

    def freeze(self):
        self._transform_state(from_state='normal', to_state='frozen')

    def unfrozen(self):
        self._transform_state(from_state='frozen', to_state='normal')

    @staticmethod
    def hash_password(salt, password):
        hashed = sha256()
        hashed.update("<%s|%s>", % (salt, password))
        return hashed.hexdigest()

    def _transform_state(self, from_state, to_state):
        if self.state == from_state:
            self.state = to_state
        else:
            raise UserStateException("The state of user is mismatched!")


class College(db.Model):
    """Model of College"""

    __tablename__ = 'college'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=True)
    order = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    clip = db.relationship('Clip', backref='college',
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
    clip = db.relationship('Clip', backref='teacher', lazy='dynamic')
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

import urllib
from uuid import uuid4
from hashlib import sha256, md5
from datetime import datetime

from flask import url_for
from flask.ext.babel import lazy_gettext as _
from flask.ext.sqlalchemy import BaseQuery
from flask.ext.rbac import RoleMixin, UserMixin

from mooc.extensions import db
from mooc.utils.helpers import enumdef
from mooc.exception import UserStateException
from mooc.models.master import ModelMixin


class UserQuery(BaseQuery):

    def authenticate(self, username, raw_passwd):
        user = self.filter(User.username == username).first()
        if user and user.check_password(raw_passwd):
            return user
        return None


roles_parents = db.Table(
    'roles_parents',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('parent_id', db.Integer, db.ForeignKey('role.id'))
)

users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(RoleMixin, db.Model, ModelMixin):

    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    parents = db.relationship('Role', secondary=roles_parents,
                              primaryjoin=(id == roles_parents.c.role_id),
                              secondaryjoin=(id == roles_parents.c.parent_id),
                              backref=db.backref('children', lazy='dynamic'))
    users = db.relationship('User', secondary=users_roles,
                            backref=db.backref('roles', lazy='dynamic'))

    def __init__(self, name):
        RoleMixin.__init__(self)
        self.name = name

    def add_parent(self, parent):
        self.parents.append(parent)

    def add_parents(self, *ps):
        for parent in ps:
            self.add_parent(parent)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<Role: %s>" % self.name

    @staticmethod
    def get_by_name(name):
        return Role.query.filter_by(name=name).first()


class User(db.Model, UserMixin, ModelMixin):
    """Model of user."""

    __tablename__ = 'user'
    query_class = UserQuery
    USER_STATE_VALUES = ('normal', 'frozen', 'deleted', 'unactivated')
    USER_STATE_TEXTS = (_('Normal'), _('Frozen'),
                        _('Deleted'), _('Unactivated'))

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=True)
    hashed_password = db.Column(db.String(40))
    nickname = db.Column(db.String(16), unique=True)
    name = db.Column(db.String(20))
    is_male = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(50))
    phone = db.Column(db.String(11))
    qq = db.Column(db.String(15))
    avatar = db.Column(db.String(250))
    created = db.Column(db.DateTime, default=datetime.utcnow())
    salt = db.Column(db.String(32), nullable=False)
    state = db.Column(db.Enum(*USER_STATE_VALUES))
    learn_records = db.relationship('LearnRecord', backref='user',
                                    uselist=True)
    questions = db.relationship('Question', backref='author',
                                uselist=True, lazy='dynamic')
    answers = db.relationship('Answer', backref='author',
                              uselist=True, lazy='dynamic')
    up_down_records = db.relationship('UpDownRecord', backref='user',
                                      uselist=True, lazy='dynamic')

    def __init__(self, **kwargs):

        self.salt = uuid4().hex

        if 'username' in kwargs:
            username = kwargs.pop('username')
            self.username = username.lower()

        if 'passwd' in kwargs:
            raw_passwd = kwargs.pop('passwd')
            self.change_password(raw_passwd)

        if 'email' in kwargs:
            email = kwargs.pop('email')
            self.email = email.lower()

        if 'is_male' in kwargs:
            is_male = kwargs.pop('is_male')
            self.is_male = (is_male == True)

        if 'state' in kwargs:
            self.state = kwargs.pop('state')
        else:
            self.state = 'unactivated'

        db.Model.__init__(self, **kwargs)

        self.created = datetime.utcnow()

    def __unicode__(self):
        return self.nickname

    def __repr__(self):
        return "<User:%s(%s)>" % (self.username, self.nickname)

    def change_password(self, raw_passwd):
        self.salt = uuid4().hex
        self.hashed_password = self._hash_password(self.salt, raw_passwd)

    def check_password(self, raw_passwd):
        _hashed_password = self._hash_password(self.salt, raw_passwd)
        return (self.hashed_password == _hashed_password)

    def is_active(self):
        return (self.state == 'normal')

    def is_anonymous(self):
        return (self.username is None)

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return (self.state == 'normal')

    def active(self):
        self.state = 'normal'

    def get_avatar(self, size=70):
        if self.avatar:
            return self.avatar

        if not self.email:
            self.email = 'None'
        URL_PATTERN = "http://www.gravatar.com/avatar/%s?%s"
        gravatar_url = URL_PATTERN % (md5(self.email.lower()).hexdigest(),
                                      urllib.urlencode({'s': str(size)}))
        return gravatar_url

    @staticmethod
    def _hash_password(salt, password):
        hashed = sha256()
        hashed.update("<%s|%s>" % (salt, password))
        return hashed.hexdigest()



class SzuAccount(db.Model, ModelMixin):

    __tablename__ = 'szu_account'

    TYPE_VALUES = ('undergrade', 'graduate', 'teacher', 'other')
    TYPE_TEXTS = (_('Undergrade'), _('Graduate'),
                  _('Teacher'), _('Other'))

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_id = db.Column(db.String(6), unique=True)
    stu_number = db.Column(db.String(10), unique=True)
    short_phone = db.Column(db.String(6), unique=True)
    szu_account_type = db.Column(db.Enum(*TYPE_VALUES))
    user = db.relationship(
        'User', uselist=False,
        backref=db.backref('szu_account', uselist=False))
    college = db.relationship(
        "College", uselist=False,
        backref=db.backref('szu_account', uselist=False))
    teacher = db.relationship(
        "Teacher", uselist=False,
        backref=db.backref('szu_account', uselist=False))

    def __init__(self, **kwargs):
        if 'szu_account_type' in kwargs:
            szu_account_type = kwargs.pop('szu_account_type')
            self.set_account_type(szu_account_type)

        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return "<SzuAccount %s>" % (self.stu_number)

    def set_account_type(self, szu_account_type):
        if szu_account_type in self.TYPE_VALUES:
            self.szu_account_type = szu_account_type
        else:
            self.szu_account_type = 'other'

    @staticmethod
    def get_type(type_name):
        if type_name in SzuAccount.TYPE_VALUES:
            return SzuAccount.TYPE_TEXTS[
                SzuAccount.TYPE_VALUES.index(type_name)]
        else:
            return None


class College(db.Model, ModelMixin):
    """Model of College"""

    __tablename__ = 'college'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=True)
    order = db.Column(db.Integer)
    szu_account_id = db.Column(db.Integer, db.ForeignKey('szu_account.id'))
    courses = db.relationship('Course', backref='college',
                              lazy='dynamic', uselist=True)

    def __init__(self, **kwargs):
        if 'order' in kwargs:
            self.order = kwargs.pop('order')
        else:
            order = 9999

        db.Model.__init__(self, **kwargs)

    def __str__(self):
        return ("%s" % self.name)

    def __repr__(self):
        return "<College %s, %d>" % (self.name, self.order)


class Teacher(db.Model, ModelMixin):
    """Model of Teacher"""

    __tablename__ = 'teacher'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10))
    description = db.Column(db.Text)
    lectures = db.relationship('Lecture', uselist=True,
                               backref=db.backref('teacher', uselist=False))
    courses = db.relationship("Course", uselist=True,
                              backref=db.backref('teacher', uselist=False))
    szu_account_id = db.Column(db.Integer, db.ForeignKey('szu_account.id'))

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __str__(self):
        return ("%s" % self.szu_account.user.name
                if self.szu_account.user.name
                else self.szu_account.user.nickname)

    def __repr__(self):
        return "<Teacher %s>" % (self.szu_account_id)

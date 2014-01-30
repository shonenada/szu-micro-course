import os
import unittest

from mooc.app import create_app, db
from mooc.account.model import Role, User


class BaseSuite(unittest.TestCase):

    def setUp(self):

        config = {
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SENTRY_ON': False,
            'SECRET_KEY': 'SECRET_KEY_FOR_TEST',
            'ADMIN_PAGESIZE': 20,
        }

        app = create_app(config=config)
        self.app = app

        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tests/test.sqlite'

        self.client = app.test_client()

        with self.app.test_request_context():
            db.create_all()

        if hasattr(self, 'prehook'):
            self.prehook()

    def prepare_role(self):
        self.roles = {}
        
        with self.app.test_request_context():
            anonymous = Role('anonymous')
            local_user = Role('local_user')
            student = Role('student')
            teacher = Role('teacher')
            super_admin = Role('super_admin')

            self.roles['anonymous'] = anonymous
            self.roles['local_user'] = local_user
            self.roles['student'] = student
            self.roles['teacher'] = teacher
            self.roles['super_admin'] = super_admin

            db.session.add(anonymous)
            db.session.add(local_user)
            db.session.add(student)
            db.session.add(teacher)
            db.session.add(super_admin)

            db.session.commit()

    def prepare_account(self):
        self.accounts = {}

        with self.app.test_request_context():
            male_user = User(username='normal_user', passwd='passwd')
            female_user = User(username='normal_user_female', passwd='passwd')
            staff_user = User(username='staff', passwd='passwd')

            self.accounts['male'] = male_user
            self.accounts['female'] = female_user
            self.accounts['staff'] = staff_user

            male_user.roles.append(self.roles['local_user'])
            female_user.roles.append(self.roles['local_user'])
            staff_user.roles.append(self.roles['super_admin'])

            db.session.add(male_user)
            db.session.add(female_user)
            db.session.add(staff_user)
            db.session.commit()

    def prepare_login(self, username='foo'):
        self.prepare_account()
        self.client.post('/signin', data={
            'username': username,
            'password': 'passwd'
        }, follow_redirects=True)

    def tearDown(self):
        with self.app.test_request_context():
            db.session.remove()
            db.drop_all()

            if hasattr(self, 'posthook'):
                self.posthook()
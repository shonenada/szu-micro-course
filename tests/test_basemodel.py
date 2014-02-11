# coding: utf-8
import uuid

from mooc.extensions import db
from mooc.models.master import ModelMixin
from mooc.models.account import Role, User
from .suite import BaseSuite


class BaseModelUnitTests(BaseSuite):

    def test_paginate(self):
        with self.app.test_request_context():
            pagination = Role.paginate(page=5, per_page=1)
            self.assertEqual(pagination.pages, 5)
            self.assertEqual(pagination.prev_num, 4)
            self.assertFalse(pagination.has_next)

    def test_edit_without_commit(self):
        with self.app.test_request_context():
            user = User(username='test_user')
            self.assertEqual(user.username, 'test_user')
    
            db.session.add(user)
            db.session.commit()
            mock_form_data = {
                'username': 'new_test_username',
                'nickname': 'nickname_of_test_user',
                'is_male': False,
            }
    
            user.edit(mock_form_data, commit=False)
            self.assertEqual(user.username, 'new_test_username')
            self.assertEqual(user.nickname, 'nickname_of_test_user')
            self.assertFalse(user.is_male)

            db.session.remove()
    
            same_user = User.query.filter_by(username='test_user').first()
            self.assertEqual(same_user.username, 'test_user')
            
    def test_edit_with_commit(self):
        with self.app.test_request_context():
            user = User(username='test_user_to_commit')
            db.session.add(user)
            db.session.commit()

            mock_form_data = {
                'username': 'new_test_username',
                'nickname': 'nickname_of_test_user',
                'is_male': False,
            }
            user.edit(mock_form_data, commit=True)

            db.session.remove()

            same_user = User.query.filter_by(username='new_test_username').first()
            self.assertFalse(same_user.is_male)

    def test_delete(self):
        with self.app.test_request_context():
            role = Role('test_role')
            db.session.add(role)
            db.session.commit()

            same_role = Role.query.filter_by(name='test_role').first()
            same_role.delete()

            also_same_role = Role.query.filter_by(name='test_role').first()
            self.assertTrue(also_same_role is None)

            user = User(username='username')
            user.active()
            db.session.add(user)
            db.session.commit()

            same_user = User.query.filter_by(username='username').first()
            same_user.delete()
            
            also_same_user = User.query.filter_by(username='username').first()
            self.assertTrue(also_same_user.state=='deleted')

    def prehook(self):
        self.prepare_role()
        self.prepare_account()

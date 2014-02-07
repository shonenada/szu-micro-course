# coding: utf-8
import os

from flask import Flask

from .suite import BaseSuite
from mooc.app import create_app


class CreateAppUnitTests(BaseSuite):

    def test_basic_create(self):
        test_app = create_app()
        self.assertIsInstance(test_app, Flask)

    def test_dict_config_create(self):
        test_app = create_app(config={'args_for_test': 'some arguments go here'})
        self.assertIn('args_for_test', test_app.config)
        self.assertEqual(test_app.config.get('args_for_test'),
                         'some arguments go here')

    def test_file_config_create(self):
        app_root = os.path.dirname(os.path.realpath(__name__))
        config_file = os.path.join(app_root, 'tests', 'config_for_test.conf')
        test_app = create_app(config=config_file)
        self.assertIn('ARG_FOR_TEST', test_app.config)
        self.assertEqual('Config for test', test_app.config.get('ARG_FOR_TEST'))

import os.path

from flask.ext.script import Manager, Server

from develop_tools.clean import clean as cln
from develop_tools.pep8 import pep8
from develop_tools.search import search
from mooc.app import create_app
from mooc.app import db


app_root = os.path.dirname(os.path.realpath(__name__))

application = create_app('mooc', os.path.join(app_root, 'development.conf'))
server = Server(port=13800)
manager = Manager(application)
manager.add_command("runserver", server)


@manager.command
def clean():
    cln()


@manager.command
def check():
    pep8()


@manager.command
def run(port=13800):
    application.run(host='0.0.0.0', port=port, debug=True)


@manager.command
def createdb(config="development.conf"):
    config_file = os.path.join(app_root, config)
    application.config.from_pyfile(config_file)
    with application.test_request_context():
        # import all Models here
        from mooc.master.model import Tag
        from mooc.account.model import (User, SzuAccount, College, Teacher,
                                        Role, roles_parents, users_roles)
        from mooc.course.model import (Subject, Category, Course, Lecture,
                                       LearnRecord, lecture_tags, course_tags)
        from mooc.qa.model import UpDownRecord, Answer, Question
        from mooc.resource.model import Resource
        db.create_all()
    print 'Created Database!'


@manager.command
def initdb(config="development.conf"):
    config_file = os.path.join(app_root, config)
    application.config.from_pyfile(config_file)
    with application.test_request_context():
        # Initial data for test
        from fixture import init_db
        init_db()
    print "Initialized Database!"


@manager.command
def syncdb(config="development.conf"):
    createdb(config)
    initdb(config)


@manager.command
def find(content, path='./', suffix='py'):
    file_pattern = r"^[a-zA-Z0-9_]+\.(" + suffix + ")$"
    search(path, file_pattern, content)


if __name__ == '__main__':
    manager.run()

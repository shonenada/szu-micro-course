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
    """Clean *.pyc and *.pyo files"""
    cln()


@manager.command
def check():
    """PEP8 Check"""
    pep8()


@manager.option('-p', dest='port', help='Port to host', default=13800)
def run(port):
    """Run app at 0.0.0.0"""
    application.run(host='0.0.0.0', port=port, debug=True)


@manager.option('-c', dest='config', help='Config file',
                default='development.conf')
@manager.option('-d', dest='destory', help='Destory database', default=False)
def createdb(config, destory):
    """Create database using `config` as config files,
    use `development.conf by default
    """
    config_file = os.path.join(app_root, config)
    application.config.from_pyfile(config_file)
    with application.test_request_context():
        if destory:
            db.drop_all()
        # import all Models here
        from mooc.master.model import Tag, Feedback
        from mooc.account.model import (User, SzuAccount, College, Teacher,
                                        Role, roles_parents, users_roles)
        from mooc.course.model import (Subject, Category, Course, Lecture,
                                       LearnRecord, lecture_tags, course_tags)
        from mooc.qa.model import UpDownRecord, Answer, Question
        from mooc.resource.model import Resource
        db.create_all()
    print 'Created Database!'


@manager.option('-c', dest='config', help='Config file',
                default='development.conf')
def initdb(config):
    """Initialize database, fill data with `fixture` module."""
    config_file = os.path.join(app_root, config)
    application.config.from_pyfile(config_file)
    with application.test_request_context():
        # Initial data for test
        from fixture import init_db
        init_db()
    print "Initialized Database!"


@manager.option('-c', dest='config', help='Config file',
                default='development.conf')
@manager.option('-d', dest='destory', help='Destory database', default=True)
def syncdb(config, destory):
    """Create and initialize database"""
    createdb(config, destory)
    initdb(config)


@manager.option('-c', dest='content', help='Content to find', required=True)
@manager.option('-p', dest='path', default='./', help='Where to find')
@manager.option('-s', dest='suffix', default='py',
                help='What kinds of file to find.')
def find(content, path, suffix):
    """Find content in project."""
    file_pattern = r"^[a-zA-Z0-9_]+\.(" + suffix + ")$"
    search(path, file_pattern, content)


if __name__ == '__main__':
    manager.run()

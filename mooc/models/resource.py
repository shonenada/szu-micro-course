from datetime import datetime

from mooc.extensions import db
from mooc.utils.helpers import enumdef
from mooc.models.master import ModelMixin


class Resource(db.Model, ModelMixin):

    __tablename__ = 'resource'

    RESOURCE_CATEGORY = ('ppt', 'doc', 'pdf', 'video', 'other')
    RESOURCE_STATE = ('normal', 'deleted')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='resources', uselist=False)
    resource_url = db.Column(db.String(250))
    category = db.Column(db.Enum(*RESOURCE_CATEGORY))
    created = db.Column(db.DateTime)
    view_count = db.Column(db.Integer, default=0)
    download_count = db.Column(db.Integer, default=0)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lecture.id'))
    lecture = db.relationship('Lecture', backref='resources', uselist=False)
    state = db.Column(db.Enum(*RESOURCE_STATE))

    def __init__(self, name):
        self.name = name
        self.created = datetime.utcnow()
        self.view_count = 0
        self.download_count = 0
        self.category = 'other'
        self.state = 'normal'

    def __repr__(self):
        return "<CourseResource %s>" % self.name

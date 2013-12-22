from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func

from mooc.app import db


class Tag(db.Model):

    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))

    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return self.tag

    def __unicode__(self):
        return self.tag

    @hybrid_property
    def count(self):
        return self.count()

    @count.expression
    def count(cls):
        return (select([func.count(Tag.id)]).
                where(cls.id == Tag.id).label('count'))

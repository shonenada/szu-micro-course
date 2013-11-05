from mooc.app import db


class Tag(db.Model):

    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    clip_id = db.Column(db.Integer, db.ForeignKey('clip.id'))
    clip = db.relationship('Clip', backref=db.backref('tag'))
    tag = db.Column(db.String(20))
    tag_type = db.Column(db.Integer)

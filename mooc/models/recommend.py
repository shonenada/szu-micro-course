from mooc.extensions import db


class Recommend(db.Model):

    __tablename__ = 'recommend'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    user = db.relationship('User', uselist=False, backref='recommends')
    tag = db.relationship('Tag', uselist=False, backref='recommends')

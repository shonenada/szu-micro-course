from mooc.app import db


class ClipTag(db.Model):
    __tablename__ = 'clip_tag'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))


class CourseTag(db.Model):
    __tablename__ = 'course_tag'
    
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))

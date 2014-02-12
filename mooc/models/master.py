from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func

from mooc.extensions import db


class ModelMixin(object):
    """Custom model of MOOC"""

    @classmethod
    def paginate(self, page, per_page=20, error_out=True, order_by=None,
                 filters=[], with_deleted=False):
        """A proxy method to return `per_page` items from page `page`.
        If there is `state` attribute in class and `with_deleted` is `False`
        it will filter out which was `state != 'deleted'`.
        If items were not found it will abort with 404.

        Example::

            User(BaseModel):
                id = BaseModel.Column(BaseModel.Integer, primary_key=True)
                name = BaseModel.Column(BaseModel.String(20))

            User.paginate(page=1, per_page=3)

        Returns an :class:`Pagination` object.

        :param page: Page to show.
        :param per_page: Sepcify how many items in a page.
        :param error_out: If `False`, disable abort with 404.
        :param filters: A list that the query wile filter.
        :param with_deleted: If True, it will not filter `state != 'deleted'`
        """
        query = self.query

        if hasattr(self, 'state') and not with_deleted:
            query = query.filter(self.state != 'deleted')

        for filte in filters:
            query = query.filter(filte)

        if not order_by is None:
            query = query.order_by(order_by)

        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=error_out
        )

        return pagination

    def save(self, commit=True):
        """Proxy method of saving object to database"""
        db.session.add(self)
        if commit:
            db.session.commit()

    def edit(self, form_data, commit=True):
        """Edit object from `form_data`.

        :param form_data: Data to save in object.
        :param commit: If `commit` is `True`
                       it will commit to database immediately
                       after editing object.
        """        
        for key, value in form_data.iteritems():
            setattr(self, key, value)

        db.session.add(self)

        if commit:
            db.session.commit()

    def delete(self, commit=True):
        """Delete object from database.

        :param commit: Commit to database immediately
        """
        if hasattr(self, 'state'):
            self.state = 'deleted'
        else:
            db.session.delete(self)

        if commit:
            db.session.commit()


class Tag(db.Model):
    """Model of tag. Used by Lecture, Course and Question.

    :param tag: The name of tag. Must be less than 20 characters.
    """
 
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))

    def __str__(self):
        return self.tag

    def __unicode__(self):
        return self.tag

    @hybrid_property
    def count(self):
        return self.count()

    @count.expression
    def count(cls):
        """Return count of cls.id"""
        return (select([func.count(Tag.id)]).
                where(cls.id == Tag.id).label('count'))


class Feedback(db.Model, ModelMixin):

    STATE = ('normal', 'deleted')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    contact = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='feedbacks', uselist=False)
    ip = db.Column(db.String(40))
    created = db.Column(db.DateTime, default=datetime.utcnow())
    feedback = db.Column(db.Text)
    state = db.Column(db.Enum(*STATE), default='normal')

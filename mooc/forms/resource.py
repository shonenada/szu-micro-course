from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form
from wtforms import (StringField, SelectField)
from wtforms.validators import InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from mooc.models.course import Category, Lecture
from mooc.models.resource import Resource


class ResourceForm(Form):

    def lectures():
        return Lecture.query.all()

    name = StringField(label=_('Resource Name'), validators=[InputRequired()])
    resource_url = StringField(label=_('URL'), validators=[InputRequired()])
    category = SelectField(
        label=_('Category'),
        choices=[(Resource.RESOURCE_CATEGORY[i], Resource.RESOURCE_CATEGORY[i])
                  for i in xrange(len(Resource.RESOURCE_CATEGORY))],
        validators=[InputRequired(message=_('Please choose the category'))]
    )
    state = SelectField(
        label=u'State',
        choices=[(Resource.RESOURCE_STATE[i],
                  Resource.RESOURCE_STATE[i]) for i in range(0, 2)],
        validators=[InputRequired(message=_("Please choose the state."))]
    )
    lecture = QuerySelectField(query_factory=lectures, allow_blank=False)

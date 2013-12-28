from flask_wtf import Form
from wtforms import (StringField, SelectField)
from wtforms.validators import InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from mooc.course.model import Category, Lecture
from mooc.resource.model import Resource


class ResourceForm(Form):

    def lectures():
        return Lecture.query.all()

    name = StringField(label=u'Name', validators=[InputRequired()])
    resource_url = StringField(label=u'URL', validators=[InputRequired()])
    category = SelectField(
        label = u'Category',
        choices = [(Resource.RESOURCE_CATEGORY[i],
                    Resource.RESOURCE_CATEGORY[i]) for i in range(0, 4)],
        validators = [InputRequired(message=u'Please choose the category')]
    )
    state = SelectField(
        label = u'State',
        choices = [(Resource.RESOURCE_STATE[i],
                    Resource.RESOURCE_STATE[i]) for i in range(0, 2)],
        validators=[InputRequired(message="Please choose the state.")]
    )
    lecture = QuerySelectField(query_factory=lectures, allow_blank=False)

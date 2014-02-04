from flask_wtf import Form
from flask.ext.babel import lazy_gettext as _
from wtforms.validators import InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import (StringField, IntegerField, DateField,
                     TextField, TextAreaField, SelectField)

from mooc.forms.master import TagsField
from mooc.models.master import Tag
from mooc.models.account import Teacher, College
from mooc.models.course import Subject, Course, Category, Lecture
from mooc.models.resource import Resource


subject_state_texts = (_('Normal'), _('Deleted'))
subject_state_values = ('normal', 'deleted')


class SubjectForm(Form):
    name = StringField(label=_('Subject Name'), validators=[InputRequired()])
    description = TextAreaField(label=_('Description'))


class CategoryForm(Form):

    def get_subject():
        return Subject.query.filter(Subject.state != 'deleted').all()

    name = StringField(label=_('Category Name'), validators=[InputRequired()])
    subject = QuerySelectField(query_factory=get_subject, allow_blank=False)


class CourseForm(Form):

    def colleges():
        return College.query.all()

    def teachers():
        return Teacher.query.all()

    def categories():
        return Category.query.filter(Category.state != 'deleted').all()

    name = StringField(label=_('Course Name'), validators=[InputRequired()])
    description = TextAreaField(label=_('Description'))
    logo_url = StringField(label=_('Logo'))
    teacher = QuerySelectField(
        label=_('Teacher'),
        query_factory=teachers, allow_blank=True)
    college = QuerySelectField(
        label=_('College'),
        query_factory=colleges, allow_blank=False)
    category = QuerySelectField(
        label=_('Category'),
        query_factory=categories, allow_blank=False)
    tags = TagsField(label=_('Tags'), tag_model=Tag)


class LectureForm(Form):

    def courses():
        return Course.query.all()

    def teachers():
        return Teacher.query.all()

    name = StringField(label=_('Lecture Name'), validators=[InputRequired()])
    description = TextAreaField(label=_('Description'),
                                validators=[InputRequired()])
    knowledge_point = TextAreaField(label=_('Knowledge Points'))
    prepare_knowledge = TextAreaField(label=_('Prepare Knowledge'))
    term = StringField(label=_('Term'))
    chapter = StringField(label=_('Chapter'))
    record_time = DateField(label=_('Record Time'))
    record_address = StringField(label=_('Record Address'))
    video_url = StringField(label=_('Video URL'))
    video_length = IntegerField(label=_('Video Length (seconds)'))
    logo_url = StringField(label=_('Logo URL'))
    order = IntegerField(label=_('Order of lecture'))
    course = QuerySelectField(
        label=_('Course'),
        query_factory=courses, allow_blank=False)
    teacher = QuerySelectField(
        label=_('Teacher'),
        query_factory=teachers, allow_blank=True)
    tags = TagsField(label=_('Tags'), tag_model=Tag)

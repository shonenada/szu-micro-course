from flask_wtf import Form
from wtforms import (StringField, IntegerField, DateField, TextField, TextAreaField, SelectField)
from wtforms.validators import InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from mooc.master.form import TagsField
from mooc.master.model import Tag
from mooc.account.model import Teacher, College
from mooc.course.model import Subject, Course, Category, Resource, Lecture


subject_state_texts =  ('Normal', 'Deleted')
subject_state_values =  ('normal', 'deleted')


class SubjectForm(Form):
    name = StringField(label=u'Name', validators=[InputRequired()])
    description = TextAreaField(label=u'Description')


class CategoryForm(Form):

    def get_subject():
        return Subject.query.filter(Subject._state != 'deleted').all()

    name = StringField(label=u'Name', validators=[InputRequired()])
    subject = QuerySelectField(query_factory=get_subject, allow_blank=False)


class CourseForm(Form):

    def colleges():
        return College.query.all()

    def teachers():
        return Teacher.query.all()

    def categories():
        return Category.query.filter(Category._state != 'deleted').all()

    name = StringField(label=u'Name', validators=[InputRequired()])
    description = TextAreaField(label=u'Description')
    logo_url = StringField(label=u'Logo')
    teacher = QuerySelectField(query_factory=teachers, allow_blank=True)
    college = QuerySelectField(query_factory=colleges, allow_blank=False)
    category = QuerySelectField(query_factory=categories, allow_blank=False)
    tags = TagsField(tag_model=Tag, label=u'Tags')


class LectureForm(Form):

    def courses():
        return Course.query.all()

    def teachers():
        return Teacher.query.all()

    name = StringField(label=u'Name', validators=[InputRequired()])
    description = TextAreaField(label=u'Description',
                                validators=[InputRequired()])
    knowledge_point = TextAreaField(label=u'Knowledge Points')
    prepare_knowledge = TextAreaField(label=u'Prepare Knowledge')
    term = StringField(label=u'Term')
    chapter = StringField(label=u'Chapter')
    record_time = DateField(label=u'Record Time')
    record_address = StringField(label=u'Record Address')
    video_url = StringField(label=u'Video URL')
    video_length = IntegerField(label=u'Video Length (seconds)')
    logo_url = StringField(label=u'Logo URL')
    order = IntegerField(label=u'Order of lecture')
    course = QuerySelectField(query_factory=courses, allow_blank=False)
    teacher = QuerySelectField(query_factory=teachers, allow_blank=True)
    tags = TagsField(tag_model=Tag, label=u'Tags')


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

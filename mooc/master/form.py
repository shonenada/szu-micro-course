from flask.ext.babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.fields import Field
from wtforms.widgets import TextInput
from wtforms.validators import InputRequired, Length


class TagsField(Field):
    """Add a custom Field class.

    This field is designed for tags.
    It will get tags' object according to data in *form_data*.

    :param tag_model: The model of Tag.
    :param label: Label of this field.
    :param validators: Decide validators for this field.
    :param sep: How to seperate tags. Blank by default.
    """
    widget = TextInput()

    def __init__(self, tag_model, label='', validators=None, **kwargs):
        super(TagsField, self).__init__(label, validators, **kwargs)
        self.tag_model = tag_model
        self.sep = kwargs.pop('sep', u' ')

    def _value(self):
        if self.data:
            return self.sep.join([tag.tag for tag in self.data])
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = []
            form_data = valuelist[0].split(self.sep)
            for tag in form_data:
                if not tag.strip():
                    continue
                q_tag = self.tag_model.query.filter_by(tag=tag).first()

                if not q_tag:
                    q_tag = self.tag_model(tag)
                self.data.append(q_tag)
        else:
            self.data = []
            self.data = list(self._remove_duplicates(self.data))

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive,
        but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item


class FeedbackForm(Form):
    title = StringField(
        label=_('Title'),
        validators=[
            InputRequired(),
            Length(max=20),
        ],
    )
    feedback = TextAreaField(
        label=_('Feedback'),
        validators=[
            InputRequired(),
        ]
    )
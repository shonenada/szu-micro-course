#-*-coding: utf-8 -*-
from flask.ext.babel import lazy_gettext as _

from mooc.models.resource import Resource


def create_resource(data):
    resource = Resource(data['name'])
    resource.resource_url = data['resource_url']
    resource.category = data['category']
    resource.state = data['state']
    resource.lecture = data['lecture']
    db.session.add(resource)
    db.session.commit()


def friendly_resource_category(category):
    RESOURCE_CATEGORY = {'ppt': _('PPT'),
                         'doc': _('Docuement'),
                         'pdf': _('PDF'),
                         'video': _('Video'),
                         'other': _('Other')}
    if category in RESOURCE_CATEGORY.keys():
        return RESOURCE_CATEGORY[category]
    else:
        return _('Other')

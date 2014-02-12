#-*-coding: utf-8 -*-
from flask.ext.babel import lazy_gettext as _

from mooc.models.resource import Resource


def create_resource(data):
    resource = Resource(
        name=data['name'],
        resource_url=data['resource_url'],
        type=data['type'],
        state=data['state'],
        lecture=data['lecture']
        )
    resource.save()


def friendly_resource_category(category):
    RESOURCE_TYPE = {'ppt': _('PPT'),
                     'doc': _('Docuement'),
                     'pdf': _('PDF'),
                     'video': _('Video'),
                     'other': _('Other')}
    if category in RESOURCE_TYPE.keys():
        return RESOURCE_TYPE[category]
    else:
        return _('Other')

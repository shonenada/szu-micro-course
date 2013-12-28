#-*-coding: utf-8 -*-
from mooc.resource.model import Resource


def create_resource(data):
    resource = Resource(data['name'])
    resource.resource_url = data['resource_url']
    resource.category = data['category']
    resource.state = data['state']
    resource.lecture = data['lecture']
    db.session.add(resource)
    db.session.commit()


def friendly_resource_category(category):
    RESOURCE_CATEGORY = {'ppt': u'演示文稿',
                         'doc': u'文档',
                         'pdf': u'PDF',
                         'video': u'视频',
                         'other': u'其他'}
    if category in RESOURCE_CATEGORY.keys():
        return RESOURCE_CATEGORY[category]
    else:
        return u'其他'

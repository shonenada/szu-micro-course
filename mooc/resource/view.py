from flask import Blueprint, render_template, request

from mooc.app import db, rbac
from mooc.resource.model import Resource

resource_app = Blueprint('resource', __name__, template_folder='../templates')


@resource_app.route('/resource')
@rbac.allow(['anonymous'], ['GET'])
def list():
    page_num = int(request.args.get('page', 1))
    resource_query = (Resource.query.filter(Resource.state != 'DELETED')
                              .order_by(Resource.created.desc()))
    resources = resource_query.paginate(page_num, per_page=20)
    hot_resources = Resource.query.order_by(Resource.view_count
                                                    .desc()).limit(30).all()
    return render_template('resource/list.html',
                           pagination=resources,
                           hot_resources=hot_resources)

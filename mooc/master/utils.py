from flask import request, render_template, current_app, jsonify

from mooc.app import rbac
from mooc.helpers import flash


def create_object():
    pass


def generate_endpoints(module_name):
    endpoints = {
        'list': 'master.master_%s_list' % module_name,
        'create': 'master.master_%s_new' % module_name,
        'edit': 'master.master_%s_edit' % module_name,
        'delete': 'master.master_%s_delete' % module_name,
    }
    return endpoints


def _get_endpoint(module_name, action):
    endpoints = generate_endpoints(module_name)
    return endpoints[action].split('.', 1)[1]


def generate_list_controller(blueprint, model, **kwargs):
    module_name = model.__name__.lower()

    @blueprint.route(
        rule='/master/%s' % module_name,
        methods=['GET'],
        endpoint=_get_endpoint(module_name, 'list')
    )
    @rbac.allow(['super_admin'], ['GET'])
    def list_controller():
        page_num = int(request.args.get('page', 1))
        pagination= model.paginate(
            page=page_num,
            per_page=current_app.config.get('ADMIN_PAGESIZE')
        )
        return render_template(
            'admin/%s_list.html' % module_name,
            pagination=pagination,
            model_name=model.__name__,
            endpoints=generate_endpoints(module_name)
        )


def generate_create_controller(blueprint, model, form_model, **kwargs):
    module_name = model.__name__.lower()

    @blueprint.route(
        rule='/master/%s/new' % module_name,
        methods=['GET', 'POST'],
        endpoint=_get_endpoint(module_name, 'create')
    )
    @rbac.allow(['super_admin'], ['GET', 'POST'])
    def create_controller():
        form = form_model()
        create_method = kwargs.get('create_method')
        if form.validate_on_submit():
            if create_method:
                create_method(form.data)
            else:
                create_object(model, form.data)
            flash(message='Operated successfully', category='notice')
            return jsonify(success=True)
        if form.errors:
            return jsonify(success=False, messages=form.errors.values())
        return render_template(
            'admin/%s_new.html' % module_name,
            form=form,
            model_name=model.__name__,
            endpoints=generate_endpoints(module_name)
        )


def generate_edit_controller(blueprint, model, form_model, **kwargs):
    module_name = model.__name__.lower()

    @blueprint.route(
        rule='/master/%s/<int:mid>/edit' % module_name,
        methods=['GET', 'PUT'],
        endpoint=_get_endpoint(module_name, 'edit')
    )
    @rbac.allow(['super_admin'], ['GET', 'PUT'])
    def edit_controller(mid):
        obj = model.query.get(mid)
        form_args = kwargs.get('form_args', None)
        if form_args:
            form = form_model(request.form, obj, **form_args)
        else:
            form = form_model(request.form, obj)
        if form.validate_on_submit():
            obj.edit(form.data, **kwargs)
            flash('Operated successfully!', 'notice')
            return jsonify(success=True)
        if form.errors:
            return jsonify(success=False, messages=form.errors.values())
        return render_template(
            'admin/%s_edit.html' % module_name,
            mid=mid,
            form=form,
            model_name=model.__name__,
            endpoints=generate_endpoints(module_name)
        )


def generate_delete_controller(blueprint, model, **kwargs):
    module_name = model.__name__.lower()

    @blueprint.route(
        rule='/master/%s/<int:mid>' % module_name,
        methods=['DELETE'],
        endpoint=_get_endpoint(module_name, 'delete')
    )
    @rbac.allow(['super_admin'], ['DELETE'])
    def delete_controller(mid):
        obj = model.query.get(mid)
        obj.delete()
        flash(message='Operated successfully!', category='notice')
        return jsonify(success=True)


def generate_all_controller(blueprint, model, form_model, **kwargs):
    generate_list_controller(blueprint, model, **kwargs)
    generate_create_controller(blueprint, model, form_model,  **kwargs)
    generate_edit_controller(blueprint, model, form_model, **kwargs)
    generate_delete_controller(blueprint, model, **kwargs)

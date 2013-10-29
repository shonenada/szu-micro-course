from flask import Blueprint, render_template


master_app = Blueprint('master', __name__, template_folder='../templates')


@master_app.route('/')
def index():
    return "Hello MOOC."

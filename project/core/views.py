from flask import render_template, Blueprint, request

core_bp = Blueprint('core', __name__, template_folder='templates/core')

@core_bp.route('/')
def index():
   return render_template('index.html')


@core_bp.route('/about')
def about():
   return render_template('about.html')
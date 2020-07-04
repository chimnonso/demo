from flask import render_template, Blueprint, request
from project.models import BlogPost

core_bp = Blueprint('core', __name__, template_folder='templates/core')

@core_bp.route('/')
def index():
   blog_posts = BlogPost.query.order_by(BlogPost.created_on.desc())
   return render_template('index.html', blog_posts=blog_posts)


@core_bp.route('/about')
def about():
   return render_template('about.html')
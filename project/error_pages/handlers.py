from flask import Blueprint, render_template


error_pages = Blueprint('error_pages', __name__, template_folder="templates/error_pages")


@error_pages.app_errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404
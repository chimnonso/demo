from flask import Flask

from project.core.views import core_bp
from project.error_pages.handlers import error_pages

app = Flask(__name__)
app.register_blueprint(core_bp)
app.register_blueprint(error_pages)
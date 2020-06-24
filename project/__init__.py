from flask import Flask

from project.core.views import core_bp


app = Flask(__name__)
app.register_blueprint(core_bp)
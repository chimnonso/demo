import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
###################################
####### DATABASE ##################
###################################

basedir = os.path.abspath(os.path.dirname(__file__))
secret_key = os.urandom(16)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
print(basedir)


###################################
####### LOGIN ##################
###################################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
# login_manager.login_message_category


from project.core.views import core_bp
from project.error_pages.handlers import error_pages
from project.users.views import users
app.register_blueprint(core_bp)
app.register_blueprint(users)
app.register_blueprint(error_pages)
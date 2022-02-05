from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_principal import identity_loaded, Principal, UserNeed, RoleNeed

db = SQLAlchemy()

DB_NAME = 'employeeinformation.db'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'files')


def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = '201 File System Key'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024    # 50 Mb limit
	#app.config["CACHE_TYPE"] = "null"
	# change to "redis" and restart to cache again

	db.init_app(app)
	
	# ---------------------------------------------------------------------------- #
	#                            BULEPRINT REGISTRATION                            #
	# ---------------------------------------------------------------------------- #

	from .auth import auth
	from .views import views
	from .employees import employees
	from .tokenVerifier import tokenizer
	from .csEligibility import cse
	from .vocationalCourse import vocation
	from .learningDevelopment import ld
	from .vaccination import vaccine
	from .familyBg import familyBg
	from .college import college



	app.register_blueprint(auth, url_prefix='/')
	app.register_blueprint(views, url_prefix ='/')
	app.register_blueprint(employees, url_prefix ='/employees')
	app.register_blueprint(tokenizer, url_prefix = '/tokenizer')
	app.register_blueprint(cse, url_prefix = '/cse')
	app.register_blueprint(vocation, url_prefix = '/vocation')
	app.register_blueprint(ld, url_prefix = '/ld')
	app.register_blueprint(vaccine, url_prefix = '/vaccine')
	app.register_blueprint(familyBg, url_prefix = '/familyBg')
	app.register_blueprint(college, url_prefix = '/college')

	# ---------------------------- END OF REGISTRATION --------------------------- #

	from .models import User

	create_database(app)
	
	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	principals = Principal()
	principals.init_app(app)

	@identity_loaded.connect_via(app)
	def on_identity_loaded(sender, identity):
		identity.user = current_user
		if hasattr(current_user, 'id'):
			identity.provides.add(UserNeed(current_user.id))
		if hasattr(current_user, 'type_of_user'):
			identity.provides.add(RoleNeed(str(current_user.type_of_user)))

	return app



def create_database(app):
	#if not path.exists('website/'+DB_NAME):
	db.create_all(app=app)
	print ('Database Created!')
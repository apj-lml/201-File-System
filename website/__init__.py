from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
import os
from flask_principal import identity_loaded, Principal, UserNeed, RoleNeed
import jinja2
from datetime import datetime
from flask_marshmallow import Marshmallow


# from website.models import User

# from flask_babel import Babel


# db = SQLAlchemy(session_options={"autoflush": False})
db = SQLAlchemy()
ma = Marshmallow()

#sqlite
#DB_NAME = 'employeeinformation.db'

#mysql
DB_NAME = 'employeeinformation'
DB_USERNAME = 'aljohnjacinto'
DB_HOST = 'aljohnjacinto.mysql.pythonanywhere-services.com'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'files')


def create_app():
	
	app = Flask(__name__)
	app.config['SECRET_KEY'] = '201 File System Key'

	#sqlite database
	# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

	#mysql database offline
	# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:rootpassword@localhost/{DB_NAME}'

	# #mysql database online
	app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:rootpassword@{DB_HOST}/aljohnjacinto${DB_NAME}'

	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	app.config['MAX_CONTENT_LENGTH'] = 250 * 1024 * 1024    # 250 Mb limit

	# app.config.from_pyfile('mysettings.cfg')
	
	# babel.init_app(babel)
	#app.config["CACHE_TYPE"] = "null"
	# change to "redis" and restart to cache again

	db.init_app(app)
	ma.init_app(app)
	
	_js_escapes = {
        '\\': '\\u005C',
        '\'': '\\u0027',
        '"': '\\u0022',
        '>': '\\u003E',
        '<': '\\u003C',
        '&': '\\u0026',
        '=': '\\u003D',
        '-': '\\u002D',
        ';': '\\u003B',
        u'\u2028': '\\u2028',
        u'\u2029': '\\u2029'
	}

	# Escape every ASCII character with a value less than 32.
	_js_escapes.update(('%c' % z, '\\u%04X' % z) for z in range(32))

	def escapejs(value):
		return jinja2.Markup("".join(_js_escapes.get(l, l) for l in value))

	@app.template_filter('format_mydatetime')
	def format_mydatetime(value):
		if value == 'PRESENT':
			return value
		elif value == 'N/A' or value ==  None:
			return 'N/A'
		elif value == '' or value ==  None:
			return 'N/A'
		else:
			mydatetime = datetime.strptime(value, '%Y-%m-%d')
			return mydatetime.strftime("%m/%d/%Y")

	@app.template_filter('format_mydatetime_2')
	def format_mydatetime(value):
		if value == 'PRESENT':
			return value
		elif value == 'N/A' or value ==  None:
			return 'N/A'
		elif value == '' or value ==  None:
			return 'N/A'
		else:
			mydatetime = datetime.strptime(value, '%Y-%m-%d')
			return mydatetime.strftime("%B %d, %Y")

	# @app.template_filter('query_units')
	# def query_units(value):
	# 	agency_section = Agency_Section.query.filter_by(agency_section = value).all()
	# 	each_section = ""
	# 	for section in agency_section:
	# 		each_section = f"<option value='ADMINISTRATIVE UNIT'>ADMINISTRATIVE UNIT</option>"

	# 	return mydatetime.strftime("%m/%d/%Y")

	app.jinja_env.filters['escapejs'] = escapejs
	# app.jinja_env.filters['format_datetime'] = format_datetime

	# ---------------------------------------------------------------------------- #
	#                            BLUEPRINT REGISTRATION                            #
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
	from .masteral import masteral
	from .doctoral import doctoral
	from .shirt import shirt
	from .workExperience import workExperience
	from .voluntaryWork import voluntaryWork
	from .otherInformation import otherInformation
	from .questions import questions
	from .otherQuestions import otherQuestions
	from .characterReference import characterReference
	from .emergencyContact import emergencyContact
	from .appointment import appointment
	from .staff_movement import staff_movement
	from .downloadableForms import DownloadableForms
	from .listOfExpiry import listOfExpiry
	from .systemSettings import systemSettings
	from .agencyUnit import agencyUnit
	from .wes import wes
	from .afl import afl
	from .rol import rol
	from .listOfLoyaltyAwardees import listOfLoyaltyAwardees
	from .listOfRetirees import listOfRetirees


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
	app.register_blueprint(masteral, url_prefix = '/masteral')
	app.register_blueprint(doctoral, url_prefix = '/doctoral')
	app.register_blueprint(shirt, url_prefix = '/shirt')
	app.register_blueprint(workExperience, url_prefix = '/workExperience')
	app.register_blueprint(voluntaryWork, url_prefix = '/voluntaryWork')
	app.register_blueprint(otherInformation, url_prefix = '/otherInformation')
	app.register_blueprint(questions, url_prefix = '/questions')
	app.register_blueprint(otherQuestions, url_prefix = '/otherQuestions')
	app.register_blueprint(characterReference, url_prefix = '/characterReference')
	app.register_blueprint(emergencyContact, url_prefix = '/emergencyContact')
	app.register_blueprint(appointment, url_prefix = '/appointment')
	app.register_blueprint(staff_movement, url_prefix = '/staff_movement')
	app.register_blueprint(DownloadableForms, url_prefix = '/forms')
	app.register_blueprint(listOfExpiry, url_prefix = '/listOfExpiry')
	app.register_blueprint(systemSettings, url_prefix = '/systemSettings')
	app.register_blueprint(agencyUnit, url_prefix = '/agencyUnit')
	app.register_blueprint(wes, url_prefix = '/wes')
	app.register_blueprint(afl, url_prefix = '/afl')
	app.register_blueprint(rol, url_prefix = '/rol')
	app.register_blueprint(listOfLoyaltyAwardees, url_prefix = '/listOfLoyaltyAwardees')
	app.register_blueprint(listOfRetirees, url_prefix = '/listOfRetirees')



	# ---------------------------- END OF REGISTRATION --------------------------- #


	from .models import Agency_Section, User

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
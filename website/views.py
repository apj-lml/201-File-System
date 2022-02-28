from gc import collect
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, logout_user, login_required
#from flask.ext.principal import Principal, Permission, RoleNeed
from flask_principal import Principal, Permission, RoleNeed

from . import db
from .models import College, Family_Background, Masteral, User, Vocational_Course

views = Blueprint('views', __name__)

admin_permission = Permission(RoleNeed('admin'))

@views.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

@views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	return render_template('dashboard.html')

@views.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def admin_dashboard():
	return render_template('admin-dashboard.html')

@views.route('/learning-development/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def learning_development(emp_id):
	user = db.session.query(User).get(emp_id)
	return render_template('learning_development.html', emp_id = emp_id, user_profile = user)

@views.route('/family-background/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def family_background(emp_id):
	user = db.session.query(User).get(int(emp_id))
	return render_template('family_bg.html', emp_id = emp_id, user_profile = user)

@views.route('/covid-vaccine/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def covid_vaccine(emp_id):
	user = db.session.query(User).get(int(emp_id))
	return render_template('vaccination.html', emp_id = emp_id, user_profile = user)

@views.route('/change-password/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def change_password(emp_id):
	user = db.session.query(User).get(int(emp_id))
	return render_template('change_password.html', emp_id = emp_id, user_profile = user)

@views.route('/tshirt-sizes/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def shirt_size(emp_id):
	user = db.session.query(User).get(int(emp_id))
	return render_template('t_shirt_sizes.html', emp_id = emp_id, user_profile = user)

@views.route('/work-experience/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def work_experience(emp_id):
	user = db.session.query(User).get(int(emp_id))
	return render_template('work_experience.html', emp_id = emp_id, user_profile = user)

@views.route('/voluntary-work/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def voluntary_work(emp_id):
	user = db.session.query(User).get(int(emp_id))
	return render_template('voluntary_work.html', emp_id = emp_id, user_profile = user)

@views.route('/other-information/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def other_information(emp_id):
	user = db.session.query(User).get(int(emp_id))
	return render_template('other_information.html', emp_id = emp_id, user_profile = user)

@views.route('/questions/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def questions(emp_id):
	user = db.session.query(User).get(int(emp_id))
	return render_template('questions.html', emp_id = emp_id, user_profile = user)

@views.route('/character-reference/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def character_reference(emp_id):
	user = db.session.query(User).get(int(emp_id))
	return render_template('character_reference.html', emp_id = emp_id, user_profile = user)

@views.route('/print-preview/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def print_preview(emp_id):
	user = db.session.query(User).get(int(emp_id))
	spouse = db.session.query(Family_Background).filter_by(user_id = emp_id, fb_relationship = "SPOUSE")
	father = db.session.query(Family_Background).filter_by(user_id = emp_id, fb_relationship = "FATHER")
	mother = db.session.query(Family_Background).filter_by(user_id = emp_id, fb_relationship = "MOTHER")
	child = db.session.query(Family_Background).filter_by(user_id = emp_id, fb_relationship = "CHILD")
	vocation = db.session.query(Vocational_Course).filter_by(user_id = emp_id)
	college = db.session.query(College).filter_by(user_id = emp_id)
	masteral = db.session.query(Masteral).filter_by(user_id = emp_id)

	return render_template('print_preview.html', emp_id = emp_id,
	 	user_profile = user,
		spouse = spouse, 
		child = child, 
		father = father, 
		mother = mother,
		vocation = vocation,
		college = college,
		masteral = masteral
		)

@views.route('/emergency-contact/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def emergency_contact(emp_id):
	user = db.session.query(User).get(int(emp_id))
	
	return render_template('emergency_contact.html', emp_id = emp_id, user_profile = user)
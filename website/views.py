from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, logout_user, login_required
#from flask.ext.principal import Principal, Permission, RoleNeed
from flask_principal import Principal, Permission, RoleNeed

from . import db
from .models import Family_Background, User

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
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Career_Service, College, Doctoral, Learning_Development, Masteral, Service_Record, User, Uploaded_File, Vaccine, Vocational_Course
from . import db
#from datetime import datetime
import datetime
from .myhelper import allowed_file, my_random_string
from werkzeug.utils import secure_filename
import os, os.path
import json

staff_movement = Blueprint('staff_movement', __name__)

admin_permission = Permission(RoleNeed('admin'))

@staff_movement.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

@staff_movement.route('get-employees/<emp_id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_employees(emp_id):
	if request.method == 'GET' and emp_id == "0" :
		user = User.query.all()
		column_keys = User.__table__.columns.keys()
	# Temporary dictionary to keep the return value from table
		rows_dic_temp = {}
		rows_dic = []
	# Iterate through the returned output data set
		for row in user:
			for col in column_keys:
				rows_dic_temp[col] = getattr(row, col)
			rows_dic.append(rows_dic_temp)
			rows_dic_temp= {}
			# print(rows_dic)
		return jsonify(rows_dic)
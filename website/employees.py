from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Service_Record, User, Uploaded_File
from . import db
from datetime import datetime
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import os, os.path
import json
ALLOWED_EXTENSIONS = {'pdf'}

employees = Blueprint('employees', __name__)

admin_permission = Permission(RoleNeed('admin'))

@employees.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))


@employees.route('get-employees/<emp_id>', methods=['POST', 'GET'])
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
		return jsonify(rows_dic)
	#else:
	# 	user = User.query.filter_by(id = emp_id)
	# 	column_keys = User.__table__.columns.keys()
	# # Temporary dictionary to keep the return value from table
	# 	rows_dic_temp = {}
	# 	rows_dic = []
	# # Iterate through the returned output data set
	# 	for row in user:
	# 		for col in column_keys:
	# 			rows_dic_temp[col] = getattr(row, col)
	# 		rows_dic.append(rows_dic_temp)
	# 		rows_dic_temp= {}
	# 	return redirect(url_for('employees.my_profile',  user_profile = rows_dic))

@employees.route('my-profile/<emp_id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def my_profile(emp_id):
	
	if request.method == 'GET':
		user = User.query.get(emp_id)
		#print(user.id)
		
		return render_template('employee_profile.html', user_profile = user)

	return jsonify({})


@employees.route('update-employee/<emp_id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_employee(emp_id):
	formdata = request.form.to_dict()

	user = db.session.query(User).get(emp_id)

	if formdata['date_of_validity'] != '':
		formdata['date_of_validity'] = datetime.strptime(formdata['date_of_validity'], '%Y-%m-%d').date()
	else:
		formdata['date_of_validity'] = None

	formdata['birthdate'] = datetime.strptime(formdata['birthdate'], '%Y-%m-%d').date()

	final_name = ''
	for afile in request.files:
		file = request.files[afile]

		#print(f'print file: {afile}')
		if file.filename == "":
		#if afile not in request.files:
			print('No file selected part')
			#return redirect(request.url)
		else:
			if not file and allowed_file(file.filename):
				print('Invalid file submitted')
				#return redirect(request.url)
			else:
				today_is = datetime.today().strftime('%Y-%m-%d-%H%M%S')
				file_extension = file.filename.rsplit('.', 1)[1].lower()
				file_name = file.filename.rsplit('.', 1)[0]
				final_name = secure_filename(afile+'_'+ formdata['last_name']+'_'+formdata['first_name'] + '_' + formdata['employee_id']+'_' + today_is +'_' + file_name +'.'+file_extension)
				
				# my_file = Path(current_app.config['UPLOAD_FOLDER']+'\\'+final_name)
				# if my_file.is_file():
				# 	print('file already exist')

				if os.path.isfile(current_app.config['UPLOAD_FOLDER']):
					print('path does not exist... creating path')
					os.mkdir(current_app.config['UPLOAD_FOLDER'])
				else:
					print('path exist!')
					file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], final_name))

					#saving upload info to database
					files_to_upload = Uploaded_File(file_name = final_name, file_path = "\\static\\files\\", file_tag = afile, user_id = emp_id)
					db.session.add(files_to_upload)
					db.session.commit()

	formdata.pop('employee_id')
	#code for automated update
	for key, value in formdata.items(): 
			if type(value) is datetime.date:
				setattr(user, key, value.upper())
				print(value)
	db.session.commit()
	#end update

	return redirect(request.referrer)

@employees.route('delete-file', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def delete_file():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		
		my_file = Uploaded_File.query.get(formdata['file_id'])
		print(my_file)
		os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], my_file.file_name))
		db.session.delete(my_file)
		db.session.commit()
	return jsonify('{message: File Deleted Successfully}')

@employees.route('service-record/<emp_id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def service_record(emp_id):
	user = db.session.query(User).get(emp_id)
	if request.method == "POST":
		formdata = request.form.to_dict()
		if 'sf_present' in formdata:
			formdata['service_to'] = 'Present'
			formdata.pop('sf_present')
		formdata['user_id'] = emp_id
		new_service_record = Service_Record(**formdata)
		db.session.add(new_service_record)
		db.session.commit()
		return redirect(url_for('employees.service_record', emp_id = emp_id, user=user))
	return render_template('service_record.html', emp_id = emp_id, user=user)


@employees.route('get-service-record/<emp_id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_service_record(emp_id):
	if request.method == "GET":

		new_service_record = Service_Record.query.filter_by(user_id = emp_id).all()
		column_keys = Service_Record.__table__.columns.keys()
	# Temporary dictionary to keep the return value from table
		rows_dic_temp = {}
		rows_dic = []
	# Iterate through the returned output data set
		for row in new_service_record:
			for col in column_keys:
				rows_dic_temp[col] = getattr(row, col)
			rows_dic.append(rows_dic_temp)
			rows_dic_temp= {}
			print(rows_dic)
		return jsonify(rows_dic)

	return render_template('service_record.html', emp_id = emp_id)

@employees.context_processor
def inject_today_date():
    return {'today_date': datetime.utcnow()}
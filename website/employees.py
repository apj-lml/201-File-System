from genericpath import commonprefix
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import User, Uploaded_File
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


@employees.route('get-employees', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_employees():
	
	if request.method == 'GET':
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

	return jsonify({})

@employees.route('my-profile', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def my_profile():
	
	if request.method == 'GET':
		user = User.query.filter_by(id = current_user.id)

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
		return render_template('employee_profile.html', user_profile = current_user)

	return jsonify({})


@employees.route('update-employee', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_employee():
	formdata = request.form.to_dict()
	files = request.files
	user = db.session.query(User).get(current_user.id)

	if formdata['date_of_validity'] != '':
		formdata['date_of_validity'] = datetime.strptime(formdata['date_of_validity'], '%Y-%m-%d').date()
	else:
		formdata['date_of_validity'] = None
	formdata['birthdate'] = datetime.strptime(formdata['birthdate'], '%Y-%m-%d').date()
	#code for automated update
	for key, value in formdata.items(): 
		setattr(user, key, value)

	db.session.commit()
	#end update

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
					files_to_upload = Uploaded_File(file_name = final_name, file_path = "\\static\\files\\", file_tag = afile, user_id = current_user.id)
					db.session.add(files_to_upload)
					db.session.commit()

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
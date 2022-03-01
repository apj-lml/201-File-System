
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Career_Service, College, Doctoral, Learning_Development, Masteral, Service_Record, User, Uploaded_File, Vaccine, Vocational_Course
from . import db
#from datetime import datetime
import datetime
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import os, os.path
import json
from werkzeug.security import generate_password_hash, check_password_hash

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
			# print(rows_dic)
		return jsonify(rows_dic)


@employees.route('my-profile/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def my_profile(emp_id):
	
	if request.method == 'GET':
		print("EMPLOYEE ID: ", emp_id)
		if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
			return "PAGE NOT FOUND", 404
		else:
			user = User.query.get(emp_id)
		# print(user)
		
		return render_template('employee_profile.html', user_profile = user)

	return jsonify({})


@employees.route('update-employee/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def update_employee(emp_id):
	formdata = request.form.to_dict()

	user = db.session.query(User).get(emp_id)

	formdata['birthdate'] = datetime.datetime.strptime(formdata['birthdate'], '%Y-%m-%d').date()

# ---------------------------------------------------------------------------- #
#                              UPLOADING OF FILE                               #
# ---------------------------------------------------------------------------- #
	final_name = ''
	for afile in request.files:
		files = request.files.getlist(afile)

		# print(f'print file: {file}')
		for file in files:
			print(f'print file: {file}')

			if file.filename == "":
			#if afile not in request.files:
				print('No file selected')
				#return redirect(request.url)
			else:
				if not allowed_file(file.filename):
					print('Invalid file submitted')
					return jsonify('Invalid File Submitted! Only PDF Files are allowed'), 406
					#return redirect(request.url)
				else:
					today_is = datetime.datetime.today().strftime('%Y-%m-%d-%H%M%S')
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
# ---------------------------------------------------------------------------- #
#                              END OF FILE UPLOAD                              #
# ---------------------------------------------------------------------------- #

	formdata = formdata.copy()

	cs_update_no_fields = formdata['cs_update_no_fields']
	college_no_update_fields = formdata['college_no_update_fields']
	masteral_no_update_fields = formdata['masteral_no_update_fields']
	vocational_no_update_fields = formdata['vocational_no_update_fields']
	doctoral_no_update_fields = formdata['doctoral_no_update_fields']


# ---------------------------------------------------------------------------- #
#              popping unnecessary data before saving to database              #
# ---------------------------------------------------------------------------- #


	formdata.pop('employee_id')

# ---------------------------------------------------------------------------- #
#                                CAPITALIZE DATA                               #
# ---------------------------------------------------------------------------- #
	for k,v in formdata.items():
		if type(v) is str:
			formdata.update({k: v.upper()})
		else:
			formdata.update({k: v})
		# print(k, v)
# ---------------------------------------------------------------------------- #
#                         UPDATING OF EMPLOYEE PROFILE                         #
# ---------------------------------------------------------------------------- #
	print(formdata)
	
	#code for automated update
	for key, value in formdata.items(): 
		setattr(user, key, value)
	db.session.commit()


# ---------------------------------------------------------------------------- #
#                         UPDATING OF VOCATIONAL COURSE                        #
# ---------------------------------------------------------------------------- #
	for xy in range(1, int(vocational_no_update_fields)+1):
		
		vocational_course = Vocational_Course.query.filter_by(id = formdata['v_id['+str(xy)+']'])
		vocational_course.update(dict(v_school = formdata['v_school['+str(xy)+']'].upper(), 
								vocational_trade_course = formdata['vocational_trade_course['+str(xy)+']'].upper(), 
								v_period_of_attendance_from = formdata['v_period_of_attendance_from['+str(xy)+']'].upper(),
								v_period_of_attendance_to = formdata['v_period_of_attendance_to['+str(xy)+']'].upper(),
								v_highest_level = formdata['v_highest_level['+str(xy)+']'].upper(),
                				v_highest_grade_year_units = formdata['v_highest_grade_year_units['+str(xy)+']'],
								v_scholarship_academic_honor = formdata['v_scholarship_academic_honor['+str(xy)+']'].upper()))


		db.session.commit()
# ---------------------------------------------------------------------------- #
#                                UPDATING OF CSE                               #
# ---------------------------------------------------------------------------- #
	for xy in range(1, int(cs_update_no_fields)+1):
		
		cse = Career_Service.query.filter_by(id = formdata['cse_id['+str(xy)+']'])
		cse.update(dict(cs_eligibility = formdata['cs_eligibility['+str(xy)+']'].upper(), 
						cs_rating = formdata['cs_rating['+str(xy)+']'].upper(), 
						date_of_examination = formdata['date_of_examination['+str(xy)+']'], 
						place_of_examination_conferment = formdata['place_of_examination_conferment['+str(xy)+']'].upper(),
						license_no = formdata['license_no['+str(xy)+']'].upper(), 
						date_of_validity = formdata['date_of_validity['+str(xy)+']']))

		db.session.commit()

# ---------------------------------------------------------------------------- #
#                            UPDATING OF COLLEGE                               #
# ---------------------------------------------------------------------------- #
	for xy in range(1, int(college_no_update_fields)+1):
		
		college = College.query.filter_by(id = formdata['college_id['+str(xy)+']'])
		college.update(dict(
						c_school = formdata['c_school['+str(xy)+']'].upper(), 
						c_degree_course = formdata['c_degree_course['+str(xy)+']'], 
						c_period_of_attendance_from = formdata['c_period_of_attendance_from['+str(xy)+']'].upper(),
						c_period_of_attendance_to = formdata['c_period_of_attendance_to['+str(xy)+']'].upper(), 
						c_highest_level_units_earned = formdata['c_highest_level_units_earned['+str(xy)+']'].upper(),
						c_highest_grade_year_units = formdata['c_highest_grade_year_units['+str(xy)+']'].upper(),
						c_scholarship_academic_honor = formdata['c_scholarship_academic_honor['+str(xy)+']'].upper(),
						))

		db.session.commit()

# ---------------------------------------------------------------------------- #
#                           UPDATING OF MASTERAL                               #
# ---------------------------------------------------------------------------- #
	for xy in range(1, int(masteral_no_update_fields)+1):
		
		masteral = Masteral.query.filter_by(id = formdata['gs_id['+str(xy)+']'])
		masteral.update(dict(
						gs_school = formdata['gs_school['+str(xy)+']'].upper(), 
						gs_degree_course = formdata['gs_degree_course['+str(xy)+']'], 
						gs_period_of_attendance_from = formdata['gs_period_of_attendance_from['+str(xy)+']'].upper(),
						gs_period_of_attendance_to = formdata['gs_period_of_attendance_to['+str(xy)+']'].upper(), 
						gs_highest_level_units_earned = formdata['gs_highest_level_units_earned['+str(xy)+']'].upper(),
						gs_highest_grade_year_units = formdata['gs_highest_grade_year_units['+str(xy)+']'].upper(),
						gs_scholarship_academic_honor = formdata['gs_scholarship_academic_honor['+str(xy)+']'].upper(),
						))

		db.session.commit()

# ---------------------------------------------------------------------------- #
#                           UPDATING OF DOCTORAL                               #
# ---------------------------------------------------------------------------- #
	for xy in range(1, int(doctoral_no_update_fields)+1):
		
		doctoral = Doctoral.query.filter_by(id = formdata['doctoral_id['+str(xy)+']'])
		doctoral.update(dict(
						doc_school = formdata['doc_school['+str(xy)+']'].upper(), 
						doc_degree_course = formdata['doc_degree_course['+str(xy)+']'], 
						doc_period_of_attendance_from = formdata['doc_period_of_attendance_from['+str(xy)+']'].upper(),
						doc_period_of_attendance_to = formdata['doc_period_of_attendance_to['+str(xy)+']'].upper(), 
						doc_highest_level_units_earned = formdata['doc_highest_level_units_earned['+str(xy)+']'].upper(),
						doc_highest_grade_year_units = formdata['doc_highest_grade_year_units['+str(xy)+']'].upper(),
						doc_scholarship_academic_honor = formdata['doc_scholarship_academic_honor['+str(xy)+']'].upper(),
						))

		db.session.commit()

# ---------------------------------------------------------------------------- #
#                        UPDATE LEARNING AND DEVELOPMENT                       #
# ---------------------------------------------------------------------------- #
	# for xy in range(1, int(ld_update_no_fields)+1):
	# 	print("SOMETING IN HERE")
		
	# 	ld = Learning_Development.query.filter_by(id = formdata['ld_id['+str(xy)+']'])
	# 	ld.update(dict(ld_program = formdata['ld_program['+str(xy)+']'].upper(), ld_date_from = formdata['ld_date_from['+str(xy)+']'].upper(), ld_date_to = formdata['ld_date_to['+str(xy)+']'], ld_no_hours = formdata['ld_no_hours['+str(xy)+']'],
	# 		ld_type = formdata['ld_type['+str(xy)+']'].upper(), ld_sponsored_by = formdata['ld_sponsored_by['+str(xy)+']'].upper()))


	# 	db.session.commit()


	return 'HELLO WORLD', 200



@employees.route('delete-file', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
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
#@admin_permission.require(http_exception=403)
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
#@admin_permission.require(http_exception=403)
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

@employees.route('add-update-cse/<emp_id>', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def add_update_cse(emp_id):
	# if request.method == "POST":
	# 	formdata = request.form.to_dict()
	# 	cs_no_fields = formdata["cs_no_fields"]

	# 	for x in range(1, int(cs_no_fields)+1):
	# 		formdata['cs_eligibility['+str(x)+']']
	# 		formdata['cs_rating['+str(x)+']']
	# 		formdata['date_of_examination['+str(x)+']']
	# 		formdata['place_of_examination_conferment['+str(x)+']']
	# 		formdata['license_no['+str(x)+']']
	# 		formdata['date_of_validity['+str(x)+']']

	# 		new_cs_eligibility = Career_Service(cs_eligibility = formdata['cs_eligibility['+str(x)+']'], cs_rating = formdata['cs_rating['+str(x)+']'],
	# 			date_of_examination = formdata['date_of_examination['+str(x)+']'], place_of_examination_conferment = formdata['place_of_examination_conferment['+str(x)+']'],
	# 			license_no = formdata['license_no['+str(x)+']'], date_of_validity = formdata['date_of_validity['+str(x)+']'], user_id = emp_id)
	# 		db.session.add(new_cs_eligibility)
	# 		db.session.flush()
	# 		db.session.commit()

	return "ok", 200

@employees.route('update-password/<emp_id>', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def update_password(emp_id):
	if request.method == "POST":
		formdata = request.form.to_dict()
		user = User.query.get(emp_id)
		print (user.password)

		if not check_password_hash(user.password, formdata['current_password']):
			return jsonify('Wrong password submitted!'), 403
		elif len(formdata['new_password']) < 5:
			return jsonify('New password should be greater than 5 characters!'), 403
		elif formdata['new_password'] != formdata['confirm_password']:
			return jsonify('Passwords does not match.'), 403
		else:
			user.password = generate_password_hash(formdata['new_password'])
			db.session.commit()
			return jsonify('Successfully changed your password!')
	return "ok", 200

@employees.context_processor
def inject_today_date():
    return {'today_date': datetime.datetime.utcnow()}

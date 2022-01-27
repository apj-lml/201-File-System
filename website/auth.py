from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user, login_required
import datetime
import time
from .models import Career_Service, Learning_Development, User, Uploaded_File, Vaccine, Vocational_Course
from . import db
import os, os.path
import json
from flask_principal import Principal, identity_changed, Identity, AnonymousIdentity

ALLOWED_EXTENSIONS = {'pdf'}

auth = Blueprint('auth', __name__)

@auth.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

@auth.route('/', methods=['GET', 'POST'])
def login():
	logout_user()
	session.clear()
	if request.method == 'POST':
		formdata = json.loads(request.data)
		email = formdata['email']
		password = formdata['password']

		user = User.query.filter_by(employee_id=email).first()
		if user:
			if check_password_hash(user.password, password):
				flash('Login successful', category = 'success')
				login_user(user)
				#session.permanent = False
				if user.type_of_user == 'admin':
					identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
					return redirect(url_for('views.admin_dashboard'))
				elif user.type_of_user == 'super admin':
					return redirect(url_for('views.super_admin_dashboard'))
				else: #user access only
					return redirect(url_for('views.dashboard'))
			else:
				#flash('Incorrect password, try again', category='error')
				#session['error_msg'] = 'Incorrect username or password!'
				return "Incorrect password, try again"
		else:
			#session['error_msg'] = 'Employee ID number does not exist!'
			return "Employee ID number does not exist!"
	return render_template('login.html', user=current_user)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	for key in ('identity.name', 'identity.auth_type'):
		session.pop(key, None)
	identity_changed.send(current_app._get_current_object(), identity = AnonymousIdentity())

	return redirect(url_for('auth.login'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/check-token', methods=['GET', 'POST'])
def check_token():

	return render_template('check_token.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	if 'token-verified' in session:
		if request.method == 'POST':
			#logout_user()
			#formdata = json.loads(request.data) <-- use this if receiving json request
			formdata = request.form.to_dict()
			
			employee_id = formdata['employee_id']
			password1 = formdata['password']
			password2 = formdata['floatingPassword2']

			user = User.query.filter_by(employee_id=employee_id).first()
			if user:
				#flash('User already exists', category = 'error')
				return jsonify('User already exists'), 200
			elif password1 != password2:
				flash('Password does not match', category = 'error')
				return 'Password Error', 200

			else:
				formdata['password'] = generate_password_hash(password1)
				# if formdata['date_of_validity'] != '':
				# 	formdata['date_of_validity'] = datetime.strptime(formdata['date_of_validity'], '%Y-%m-%d').date()
				# else:
				# 	formdata['date_of_validity'] = None
				formdata['birthdate'] = datetime.datetime.strptime(formdata['birthdate'], '%Y-%m-%d').date()

				new_formdata = formdata.copy()
				cs_no_fields = new_formdata['cs_no_fields']
				vocational_no_fields = new_formdata['vocational_no_fields']
				ld_no_fields = new_formdata['ld_no_fields']
				vac_no_fields = new_formdata['vac_no_fields']
	# ---------------------------------------------------------------------------- #
	#              popping unnecessary data before saving to database              #
	# ---------------------------------------------------------------------------- #
				for z in range(1, int(ld_no_fields)+1):
					# print('HERE HEREEEEE!!!!!', x)
					formdata.pop('ld_program['+str(z)+']')
					formdata.pop('ld_date_from['+str(z)+']')
					formdata.pop('ld_date_to['+str(z)+']')
					formdata.pop('ld_no_hours['+str(z)+']')
					formdata.pop('ld_type['+str(z)+']')
					formdata.pop('ld_sponsored_by['+str(z)+']')

				for y in range(1, int(vocational_no_fields)+1):
					# print('HERE HEREEEEE!!!!!', x)
					formdata.pop('v_school['+str(y)+']')
					formdata.pop('vocational_trade_course['+str(y)+']')
					formdata.pop('v_period_of_attendance_from['+str(y)+']')
					formdata.pop('v_period_of_attendance_to['+str(y)+']')
					formdata.pop('v_highest_level['+str(y)+']')
					formdata.pop('v_scholarship_academic_honor['+str(y)+']')
				
				for x in range(1, int(cs_no_fields)+1):
					# print('HERE HEREEEEE!!!!!', x)
					formdata.pop('cs_eligibility['+str(x)+']')
					formdata.pop('cs_rating['+str(x)+']')
					formdata.pop('date_of_examination['+str(x)+']')
					formdata.pop('place_of_examination_conferment['+str(x)+']')
					formdata.pop('license_no['+str(x)+']')
					formdata.pop('date_of_validity['+str(x)+']')

				for x in range(1, int(vac_no_fields)+1):
					# print('HERE HEREEEEE!!!!!', x)
					formdata.pop('vac_type['+str(x)+']')
					formdata.pop('vac_id_no['+str(x)+']')
					formdata.pop('vac_brand['+str(x)+']')
					formdata.pop('vac_place['+str(x)+']')
					formdata.pop('vac_date['+str(x)+']')

				formdata.pop('ld_no_fields')
				formdata.pop('cs_no_fields')
				formdata.pop('vocational_no_fields')
				formdata.pop('floatingPassword2')
				formdata.pop('same_as_permanent')
				formdata.pop('vac_no_fields')
	# ---------------------------------------------------------------------------- #
	#                    saving employee info to the databse                       #
	# ---------------------------------------------------------------------------- #
				#newDict = {k:v.upper() for k,v in formdata.items()}
				# for k, v in formdata.items():
				# 	formdata[k] = formdata.pop(k).upper()
				#print(value)
				finaldata = User(**formdata)
				db.session.add(finaldata)
				db.session.flush()
				db.session.commit()
	# ---------------------------------------------------------------------------- #
	#                              for cs eligibility                              #
	# ---------------------------------------------------------------------------- #

				for x in range(1, int(cs_no_fields)+1):
					# new_formdata['cs_eligibility['+str(x)+']']
					# new_formdata['cs_rating['+str(x)+']']
					# new_formdata['date_of_examination['+str(x)+']']
					# new_formdata['place_of_examination_conferment['+str(x)+']']
					# new_formdata['license_no['+str(x)+']']
					# new_formdata['date_of_validity['+str(x)+']']

					new_cs_eligibility = Career_Service(cs_eligibility = new_formdata['cs_eligibility['+str(x)+']'], cs_rating = new_formdata['cs_rating['+str(x)+']'],
						date_of_examination = new_formdata['date_of_examination['+str(x)+']'], place_of_examination_conferment = new_formdata['place_of_examination_conferment['+str(x)+']'],
						license_no = new_formdata['license_no['+str(x)+']'], date_of_validity = new_formdata['date_of_validity['+str(x)+']'], user_id = finaldata.id)
					db.session.add(new_cs_eligibility)
					db.session.flush()
					db.session.commit()

	# ---------------------------------------------------------------------------- #
	#                            for vocational courses                            #
	# ---------------------------------------------------------------------------- #

				for y in range(1, int(vocational_no_fields)+1):
					# new_formdata['v_school['+str(y)+']']
					# new_formdata['vocational_trade_course['+str(y)+']']
					# new_formdata['v_period_of_attendance_from['+str(y)+']']
					# new_formdata['v_period_of_attendance_to['+str(y)+']']
					# new_formdata['v_highest_level['+str(y)+']']
					# new_formdata['v_scholarship_academic_honor['+str(y)+']']

					new_cs_eligibility = Vocational_Course(v_school = new_formdata['v_school['+str(y)+']'], vocational_trade_course = new_formdata['vocational_trade_course['+str(y)+']'],
						v_period_of_attendance_from = new_formdata['v_period_of_attendance_from['+str(y)+']'], v_period_of_attendance_to = new_formdata['v_period_of_attendance_to['+str(y)+']'],
						v_highest_level = new_formdata['v_highest_level['+str(y)+']'], v_scholarship_academic_honor = new_formdata['v_scholarship_academic_honor['+str(y)+']'], user_id = finaldata.id)
					db.session.add(new_cs_eligibility)
					db.session.flush()
					db.session.commit()

	# ---------------------------------------------------------------------------- #
	#                         for Learning and Development                         #
	# ---------------------------------------------------------------------------- #
				for z in range(1, int(ld_no_fields)+1):
					# new_formdata['ld_program['+str(z)+']']
					# new_formdata['ld_date_from['+str(z)+']']
					# new_formdata['ld_date_to['+str(z)+']']
					# new_formdata['ld_no_hours['+str(z)+']']
					# new_formdata['ld_type['+str(z)+']']
					# new_formdata['ld_sponsored_by['+str(z)+']']

					new_ld = Learning_Development(ld_program = new_formdata['ld_program['+str(z)+']'], ld_date_from = new_formdata['ld_date_from['+str(z)+']'],
						ld_date_to = new_formdata['ld_date_to['+str(z)+']'], ld_no_hours = new_formdata['ld_no_hours['+str(z)+']'],
						ld_type = new_formdata['ld_type['+str(z)+']'], ld_sponsored_by = new_formdata['ld_sponsored_by['+str(z)+']'], user_id = finaldata.id)
					db.session.add(new_ld)
					db.session.flush()
					db.session.commit()

# ---------------------------------------------------------------------------- #
#                                  Vaccination                                 #
# ---------------------------------------------------------------------------- #
				for zx in range(1, int(vac_no_fields)+1):
					new_vac = Vaccine(vac_type = new_formdata['vac_type['+str(zx)+']'], vac_id_no = new_formdata['vac_id_no['+str(zx)+']'],
						vac_brand = new_formdata['vac_brand['+str(zx)+']'], vac_place = new_formdata['vac_place['+str(zx)+']'],
						vac_date = new_formdata['vac_date['+str(zx)+']'], user_id = finaldata.id)
					db.session.add(new_vac)
					db.session.flush()
					db.session.commit()

# ---------------------------------------------------------------------------- #
#                            this is for file upload                           #
# ---------------------------------------------------------------------------- #
				final_name = ''
				for afile in request.files:
					file = request.files[afile]

					print(f'print file: {afile}')
					if afile not in request.files:
						print('No file selected')
						#return redirect(request.url)

					if not file and allowed_file(file.filename):
						print('Invalid file submitted')
						#return redirect(request.url)
					else:
						file_extension = file.filename.rsplit('.', 1)[1].lower()
						file_name = file.filename.rsplit('.', 1)[0]
						final_name = secure_filename(afile+'_'+ formdata['last_name']+'_'+formdata['first_name'] + '_' + str(round(time.time() * 1000)) +'_' + file_name +'.'+file_extension)
						if os.path.isfile(current_app.config['UPLOAD_FOLDER']):
							print('path does not exist... creating path')
							os.mkdir(current_app.config['UPLOAD_FOLDER'])
						else:
							print('path exist!')
							file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], final_name))

							#saving upload info to database
							files_to_upload = Uploaded_File(file_name = final_name, file_path = '\\static\\files\\' + final_name, file_tag = afile, user_id = finaldata.id)
							db.session.add(files_to_upload)
							db.session.commit()
	# ---------------------------------------------------------------------------- #	
	#                              end of file upload                              #
	# ---------------------------------------------------------------------------- #
		else:
			return render_template('signup.html', user=current_user)
		
	return redirect(url_for('auth.login'))
	

@auth.route('/home')
def home():

	return 'HOME'
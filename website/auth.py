from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime, date
from .models import User, Uploaded_File
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
	if request.method == 'POST':
		formdata = json.loads(request.data)
		email = formdata['email']
		password = formdata['password']

		user = User.query.filter_by(email=email).first()
		if user:
			if check_password_hash(user.password, password):
				flash('Login successful', category = 'success')
				login_user(user, remember = True)
				if user.type_of_user == 'admin':
					identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
					return redirect(url_for('views.admin_dashboard'))
				elif user.type_of_user == 'super admin':
					return redirect(url_for('views.super_admin_dashboard'))
				else: #user access only
					return redirect(url_for('views.dashboard'))
			else:
				flash('Incorrect password, try again', category='error')
		else:
			flash('Email does not exist', category='error')
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




@auth.route('/signup', methods=['GET', 'POST'])
def signup():

	if request.method == 'POST':

		#formdata = json.loads(request.data) <-- use this if receiving json request
		formdata = request.form.to_dict()


		email = formdata['email']
		password1 = formdata['password']
		password2 = formdata['floatingPassword2']

		user = User.query.filter_by(email=email).first()
		if user:
			flash('User already exists', category = 'error')
			return 'Duplicate User', 200
		elif password1 != password2:
			flash('Password does not match', category = 'error')
			return 'Password Error', 200

		else:
			formdata['password'] = generate_password_hash(password1)
			if formdata['date_of_validity'] != '':
				formdata['date_of_validity'] = datetime.strptime(formdata['date_of_validity'], '%Y-%m-%d').date()
			else:
				formdata['date_of_validity'] = None
			formdata['birthdate'] = datetime.strptime(formdata['birthdate'], '%Y-%m-%d').date()

#----------------popping unnecessary data before saving to database------------
			formdata.pop('floatingPassword2')
			formdata.pop('same_as_permanent')
#--------------------------------end of popping------------------------------

			# conv = lambda i:i or None
			# converteddata = [conv(i) for i in formdata]
			# print("The list after conversion of Empty Strings : " + str(converteddata))
			
			finaldata = User(**formdata)
			db.session.add(finaldata)
			db.session.flush()
			db.session.commit()

#------------------this is for file upload--------------
			final_name = ''
			for afile in request.files:
				file = request.files[afile]

				print(f'print file: {afile}')
				if afile not in request.files:
					print('No file selected part')
					return redirect(request.url)

				if not file and allowed_file(file.filename):
					print('Invalid file submitted')
					return redirect(request.url)
				else:
					file_extension = file.filename.rsplit('.', 1)[1].lower()
					file_name = file.filename.rsplit('.', 1)[0]
					final_name = secure_filename(afile+'_'+ formdata['last_name']+'_'+formdata['first_name'] + '_' + formdata['employee_id'] +'_' + file_name +'.'+file_extension)
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
#------------------end of file upload--------------------

			return 'ok'
	return render_template('signup.html', user=current_user)






@auth.route('/home')
def home():

	return 'HOME'
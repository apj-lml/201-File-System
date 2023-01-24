from .models import Uploaded_File
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app, session
from . import db
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
import datetime
from .myhelper import allowed_file, my_random_string
from werkzeug.utils import secure_filename
import os, os.path

DownloadableForms = Blueprint('DownloadableForms', __name__)

admin_permission = Permission(RoleNeed('admin'))

@DownloadableForms.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

@DownloadableForms.route('/', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def get_forms():
	if request.method == "GET":

		new_service_record = Uploaded_File.query.filter_by(file_tag = 'dform').all()
		column_keys = Uploaded_File.__table__.columns.keys()
	# Temporary dictionary to keep the return value from table
		rows_dic_temp = {}
		rows_dic = []
	# Iterate through the returned output data set
		for row in new_service_record:
			for col in column_keys:
				rows_dic_temp[col] = getattr(row, col)
			rows_dic.append(rows_dic_temp)
			rows_dic_temp= {}
			#print(rows_dic)
		#return jsonify(rows_dic)

	return render_template('downloadable_forms.html', dforms = rows_dic)



@DownloadableForms.route('/add-form', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def add_forms():
# ---------------------------------------------------------------------------- #
#                              UPLOADING OF FILE                               #
# ---------------------------------------------------------------------------- #

	final_name = ''

	for afilex in request.files:
		filesx = request.files.getlist(afilex)
		print(afilex)
		for filex in filesx:
			if afilex == "wes" :
				if filex.filename == "":
					print('No file selected')
				else:
					if not allowed_file(filex.filename, {'pdf','doc','docx'}):
						print('Invalid file submitted')
						return jsonify('Invalid File Submitted! Only PDF (.pdf) and Word (.doc, .docx) file types are allowed in WES.'), 406
			else:
				if filex.filename == "":
					print('No file selected')
				else:
					if not allowed_file(filex.filename, {'pdf','doc','docx','png', 'jpg', 'jpeg', 'xls', 'xlsx', 'xlsm'}):
						print('Invalid file submitted')
						return jsonify('Invalid File Submitted! Only PDF, Word, Excel files are allowed.'), 406


	for afile in request.files:
		files = request.files.getlist(afile)
		
		# print(f'print file: {file}')
		for file in files:
			print(f'print file: {file.filename}')

			if file.filename == "":
			#if afile not in request.files:
				print('No file selected')
				#return redirect(request.url)
			else:

				today_is = datetime.datetime.today().strftime('%Y-%m-%d-%H%M%S')
				file_extension = file.filename.rsplit('.', 1)[1].lower()
				file_name = file.filename.rsplit('.', 1)[0]
				final_name = secure_filename(file_name + f'_{my_random_string()}' +'.'+file_extension)

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
# ---------------------------------------------------------------------------- #
#                              END OF FILE UPLOAD                              #
# ---------------------------------------------------------------------------- #

	return redirect(url_for("DownloadableForms.get_forms"))


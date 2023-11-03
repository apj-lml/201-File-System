from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Learning_Development, User, Afl
from . import db
import datetime
import time
from .myhelper import allowed_file, my_random_string
from werkzeug.utils import secure_filename
import json
import os, os.path

afl = Blueprint('afl', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@afl.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------------------------------------------------------------------- #
#                                    GET AFL                                   #
# ---------------------------------------------------------------------------- #
@afl.route('get-afl/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_learning_and_development(emp_id):
    if request.method == "GET":
        get_ld = Learning_Development.query.filter_by(user_id = emp_id).all()
        column_keys = Learning_Development.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
    # Iterate through the returned output data set
        for row in get_ld:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
            print(rows_dic)

        return jsonify(rows_dic)

    # if request.method == "POST":
        
    #     return "ok", 200
 # ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                   EDIT AFL                                   #
# ---------------------------------------------------------------------------- #
@afl.route('edit-afl/<id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def edit_ld(id):
    if request.method == "GET":
        get_ld = Learning_Development.query.filter_by(id = id).all()
        column_keys = Learning_Development.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
    # Iterate through the returned output data set
        for row in get_ld:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
            # print(rows_dic)

        return jsonify(rows_dic)

    # if request.method == "POST":
        
    #     return "ok", 200
 # ---------------------------------------------------------------------------- #



 # ---------------------------------------------------------------------------- #
 #                                    ADD AFL                                   #
 # ---------------------------------------------------------------------------- #
@afl.route('add-afl/<emp_id>', methods=['POST', 'GET'])
@login_required
def print_afl(emp_id):
    formdata = request.form.to_dict()
    if request.method == "POST":
        print('DATA ============>', formdata)
        blob_data = request.files['blob_file'].read()
        
    #     formdata['user_id'] = emp_id

    #     for k,v in formdata.items():
    #         if type(v) is str:
    #             formdata.update({k: v.upper()})
    #         else:
    #             formdata.update({k: v})
    return jsonify('Success!')

 # ---------------------------------------------------------------------------- #
 #                                 DELETE AFL                                   #
 # ---------------------------------------------------------------------------- #
@afl.route('delete-afl', methods=['POST', 'GET'])
@login_required
def delete_learning_and_development():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		
		afl = Learning_Development.query.get(formdata['ld_id'])

		os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], afl.ld_attachment_file_name))
		db.session.delete(afl)
		db.session.commit()
	return jsonify('File Deleted Successfully')


@afl.route('save-afl/<id>/<emp_id>', methods=['POST', 'GET'])
@login_required
def update_ld(id, emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        get_we = Learning_Development.query.get(id)
        formdata.pop('id')

        final_name = ''
        
        
        for afile in request.files:
            file = request.files[afile]

            if file.filename == "":
                print('No file selected')
            else:
                if not allowed_file(file.filename):
                    return jsonify('Invalid file submitted. Only PDF files are allowed'), 406

                
                get_user = User.query.get(emp_id)


                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], get_we.ld_attachment_file_name))

                file_extension = file.filename.rsplit('.', 1)[1].lower()
                file_name = file.filename.rsplit('.', 1)[0]
                final_name = secure_filename(formdata['ld_program'] + '_' + get_user.last_name +'_' + file_name + f'_{my_random_string()}' +'.'+file_extension)
                if os.path.isfile(current_app.config['UPLOAD_FOLDER']):
                    print('path does not exist... creating path')
                    os.mkdir(current_app.config['UPLOAD_FOLDER'])
                else:
                    # print('path exist!')
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], final_name))

                    #saving upload info to database
                    # files_to_upload = Uploaded_File(file_name = final_name, file_path = '\\static\\files\\' + final_name, file_tag = afile, user_id = finaldata.id)
                    # db.session.add(files_to_upload)
                    # db.session.commit()
                    formdata['ld_attachment'] = '\\static\\files\\' + final_name
                    formdata['ld_attachment_file_name'] = final_name

        if 'nia_pimo' in formdata:
            formdata['ld_sponsored_by'] = 'NATIONAL IRRIGATION ADMINISTRATION - PANGASINAN IRRIGATION MANAGEMENT OFFICE'
            formdata.pop('nia_pimo')

        for key, value in formdata.items():
            # print(key)
            if key == 'ld_attachment' or key == 'ld_attachment_file_name':
                setattr(get_we, key, value)
            else:
                setattr(get_we, key, value.upper())


        db.session.commit()

        return jsonify('Successfully Saved Changes.')
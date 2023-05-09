from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Records_Of_Leave, User, Records_Of_Leave
from . import db
import datetime
import time
from .myhelper import my_random_string
from werkzeug.utils import secure_filename
import json
import os, os.path
import pandas

rol = Blueprint('rol', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@rol.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------------------------------------------------------------------- #
#                                    GET rol                                   #
# ---------------------------------------------------------------------------- #
@rol.route('get-rol/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_rol(emp_id):
    if request.method == "GET":
        get_ld = Records_Of_Leave.query.filter_by(user_id = emp_id).all()
        column_keys = Records_Of_Leave.__table__.columns.keys()
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
#                                   EDIT rol                                   #
# ---------------------------------------------------------------------------- #
@rol.route('edit-rol/<id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def edit_ld(id):
    if request.method == "GET":
        get_ld = Records_Of_Leave.query.filter_by(id = id).all()
        column_keys = Records_Of_Leave.__table__.columns.keys()
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
 #                                    ADD rol                                   #
 # ---------------------------------------------------------------------------- #
@rol.route('add-rol/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_rol(emp_id):

    file = request.files['rolFile']
    
    if request.method == "POST":
        formdata = request.form.to_dict()
        if file and allowed_file(file.filename):
 
            # Parse the data as a Pandas DataFrame type
            data = pandas.read_excel(file)
            
            for index, row in data.iterrows():
                user_id = row['ID']
                vacation = row['VACATION_LEAVE']
                sick = row['SICK_LEAVE']
                as_of = row['UPDATED_AS_OF']

                # check_rol = Records_Of_Leave.query.get(user_id).first()
                check_rol = db.session.query(Records_Of_Leave).filter(Records_Of_Leave.user_id == user_id).first()

                if check_rol:
                    print('HERE HERE2')
                    check_rol.vacation = vacation,
                    check_rol.sick = sick,
                    check_rol.user_id = user_id,
                    check_rol.as_of = as_of
                    db.session.commit()
                    
                    
                else:
                    print('HERE HERE')
                    new_rol = Records_Of_Leave(
                        vacation = vacation,
                        sick = sick,
                        user_id = user_id,
                        as_of = as_of
                            )
                    db.session.add(new_rol)
                    

            db.session.commit()

            json_data = data.to_json()

            
            return json_data
        return jsonify('Invalid file submitted. Only excel files are allowed'), 406
        


 # ---------------------------------------------------------------------------- #
 #                                 DELETE rol                                   #
 # ---------------------------------------------------------------------------- #
@rol.route('delete-rol', methods=['POST', 'GET'])
@login_required
def delete_learning_and_development():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		
		rol = Records_Of_Leave.query.get(formdata['ld_id'])

		os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], rol.ld_attachment_file_name))
		db.session.delete(rol)
		db.session.commit()
	return jsonify('File Deleted Successfully')


@rol.route('save-rol/<id>/<emp_id>', methods=['POST', 'GET'])
@login_required
def update_ld(id, emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        get_we = Records_Of_Leave.query.get(id)
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
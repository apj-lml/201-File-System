from pprint import pprint
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from sqlalchemy import desc
from .models import Appointment, Uploaded_File, User
from . import db
#from datetime import datetime
from datetime import datetime
from .myhelper import allowed_file, format_mydatetime, my_random_string
from werkzeug.utils import secure_filename
import os, os.path
import json
from werkzeug.security import generate_password_hash, check_password_hash

ALLOWED_EXTENSIONS = {'pdf'}

appointment = Blueprint('appointment', __name__)

admin_permission = Permission(RoleNeed('admin'))

@appointment.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))


@appointment.route('add-appointment/<emp_id>', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def add_appointment(emp_id):
    # user = db.session.query(User).get(emp_id)
    if request.method == "POST":
        formdata = request.form.to_dict()
        final_name = ''

        for k,v in formdata.items():
            # print(k)
            if k != 'appointment_attachment' or k != 'appointment_attachment_file_name':
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})

        for afile in request.files:
            files = request.files.getlist(afile)

            # print(f'print file: {file}')
            for file in files:
                # print(f'print file: {file}')

                if file.filename == "":
                #if afile not in request.files:
                    print('No file selected')
                    #return redirect(request.url)
                else:
                    if not allowed_file(file.filename):
                        # print('Invalid file submitted')
                        return jsonify('invalid_file'), 406
                        #return redirect(request.url)
                    else:
                        today_is = datetime.today().strftime('%Y-%m-%d-%H%M%S')
                        file_extension = file.filename.rsplit('.', 1)[1].lower()
                        file_name = file.filename.rsplit('.', 1)[0]
                        final_name = secure_filename(afile+'_'+ current_user.last_name+'_' + '_' + file_name +'.'+file_extension)
                        
                        # my_file = Path(current_app.config['UPLOAD_FOLDER']+'\\'+final_name)
                        # if my_file.is_file():
                        # 	print('file already exist')

                        if os.path.isfile(current_app.config['UPLOAD_FOLDER']):
                            print('path does not exist... creating path')
                            os.mkdir(current_app.config['UPLOAD_FOLDER'])
                        else:
                            print('path exist!')
                            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], final_name))
                            formdata['appointment_attachment'] = "\\static\\files\\" + final_name
                            formdata['appointment_attachment_file_name'] = final_name

                            if 'sf_present' in formdata:
                                get_we = Appointment.query.filter_by(user_id = emp_id, service_to = "PRESENT").all()
                                if get_we:
                                    return jsonify('overlapping_date'), 406
                                else:
                                    formdata['service_to'] = 'PRESENT'
                                    formdata.pop('sf_present')
                                    # formdata['service_to'] = 'PRESENT'
                                    # formdata.pop('sf_present')
                            else:
                                get_we = Appointment.query.filter_by(user_id = emp_id).order_by(desc(Appointment.service_from)).all()
                                for we in get_we:
                                    pprint(we)
                                    we_date_from = format_mydatetime(we.service_from)
                                    date_from = format_mydatetime(formdata['service_from'])
                                    date_to = format_mydatetime(formdata['service_to'])
                                    if we.service_to == "PRESENT":
                                        we_date_to = datetime.utcnow()
                                    else:
                                        we_date_to = format_mydatetime(we.service_to)

                                    if we_date_from <= date_from <= we_date_to or we_date_from <= date_to <= we_date_to:    
                                        return jsonify('overlapping_date'), 406


                            if 'nia_pimo' in formdata:
                                formdata['station_place'] = 'NATIONAL IRRIGATION ADMINISTRATION - PANGASINAN IRRIGATION MANAGEMENT OFFICE'
                                formdata.pop('nia_pimo')
                            formdata['user_id'] = emp_id


        new_Appointment = Appointment(**formdata)
        db.session.add(new_Appointment)
        db.session.commit()
    return jsonify('Successfully Saved Changes!')



@appointment.route('get-appointment/<emp_id>', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def get_appointment(emp_id):
    if request.method == "GET":

        new_Appointment = Appointment.query.filter_by(user_id = emp_id).all()
        column_keys = Appointment.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
    # Iterate through the returned output data set
        for row in new_Appointment:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
            # print(rows_dic)
        return jsonify(rows_dic)

    # return render_template('appointment.html', emp_id = emp_id)



@appointment.route('edit-appointment', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def edit_appointment():
    if request.method == "POST":
        formdata  = json.loads(request.data)
        print(formdata)
        new_Appointment = Appointment.query.filter_by(id = formdata['id']).all()
        column_keys = Appointment.__table__.columns.keys()
        rows_dic_temp = {}
        rows_dic = []
        for row in new_Appointment:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
            # print(rows_dic)
        return jsonify(rows_dic)

 # ---------------------------------------------------------------------------- #
 #                                 DELETE apt                                   #
 # ---------------------------------------------------------------------------- #
@appointment.route('delete-appointment/<id>', methods=['POST', 'GET'])
@login_required
def delete_appointment(id):
    # if request.method == "POST":
        # formdata  = json.loads(request.data)
    we = Appointment.query.get(id)

    db.session.delete(we)
    db.session.commit()
    return redirect(request.referrer)


 # ---------------------------------------------------------------------------- #
 #                                   Save apt                                   #
 # ---------------------------------------------------------------------------- #
@appointment.route('update-appointment/<id>/<emp_id>', methods=['POST', 'GET'])
@login_required
def update_appointment(id, emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        # get_we = Appointment.query.get(id)
        formdata.pop('id')

        # pprint(formdata)

        final_name = ''
        
        for afile in request.files:
            file = request.files[afile]

            if file.filename == "":
                print('No file selected')
            else:
                if not allowed_file(file.filename):
                    return jsonify('invalid_file'), 406
                
                get_user = User.query.get(emp_id)

                file_extension = file.filename.rsplit('.', 1)[1].lower()
                file_name = file.filename.rsplit('.', 1)[0]
                final_name = secure_filename(get_user.last_name +'_' + file_name + f'_{my_random_string()}' +'.'+file_extension)
                if os.path.isfile(current_app.config['UPLOAD_FOLDER']):
                    print('path does not exist... creating path')
                    os.mkdir(current_app.config['UPLOAD_FOLDER'])
                else:
                    # this is to remove old file
                    #os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], get_we.appointment_attachment_file_name))

                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], final_name))

                    #saving upload info to database
                    formdata['appointment_attachment'] = '\\static\\files\\' + final_name
                    formdata['appointment_attachment_file_name'] = final_name

        if 'sf_present' in formdata:
            formdata['service_to'] = 'PRESENT'
            formdata.pop('sf_present')

        get_we_all = Appointment.query.filter_by(user_id = emp_id).order_by(desc(Appointment.service_from)).all()
        get_we = Appointment.query.get(id)
        # pprint(formdata)
        for we in get_we_all:
            if we.id != int(id):
                if formdata['service_to'] == "PRESENT":
                    we_date_to = datetime.utcnow()
                    date_to = datetime.utcnow()
                else:
                    we_date_to = format_mydatetime(we.service_to)
                    date_to = format_mydatetime(formdata['service_to'])

                we_date_from = format_mydatetime(we.service_from)
                date_from = format_mydatetime(formdata['service_from'])
                
                if we.service_to == "PRESENT":
                    we_date_to = datetime.utcnow()
                    # we_date_to = format_mydatetime(we_date_to)
                else:
                    we_date_to = format_mydatetime(we.service_to)

                # print('WE_DATE_TO', we_date_to)
                # print('DATE_TO', date_to.strftime('%Y-%m-%d'))
                
                if we_date_from <= date_from <= we_date_to or we_date_from <= date_to <= we_date_to:
                    return jsonify('overlapping_date'), 406

        if 'nia_pimo' in formdata:
            formdata['station_place'] = 'NATIONAL IRRIGATION ADMINISTRATION - PANGASINAN IRRIGATION MANAGEMENT OFFICE'
            formdata.pop('nia_pimo')

        for key, value in formdata.items():
            # print(key)
            if key == 'appointment_attachment' or key == 'appointment_attachment_file_name':
                setattr(get_we, key, value)
            else:
                setattr(get_we, key, value.upper())

        db.session.commit()

        return jsonify('Successfully Saved Changes.')
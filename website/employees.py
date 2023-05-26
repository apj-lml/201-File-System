
# from pprint import pprint

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app, send_file, send_from_directory
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from flask_principal import Permission, RoleNeed
import pytz
from .models import Agency_Section, Agency_Unit, Career_Service, College, Doctoral, Masteral, Service_Record, User, Uploaded_File, UserSchema, Vocational_Course, Shirt, Learning_Development, Career_Service, Emergency_Contact
from . import db
#from datetime import datetime
import datetime
from .myhelper import allowed_file, my_random_string
from werkzeug.utils import secure_filename
import os, os.path
import json
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import column, inspect, text

import xlsxwriter
import pandas as pd

from werkzeug.security import generate_password_hash, check_password_hash

from website import myhelper

ALLOWED_EXTENSIONS = {'pdf'}

employees = Blueprint('employees', __name__)

admin_permission = Permission(RoleNeed('admin'))

@employees.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))

@employees.route('generate-report', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def generate_report():
    if request.method == 'POST':
        formdata = request.form.to_dict()
        # Extract the values from formdata as a list
        values = list(formdata.values())
        
        merged_data = {}

        for key, value in formdata.items():
            prefix = key.split('[')[0]  # Extract the prefix before the '[' character
            if prefix not in merged_data:
                merged_data[prefix] = []
            merged_data[prefix].append(value)

        # Save the DataFrame to an Excel file
        static_folder = current_app.root_path + '/static'
        output_file = "Output.xlsx"
        output_path = os.path.join(static_folder, output_file)  # Full path to the output file
        writer = pd.ExcelWriter(output_path, engine="xlsxwriter")

        if merged_data['personal']:
            users = User.query.with_entities(*[getattr(User, column) for column in merged_data['personal']]).all()
            df_user = pd.DataFrame(users)
            df_user.to_excel(writer, sheet_name="User", index=False)

        if 'college' in merged_data:
            colleges = College.query.with_entities(*[getattr(College, column) for column in merged_data['college']]).all()
            df_college = pd.DataFrame(colleges)
            df_college.to_excel(writer, sheet_name="College", index=False)

        if 'masteral' in merged_data:
            masteral = Masteral.query.with_entities(*[getattr(Masteral, column) for column in merged_data['masteral']]).all()
            df_masteral = pd.DataFrame(masteral)
            df_masteral.to_excel(writer, sheet_name="Masteral", index=False)

        if 'doctoral' in merged_data:
            doctoral = Doctoral.query.with_entities(*[getattr(Doctoral, column) for column in merged_data['doctoral']]).all()
            df_doctoral = pd.DataFrame(doctoral)
            df_doctoral.to_excel(writer, sheet_name="Doctoral", index=False)

        if 'vc' in merged_data:
            vc = Vocational_Course.query.with_entities(*[getattr(Vocational_Course, column) for column in merged_data['vc']]).all()
            df_vc = pd.DataFrame(vc)
            df_vc.to_excel(writer, sheet_name="Vocational Course", index=False)

        if 'shirt' in merged_data:
            shirt = Shirt.query.with_entities(*[getattr(Shirt, column) for column in merged_data['shirt']]).all()
            df_shirt = pd.DataFrame(shirt)
            df_shirt.to_excel(writer, sheet_name="Shirt Sizes", index=False)

        if 'ld' in merged_data:
            ld = Shirt.query.with_entities(*[getattr(Learning_Development, column) for column in merged_data['ld']]).all()
            df_ld = pd.DataFrame(ld)
            df_ld.to_excel(writer, sheet_name="Learning & Development", index=False)

        if 'eligibility' in merged_data:
            eligibility = Career_Service.query.with_entities(*[getattr(Career_Service, column) for column in merged_data['eligibility']]).all()
            df_eligibility = pd.DataFrame(eligibility)
            df_eligibility.to_excel(writer, sheet_name="Eligibility", index=False)

        if 'eC' in merged_data:
            eC = Emergency_Contact.query.with_entities(*[getattr(Emergency_Contact, column) for column in merged_data['eC']]).all()
            df_eC = pd.DataFrame(eC)
            df_eC.to_excel(writer, sheet_name="Emergency Contact", index=False)

        writer.close()
        # Send the file for download
        return send_from_directory(static_folder, output_file, as_attachment=True)

    
@employees.route('get-employees/<emp_id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_employees(emp_id):
    if request.method == 'GET' and emp_id == "0" :
        users = User.query.all()

        user_sgjg = {}  # Dictionary to store sgjg attribute for each user

        for user in users:
            if user.employment_status == 'JOB ORDER':
                user_sgjg[user.id] = user.salary_grade
            else:
                user_sgjg[user.id] = user.job_grade

        user_schema = UserSchema(many=True)

        # Update output with sgjg attribute
        output = user_schema.dump(users)
        for user_data in output:
            user_data['sgjg'] = user_sgjg.get(user_data['id'])

        db.session.close()
        return jsonify(output)

        

@employees.route('my-profile/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def my_profile(emp_id):
    
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "PAGE NOT FOUND", 404
        else:
            user = db.session.query(User).get(emp_id)
            my_agency_section = db.session.query(Agency_Section).all()
            my_agency_unit = db.session.query(Agency_Unit).all()

            user_profile = user
            agency_section = my_agency_section
            agency_unit = my_agency_unit

            db.session.commit()
            
            tz = pytz.timezone('Asia/Manila')  # timezone you want to convert to, from UTC is (Asia/Manila)
            utc = pytz.timezone('UTC')
            value = utc.localize(user.last_updated, is_dst=None).astimezone(pytz.utc)
            local_dt = value.astimezone(tz)

            last_updated = local_dt


        return render_template('employee_profile.html', user_profile=user_profile, agency_section=agency_section, agency_unit=agency_unit, last_updated=last_updated)
        
    return jsonify({})


@employees.route('get-singular-employee/<emp_id>', methods=['POST', 'GET'])
@login_required
def get_singular_employee(emp_id):
    user = db.session.query(User).get(emp_id)
    # user = User.query.filter_by(id = emp_id).all()
    user_schema = UserSchema()
    # user_schema = UserSchema(many=True)
    output = user_schema.dump(user)

    db.session.close()
    return jsonify(output)


@employees.route('update-employee/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def update_employee(emp_id):
    formdata = request.form.to_dict()

    user = db.session.query(User).get(emp_id)

    formdata['birthdate'] = datetime.datetime.strptime(formdata['birthdate'], '%Y-%m-%d').date()

    if formdata['first_day_in_service'] == '':
        formdata['first_day_in_service'] = None

# ---------------------------------------------------------------------------- #
#                              UPLOADING OF FILE                               #
# ---------------------------------------------------------------------------- #
    final_name = ''

    for afilex in request.files:
        filesx = request.files.getlist(afilex)
        
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
                    if not allowed_file(filex.filename):
                        print('Invalid file submitted')
                        return jsonify('Invalid File Submitted! Only PDF (.pdf) Files are allowed.'), 406


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
                final_name = secure_filename(afile+'_'+ formdata['last_name']+'_' + '_' + file_name + f'_{my_random_string()}' +'.'+file_extension)
                
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
# --------------------------- END OF FILE UPLOADING -------------------------- #


# ---------------------------------------------------------------------------- #
#                                ADDING OF DATA                                #
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
        # if v == "":
        # 	print(k,v)
        # 	# formdata.update({k: None})
        # else:
        if type(v) is str and k != 'comments_remarks':
            formdata.update({k: v.upper()})
        else:
            formdata.update({k: v})
        # print(k, v)
# ---------------------------------------------------------------------------- #
#                         UPDATING OF EMPLOYEE PROFILE                         #
# ---------------------------------------------------------------------------- #

    #if current_user.type_of_user != 'admin':
    formdata['acknowledgement'] = 'checked'
    
    #code for automated update
    for key, value in formdata.items(): 
        setattr(user, key, value)
    db.session.commit()

# ---------------------------------------------------------------------------- #
#                         UPDATING OF VOCATIONAL COURSE                        #
# ---------------------------------------------------------------------------- #
    for xy in range(1, int(vocational_no_update_fields)+1):

        v_school = formdata['v_school['+str(xy)+']']
        vocational_trade_course = formdata['vocational_trade_course['+str(xy)+']']
        v_period_of_attendance_from = formdata['v_period_of_attendance_from['+str(xy)+']']
        v_period_of_attendance_to = formdata['v_period_of_attendance_to['+str(xy)+']']
        v_highest_level = formdata['v_highest_level['+str(xy)+']']
        v_highest_grade_year_units = formdata['v_highest_grade_year_units['+str(xy)+']']
        v_scholarship_academic_honor = formdata['v_scholarship_academic_honor['+str(xy)+']']
        v_date_of_validity = formdata['v_date_of_validity['+str(xy)+']']

        vocational_course = Vocational_Course.query.filter_by(id = formdata['v_id['+str(xy)+']'])
        vocational_course.update(dict(
                                v_school = v_school,
                                vocational_trade_course = vocational_trade_course,
                                v_period_of_attendance_from = v_period_of_attendance_from,
                                v_period_of_attendance_to = v_period_of_attendance_to,
                                v_highest_level = v_highest_level,
                                v_highest_grade_year_units = v_highest_grade_year_units,
                                v_scholarship_academic_honor = v_scholarship_academic_honor,
                                v_date_of_validity = v_date_of_validity
                                ))
                                
        db.session.commit()
# ---------------------------------------------------------------------------- #
#                                UPDATING OF CSE                               #
# ---------------------------------------------------------------------------- #

    for xy in range(1, int(cs_update_no_fields)+1):

        if formdata['cs_rating['+str(xy)+']'] == "":
            formdata['cs_rating['+str(xy)+']'] = "N/A"
        
        cse = Career_Service.query.filter_by(id = formdata['cse_id['+str(xy)+']'])
        cse.update(dict(cs_eligibility = formdata['cs_eligibility['+str(xy)+']'].upper(), 
                        cs_rating = formdata['cs_rating['+str(xy)+']'].upper(), 
                        date_of_examination = formdata['date_of_examination['+str(xy)+']'], 
                        date_of_examination_to = formdata['date_of_examination_to['+str(xy)+']'], 
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
    return jsonify('Successfully Saved to Database!'), 200


@employees.route('add-employee', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def insert_employee():
    formdata = request.form.to_dict()

    # user = db.session.query(User).get(emp_id)

    formdata['birthdate'] = datetime.datetime.strptime(formdata['birthdate'], '%Y-%m-%d').date()

    formdata = formdata.copy()

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
# ---------------------------------------------------------------------------- #
#                        INSERTING OF EMPLOYEE PROFILE                         #
# ---------------------------------------------------------------------------- #
    
    #code for automated insert
    new_user = User(**formdata)
    db.session.add(new_user)
    db.session.flush()
    db.session.commit()

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
                    if not allowed_file(filex.filename):
                        print('Invalid file submitted')
                        return jsonify('Invalid File Submitted! Only PDF (.pdf) Files are allowed.'), 406


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
                final_name = secure_filename(afile+'_'+ formdata['last_name']+'_' + '_' + file_name + f'_{my_random_string()}' +'.'+file_extension)

                if os.path.isfile(current_app.config['UPLOAD_FOLDER']):
                    print('path does not exist... creating path')
                    os.mkdir(current_app.config['UPLOAD_FOLDER'])
                else:
                    print('path exist!')
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], final_name))

                    #saving upload info to database
                    files_to_upload = Uploaded_File(file_name = final_name, file_path = "\\static\\files\\", file_tag = afile, user_id = new_user.id)
                    db.session.add(files_to_upload)
                    db.session.commit()
# ---------------------------------------------------------------------------- #
#                              END OF FILE UPLOAD                              #
# ---------------------------------------------------------------------------- #

    return jsonify(user_id=new_user.id), 200

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


@employees.route('reset-password/<emp_id>', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def reset_password(emp_id):
    if request.method == "GET":
        # formdata = request.form.to_dict()
        user = User.query.get(emp_id)

        user.password = generate_password_hash('pimopassword')
        db.session.commit()
    return jsonify(message = 'Reset password success!')

@employees.route('validate/<emp_id>', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def validate_emp(emp_id):
    if request.method == "GET":
        #formdata = request.form.to_dict()
        user = User.query.get(emp_id)
        # print ("HERE", user.is_validated)
        # if user.is_validated != 'VALIDATED':
        user.is_validated = 'VALIDATED'
        # else:
        # 	user.is_validated = 'NOT VALIDATED'
        db.session.commit()
            #return jsonify('Successfully changed your password!')
    return redirect(url_for("views.admin_dashboard"))

@employees.route('not-validated/<emp_id>', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def not_validated_emp(emp_id):
    if request.method == "GET":
        #formdata = request.form.to_dict()
        user = User.query.get(emp_id)

        user.is_validated = 'NOT VALIDATED'

        db.session.commit()
            #return jsonify('Successfully changed your password!')
    return redirect(url_for("views.admin_dashboard"))

@employees.context_processor
def inject_today_date():
    return {'today_date': datetime.datetime.utcnow()}

@employees.context_processor
def utility_processor():
    def inject_count_files(file_tag, emp_id):
        count_files = Uploaded_File.query.filter_by(user_id = emp_id, file_tag = file_tag)
        counted_files = count_files.count()
        # if(count_files != 0):
        # 	output = f"You have uploaded "
        #return f"You have uploaded {counted_files} file(s) in this field."
        return counted_files
    return dict(count_files = inject_count_files)

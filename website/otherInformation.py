from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Other_Information
from . import db
from datetime import datetime
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import json

otherInformation = Blueprint('otherInformation', __name__)


admin_permission = Permission(RoleNeed('admin'))

@otherInformation.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))

# @workExperience.template_filter()
# def format_datetime(value, format='medium'):
#     if format == 'full':
#         format="EEEE, d. MMMM y 'at' HH:mm"
#     elif format == 'medium':
#         format="EE dd.MM.y HH:mm"
#     return babel.dates.format_datetime(value, format)



# ---------------------------------------------------------------------------- #
#                           ADD VW IN EMPLOYEE PROFILE                        #
# ---------------------------------------------------------------------------- #
@otherInformation.route('add-other-information/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_other_information(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        formdata['user_id'] = emp_id
        formdata = {k:v.upper() for k,v in formdata.items()}
        count_other_information = Other_Information.query.filter_by(type = formdata['type'], user_id = emp_id).count()
        # print ('---------------------', formdata['type'])
        if count_other_information < 5:
            
            # for key, value in formdata.items(): 
            #     setattr(formdata, key, value.upper())
    
            new_work_exp = Other_Information(**formdata)

            db.session.add(new_work_exp)
            db.session.flush()
            db.session.commit()
        else:
            return jsonify("You can only add up to five (5) inputs only!"), 200
            
    return jsonify("Successfully Added Other Information!"), 200


 # ---------------------------------------------------------------------------- #
 #                                 DELETE VW                                   #
 # ---------------------------------------------------------------------------- #
@otherInformation.route('delete-other-information', methods=['POST', 'GET'])
@login_required
def delete_other_information():
    if request.method == "POST":
        formdata  = json.loads(request.data)
        we = Other_Information.query.get(formdata['work_exp_id'])

        db.session.delete(we)
        db.session.commit()
    return jsonify('Work Experience Deleted Successfully')

 # ---------------------------------------------------------------------------- #
 #                                    GET VW                                   #
 # ---------------------------------------------------------------------------- #
@otherInformation.route('edit-other-information', methods=['POST', 'GET'])
@login_required
def edit_other_information():
    if request.method == "POST":
        formdata  = json.loads(request.data)
        get_we = Other_Information.query.filter_by(id = formdata['id']).all()
        column_keys = Other_Information.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
    # Iterate through the returned output data set
        for row in get_we:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
            print(rows_dic)
        return jsonify(rows_dic)

 # ---------------------------------------------------------------------------- #
 #                                   Save VW                                   #
 # ---------------------------------------------------------------------------- #
@otherInformation.route('save-other-information', methods=['POST', 'GET'])
@login_required
def update_other_information():
    if request.method == "POST":
        formdata = request.form.to_dict()
        get_we = Other_Information.query.get(formdata['id'])
        formdata.pop('id')

        #code for automated update
        print(formdata)
        for key, value in formdata.items(): 
            setattr(get_we, key, value.upper())
        db.session.commit()

        return jsonify('Successfully Saved Changes.')

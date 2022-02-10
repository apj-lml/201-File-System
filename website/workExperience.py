from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Work_Experience
from . import db
from datetime import datetime
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import json

workExperience = Blueprint('workExperience', __name__)


admin_permission = Permission(RoleNeed('admin'))

@workExperience.errorhandler(403)
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
#                           ADD WES IN EMPLOYEE PROFILE                        #
# ---------------------------------------------------------------------------- #
@workExperience.route('add-work-experience/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_work_experience(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        formdata['user_id'] = emp_id
        new_work_exp = Work_Experience(**formdata)

        db.session.add(new_work_exp)
        db.session.flush()
        db.session.commit()
            
    return jsonify("Successfully Added Work Experience!"), 200


 # ---------------------------------------------------------------------------- #
 #                                 DELETE WES                                   #
 # ---------------------------------------------------------------------------- #
@workExperience.route('delete-work-experience', methods=['POST', 'GET'])
@login_required
def delete_work_experience():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		we = Work_Experience.query.get(formdata['work_exp_id'])

		db.session.delete(we)
		db.session.commit()
	return jsonify('Work Experience Deleted Successfully')

 # ---------------------------------------------------------------------------- #
 #                                    GET WES                                   #
 # ---------------------------------------------------------------------------- #
@workExperience.route('view-work-experience', methods=['POST', 'GET'])
@login_required
def view_work_experience():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		get_we = Work_Experience.query.filter_by(id = formdata['work_exp_id']).all()
		column_keys = Work_Experience.__table__.columns.keys()
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
 #                                   Save WES                                   #
 # ---------------------------------------------------------------------------- #
@workExperience.route('save-work-experience', methods=['POST', 'GET'])
@login_required
def update_work_experience():
    if request.method == "POST":
        formdata = request.form.to_dict()
        get_we = Work_Experience.query.get(formdata['id'])
        formdata.pop('id')

        #code for automated update
        print(formdata)
        for key, value in formdata.items(): 
            setattr(get_we, key, value)
        db.session.commit()

        return jsonify('Successfully Saved Changes.')

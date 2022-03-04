from itertools import count
from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Emergency_Contact
from . import db
from datetime import datetime
import json

emergencyContact = Blueprint('emergencyContact', __name__)


admin_permission = Permission(RoleNeed('admin'))

@emergencyContact.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

# @emergencyContact.template_filter()
# def format_datetime(value, format='medium'):
#     if format == 'full':
#         format="EEEE, d. MMMM y 'at' HH:mm"
#     elif format == 'medium':
#         format="EE dd.MM.y HH:mm"
#     return babel.dates.format_datetime(value, format)



# ---------------------------------------------------------------------------- #
#                                    ADD CHAR REF                              #
# ---------------------------------------------------------------------------- #
@emergencyContact.route('add/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_emergency_contact(emp_id):
    if request.method == "POST":

        formdata = request.form.to_dict()
        for k,v in formdata.items():
            formdata.update({k: v.upper()})

        count_char_ref = Emergency_Contact.query.filter_by(user_id = emp_id).count()
        
        if count_char_ref < 1 :
            formdata['user_id'] = emp_id
            char_ref = Emergency_Contact(**formdata)

            db.session.add(char_ref)
            db.session.flush()
            db.session.commit()
            
            return jsonify("Successfully Added Emergency Contact!"), 200
        else:
            return jsonify("You can only add up to one Emergency Contact only!")


 # ---------------------------------------------------------------------------- #
 #                                 DELETE WES                                   #
 # ---------------------------------------------------------------------------- #
@emergencyContact.route('delete', methods=['POST', 'GET'])
@login_required
def delete_emergency_contact():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		cr = Emergency_Contact.query.get(formdata['id'])

		db.session.delete(cr)
		db.session.commit()
	return jsonify('Emergency Contact Deleted Successfully')

 # ---------------------------------------------------------------------------- #
 #                                    GET WES                                   #
 # ---------------------------------------------------------------------------- #
@emergencyContact.route('get/<emp_id>', methods=['POST', 'GET'])
@login_required
def view_emergency_contact(emp_id):
	if request.method == "GET":
	# formdata  = json.loads(request.data)
		get_cr = Emergency_Contact.query.filter_by(user_id = emp_id).all()
		column_keys = Emergency_Contact.__table__.columns.keys()
	# Temporary dictionary to keep the return value from table
		rows_dic_temp = {}
		rows_dic = []
	# Iterate through the returned output data set
		for row in get_cr:
			for col in column_keys:
				rows_dic_temp[col] = getattr(row, col)
			rows_dic.append(rows_dic_temp)
			rows_dic_temp= {}
			print(rows_dic)
		return jsonify(rows_dic)

 # ---------------------------------------------------------------------------- #
 #                                   Save WES                                   #
 # ---------------------------------------------------------------------------- #
@emergencyContact.route('save-work-experience', methods=['POST', 'GET'])
@login_required
def update_work_experience():
    if request.method == "POST":
        formdata = request.form.to_dict()
        get_we = Emergency_Contact.query.get(formdata['id'])
        formdata.pop('id')

        #code for automated update
        print(formdata)
        for key, value in formdata.items(): 
            setattr(get_we, key, value)
        db.session.commit()

        return jsonify('Successfully Saved Changes.')

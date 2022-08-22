from pprint import pprint
from flask import Blueprint, request, redirect, url_for, session, jsonify
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import College
from . import db
import os, os.path
import json

college = Blueprint('college', __name__)


admin_permission = Permission(RoleNeed('admin'))

@college.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

# ---------------------------------------------------------------------------- #
#                          Add COLLEGE from update profile                     #
# ---------------------------------------------------------------------------- #
@college.route('add-college/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_college(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        college_no_fields = formdata["college_no_fields"]
        
        print("this is the ID: " + emp_id)
        pprint(formdata)
# ---------------------------------------------------------------------------- #
#                                CAPITALIZE DATA                               #
# ---------------------------------------------------------------------------- #.

        for k,v in formdata.items():
            if type(v) is str:
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})

# ---------------------------------------------------------------------------- #
        for x in range(1, int(college_no_fields)+1):
            print('IM HERE')
            c_school = formdata['c_school['+str(x)+']']
            c_degree_course = formdata['c_degree_course['+str(x)+']']
            c_period_of_attendance_from = formdata['c_period_of_attendance_from['+str(x)+']']
            c_period_of_attendance_to = formdata['c_period_of_attendance_to['+str(x)+']']
            c_highest_level_units_earned = formdata['c_highest_level_units_earned['+str(x)+']']
            c_highest_grade_year_units = formdata['c_highest_grade_year_units['+str(x)+']']
            c_scholarship_academic_honor = formdata['c_scholarship_academic_honor['+str(x)+']']
            
            if(c_school != "" and c_degree_course != "" and c_period_of_attendance_from != "" and c_period_of_attendance_to != "" and c_highest_level_units_earned != "" and c_scholarship_academic_honor != ""):
                new_college = College(
                    c_school = formdata['c_school['+str(x)+']'],
                    c_degree_course = formdata['c_degree_course['+str(x)+']'],
                    c_period_of_attendance_from = formdata['c_period_of_attendance_from['+str(x)+']'],
                    c_period_of_attendance_to = formdata['c_period_of_attendance_to['+str(x)+']'],
                    c_highest_level_units_earned = formdata['c_highest_level_units_earned['+str(x)+']'],
                    c_highest_grade_year_units = formdata['c_highest_grade_year_units['+str(x)+']'],
                    c_scholarship_academic_honor = formdata['c_scholarship_academic_honor['+str(x)+']'],
                    user_id = emp_id)
                db.session.add(new_college)
                db.session.commit()
            
    return "ok", 200

 # ---------------------------------------------------------------------------- #
 #                             DELETE COLLEGE                                   #
 # ---------------------------------------------------------------------------- #
@college.route('delete-college', methods=['POST', 'GET'])
@login_required
def delete_college():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		
		data = College.query.get(formdata['id'])

		db.session.delete(data)
		db.session.commit()
	return jsonify('File Deleted Successfully')
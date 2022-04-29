from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Doctoral
from . import db
from datetime import datetime
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import os, os.path
import json

doctoral = Blueprint('doctoral', __name__)


admin_permission = Permission(RoleNeed('admin'))

@doctoral.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

# ---------------------------------------------------------------------------- #
#                         Add DOCTORAL from update profile                     #
# ---------------------------------------------------------------------------- #
@doctoral.route('add-doctoral/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_doctoral(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        doctoral_no_fields = formdata["doctoral_no_fields"]

# ---------------------------------------------------------------------------- #
#                                CAPITALIZE DATA                               #
# ---------------------------------------------------------------------------- #
        for k,v in formdata.items():
            if type(v) is str:
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})
# ---------------------------------------------------------------------------- #
        
        for x in range(1, int(doctoral_no_fields)+1):

            doc_school = formdata['doc_school['+str(x)+']']
            doc_degree_course = formdata['doc_degree_course['+str(x)+']']
            doc_period_of_attendance_from = formdata['doc_period_of_attendance_from['+str(x)+']']
            doc_period_of_attendance_to = formdata['doc_period_of_attendance_to['+str(x)+']']
            doc_highest_level_units_earned = formdata['doc_highest_level_units_earned['+str(x)+']']
            doc_highest_grade_year_units = formdata['doc_highest_grade_year_units['+str(x)+']']
            doc_scholarship_academic_honor = formdata['doc_scholarship_academic_honor['+str(x)+']']
            if(doc_school == "" and
                doc_degree_course == "" and
                doc_period_of_attendance_from == "" and
                doc_period_of_attendance_to == "" and
                doc_highest_level_units_earned == "" and
                doc_highest_grade_year_units == "" and
                doc_scholarship_academic_honor == ""
                ): pass
            else:
                new_doctoral = Doctoral(
                    doc_school = formdata['doc_school['+str(x)+']'],
                    doc_degree_course = formdata['doc_degree_course['+str(x)+']'],
                    doc_period_of_attendance_from = formdata['doc_period_of_attendance_from['+str(x)+']'],
                    doc_period_of_attendance_to = formdata['doc_period_of_attendance_to['+str(x)+']'],
                    doc_highest_level_units_earned = formdata['doc_highest_level_units_earned['+str(x)+']'],
                    doc_highest_grade_year_units = formdata['doc_highest_grade_year_units['+str(x)+']'],
                    doc_scholarship_academic_honor = formdata['doc_scholarship_academic_honor['+str(x)+']'],
                    user_id = emp_id)
                db.session.add(new_doctoral)
                db.session.flush()
                db.session.commit()
            
    return "ok", 200

 # ---------------------------------------------------------------------------- #
 #                             DELETE COLLEGE                                   #
 # ---------------------------------------------------------------------------- #
@doctoral.route('delete-doctoral', methods=['POST', 'GET'])
@login_required
def delete_doctoral():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		
		data = Doctoral.query.get(formdata['id'])

		db.session.delete(data)
		db.session.commit()
	return jsonify('File Deleted Successfully')
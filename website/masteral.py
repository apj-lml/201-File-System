from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Masteral
from . import db
from datetime import datetime
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import os, os.path
import json

masteral = Blueprint('masteral', __name__)


admin_permission = Permission(RoleNeed('admin'))

@masteral.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

# ---------------------------------------------------------------------------- #
#                         Add MASTERAL from update profile                     #
# ---------------------------------------------------------------------------- #
@masteral.route('add-masteral/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_masteral(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        masteral_no_fields = formdata["masteral_no_fields"]

# ---------------------------------------------------------------------------- #
#                                CAPITALIZE DATA                               #
# ---------------------------------------------------------------------------- #
        for k,v in formdata.items():
            if type(v) is str:
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})
# ---------------------------------------------------------------------------- #

        for x in range(1, int(masteral_no_fields)+1):

            gs_school = formdata['gs_school['+str(x)+']']
            gs_degree_course = formdata['gs_degree_course['+str(x)+']']
            gs_period_of_attendance_from = formdata['gs_period_of_attendance_from['+str(x)+']']
            gs_period_of_attendance_to = formdata['gs_period_of_attendance_to['+str(x)+']']
            gs_highest_level_units_earned = formdata['gs_highest_level_units_earned['+str(x)+']']
            gs_highest_grade_year_units = formdata['gs_highest_grade_year_units['+str(x)+']']
            gs_scholarship_academic_honor = formdata['gs_scholarship_academic_honor['+str(x)+']']

            if(
                gs_school == "" and
                gs_degree_course == "" and
                gs_period_of_attendance_from == "" and
                gs_period_of_attendance_to == "" and
                gs_highest_level_units_earned == "" and
                gs_highest_grade_year_units == "" and
                gs_scholarship_academic_honor == ""
            ): pass
            else:
                new_masteral = Masteral(
                    gs_school = formdata['gs_school['+str(x)+']'],
                    gs_degree_course = formdata['gs_degree_course['+str(x)+']'],
                    gs_period_of_attendance_from = formdata['gs_period_of_attendance_from['+str(x)+']'],
                    gs_period_of_attendance_to = formdata['gs_period_of_attendance_to['+str(x)+']'],
                    gs_highest_level_units_earned = formdata['gs_highest_level_units_earned['+str(x)+']'],
                    gs_highest_grade_year_units = formdata['gs_highest_grade_year_units['+str(x)+']'],
                    gs_scholarship_academic_honor = formdata['gs_scholarship_academic_honor['+str(x)+']'],
                    user_id = emp_id)
                db.session.add(new_masteral)
                db.session.flush()
                db.session.commit()
            
    return "ok", 200

 # ---------------------------------------------------------------------------- #
 #                             DELETE MASTERS                                   #
 # ---------------------------------------------------------------------------- #
@masteral.route('delete-masteral', methods=['POST', 'GET'])
@login_required
def delete_masteral():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		
		data = Masteral.query.get(formdata['id'])

		db.session.delete(data)
		db.session.commit()
	return jsonify('File Deleted Successfully')
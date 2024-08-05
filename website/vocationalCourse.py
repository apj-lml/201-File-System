
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Vocational_Course
from . import db
from datetime import datetime
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import json

vocation = Blueprint('vocation', __name__)


admin_permission = Permission(RoleNeed('admin'))

@vocation.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

# ---------------------------------------------------------------------------- #
#                   ADD VOCATIONAL COURSE IN EMPLOYEE PROFILE                  #
# ---------------------------------------------------------------------------- #
@vocation.route('add-vocational/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_vocational(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        vocational_no_fields = formdata["vocational_no_fields"]

        for x in range(1, int(vocational_no_fields)+1):

            v_school = formdata['v_school['+str(x)+']']
            vocational_trade_course = formdata['vocational_trade_course['+str(x)+']']
            v_period_of_attendance_from = formdata['v_period_of_attendance_from['+str(x)+']']
            v_period_of_attendance_to = formdata['v_period_of_attendance_to['+str(x)+']']
            v_highest_level = formdata['v_highest_level['+str(x)+']']
            v_highest_grade_year_units = formdata['v_highest_grade_year_units['+str(x)+']']
            v_scholarship_academic_honor = formdata['v_scholarship_academic_honor['+str(x)+']']
            v_date_of_validity = formdata['v_date_of_validity['+str(x)+']']
            
            if (v_school == "" and vocational_trade_course == "" and v_period_of_attendance_from == "" and v_period_of_attendance_to == "" and v_highest_level == "" and v_highest_grade_year_units == "" and v_scholarship_academic_honor == "" and v_date_of_validity == ""):
                pass
            else:
                new_vocational = Vocational_Course(
                    v_school = formdata['v_school['+str(x)+']'].upper(),
                    vocational_trade_course = formdata['vocational_trade_course['+str(x)+']'].upper(),
                    v_period_of_attendance_from = formdata['v_period_of_attendance_from['+str(x)+']'],
                    v_period_of_attendance_to = formdata['v_period_of_attendance_to['+str(x)+']'],
                    v_highest_level = formdata['v_highest_level['+str(x)+']'].upper(),
                    v_highest_grade_year_units = formdata['v_highest_grade_year_units['+str(x)+']'].upper(),
                    v_scholarship_academic_honor = formdata['v_scholarship_academic_honor['+str(x)+']'],
                    v_date_of_validity = formdata['v_date_of_validity['+str(x)+']'],
                    user_id = emp_id)
                db.session.add(new_vocational)
                db.session.flush()
                db.session.commit()
            
    return "vocation ok", 200


 # ---------------------------------------------------------------------------- #
 #                          DELETE VOCATIONAL                                   #
 # ---------------------------------------------------------------------------- #
@vocation.route('delete-vocational', methods=['POST', 'GET'])
@login_required
def delete_learning_and_development():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		
		voc = Vocational_Course.query.get(formdata['id'])

		db.session.delete(voc)
		db.session.commit()
	return jsonify('File Deleted Successfully')
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
            formdata['v_school['+str(x)+']']
            formdata['vocational_trade_course['+str(x)+']']
            formdata['v_period_of_attendance_from['+str(x)+']']
            formdata['v_period_of_attendance_to['+str(x)+']']
            formdata['v_highest_level['+str(x)+']']
            formdata['v_scholarship_academic_honor['+str(x)+']']
            
            new_vocational = Vocational_Course(v_school = formdata['v_school['+str(x)+']'], vocational_trade_course = formdata['vocational_trade_course['+str(x)+']'],
				v_period_of_attendance_from = formdata['v_period_of_attendance_from['+str(x)+']'], v_period_of_attendance_to = formdata['v_period_of_attendance_to['+str(x)+']'],
				v_highest_level = formdata['v_highest_level['+str(x)+']'], v_scholarship_academic_honor = formdata['v_scholarship_academic_honor['+str(x)+']'], user_id = emp_id)
            db.session.add(new_vocational)
            db.session.flush()
            db.session.commit()
            
    return "vocation ok", 200
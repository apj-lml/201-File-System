from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Career_Service, Service_Record, User, Uploaded_File
from . import db
from datetime import datetime
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import os, os.path
import json

cse = Blueprint('cse', __name__)


admin_permission = Permission(RoleNeed('admin'))

@cse.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

# ---------------------------------------------------------------------------- #
#                      Add eligibility from update profile                     #
# ---------------------------------------------------------------------------- #
@cse.route('add-eligibility/<emp_id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def add_eligibility(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        cs_no_fields = formdata["cs_no_fields"]

        for x in range(1, int(cs_no_fields)+1):
            formdata['cs_eligibility['+str(x)+']']
            formdata['cs_rating['+str(x)+']']
            formdata['date_of_examination['+str(x)+']']
            formdata['place_of_examination_conferment['+str(x)+']']
            formdata['date_of_validity['+str(x)+']']

            new_cs_eligibility = Career_Service(cs_eligibility = formdata['cs_eligibility['+str(x)+']'], cs_rating = formdata['cs_rating['+str(x)+']'],
				date_of_examination = formdata['date_of_examination['+str(x)+']'], place_of_examination_conferment = formdata['place_of_examination_conferment['+str(x)+']'],
				license_no = formdata['license_no['+str(x)+']'], date_of_validity = formdata['date_of_validity['+str(x)+']'], user_id = emp_id)
            db.session.add(new_cs_eligibility)
            db.session.flush()
            db.session.commit()
            
    return "ok", 200
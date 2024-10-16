
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
# @cse.route('add-eligibility', methods=['POST', 'GET'])
@cse.route('add-eligibility/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_eligibility(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        cs_no_fields = formdata["cs_no_fields"]

        for x in range(1, int(cs_no_fields)+1):

            cs_eligibility = formdata['cs_eligibility['+str(x)+']']
            cs_rating = formdata['cs_rating['+str(x)+']']
            date_of_examination = formdata['date_of_examination['+str(x)+']']
            date_of_examination_to = formdata['date_of_examination_to['+str(x)+']']
            place_of_examination_conferment = formdata['place_of_examination_conferment['+str(x)+']']
            license_no = formdata['license_no['+str(x)+']']
            date_of_validity = formdata['date_of_validity['+str(x)+']']

            if(
                cs_eligibility == "" and
                cs_rating == "" and
                date_of_examination == "" and
                date_of_examination_to == "" and
                place_of_examination_conferment == "" and
                license_no == "" and
                date_of_validity == ""
            ):pass
            
            else:
                if cs_rating == "":
                    cs_rating="N/A"

                new_cs_eligibility = Career_Service(
                    cs_eligibility = formdata['cs_eligibility['+str(x)+']'],
                    cs_rating = formdata['cs_rating['+str(x)+']'],
                    date_of_examination = formdata['date_of_examination['+str(x)+']'],
                    date_of_examination_to = formdata['date_of_examination_to['+str(x)+']'],
                    place_of_examination_conferment = formdata['place_of_examination_conferment['+str(x)+']'],
                    license_no = formdata['license_no['+str(x)+']'],
                    date_of_validity = formdata['date_of_validity['+str(x)+']'],
                    user_id = emp_id)

                db.session.add(new_cs_eligibility)
                db.session.flush()
                db.session.commit()
            
    return "im ok", 200

@cse.route('delete-cse', methods=['POST', 'GET'])
@login_required
def delete_cse():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		
		data = Career_Service.query.get(formdata['id'])

		db.session.delete(data)
		db.session.commit()
	return jsonify('Civil Service Eligibility Deleted Successfully')
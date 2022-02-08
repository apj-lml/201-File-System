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
 #                          DELETE VOCATIONAL                                   #
 # ---------------------------------------------------------------------------- #
@workExperience.route('delete-vocational', methods=['POST', 'GET'])
@login_required
def delete_learning_and_development():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		voc = Work_Experience.query.get(formdata['id'])

		db.session.delete(voc)
		db.session.commit()
	return jsonify('File Deleted Successfully')
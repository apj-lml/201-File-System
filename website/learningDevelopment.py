from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Learning_Development
from . import db
from datetime import datetime
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import json

ld = Blueprint('ld', __name__)


admin_permission = Permission(RoleNeed('admin'))

@ld.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

# ---------------------------------------------------------------------------- #
#                                    GET L&D                                   #
# ---------------------------------------------------------------------------- #
@ld.route('get-learning-and-development/<emp_id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_learning_and_development(emp_id):
    if request.method == "GET":
        get_ld = Learning_Development.query.filter_by(user_id = emp_id).all()
        column_keys = Learning_Development.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
    # Iterate through the returned output data set
        for row in get_ld:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
            print(rows_dic)

        return jsonify(rows_dic)

    # if request.method == "POST":
        
    #     return "ok", 200
 # ---------------------------------------------------------------------------- #



 # ---------------------------------------------------------------------------- #
 #                                    ADD L&D                                   #
 # ---------------------------------------------------------------------------- #
@ld.route('add-learning-and-development/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_learning_and_development(emp_id):
    formdata = request.form.to_dict()
    print('DATA', formdata)
    if request.method == "POST":
        formdata['user_id'] = emp_id
        new_ld = Learning_Development(**formdata)
        db.session.add(new_ld)
        db.session.commit()
        
        return jsonify()
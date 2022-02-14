
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import User, Shirt
from . import db
#from datetime import datetime
import datetime
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import os, os.path
import json
from werkzeug.security import generate_password_hash, check_password_hash

ALLOWED_EXTENSIONS = {'pdf'}

shirt = Blueprint('shirt', __name__)

admin_permission = Permission(RoleNeed('admin'))

@shirt.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

@shirt.route('add-shirt-size/<emp_id>', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def add_shirt_size(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        user = User.query.get(emp_id)
        
        if formdata['add_or_update'] == 'add':
            formdata.pop('add_or_update')
            formdata['user_id'] = emp_id
            finaldata = Shirt(**formdata)
            db.session.add(finaldata)
            db.session.flush()
            db.session.commit()
            return jsonify('Successfully Added Shirt Size')

        else:
            user.polo_shirt_size = formdata['polo_shirt_size']
            db.session.commit()
            return jsonify('Successfully Updated Shirt Size')
        
    return 'ok', 200
    
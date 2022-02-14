from pprint import pprint
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Family_Background
from . import db
import datetime
import time
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import json
import os, os.path

familyBg = Blueprint('familyBg', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@familyBg.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------------------------------------------------------------------- #
#                              GET FAMILY BG                                   #
# ---------------------------------------------------------------------------- #
@familyBg.route('get-familyBg/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_family_background(emp_id):
        
        
        return jsonify({})

# ---------------------------------------------------------------------------- #
#                                 ADD FAMILY BG                                #
# ---------------------------------------------------------------------------- #
@familyBg.route('add-familyBg/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_family_background(emp_id):
        if request.method == "POST":
            formdata = request.form.to_dict()

            for xy in range(1, int(formdata['family_count']) + 1):
                # try:

                
                if 'fb_last_name['+str(xy)+']' in formdata:
                    fb_last_name = formdata['fb_last_name['+str(xy)+']']
                else:
                    fb_last_name = None
                if 'fb_first_name['+str(xy)+']' in formdata:
                    fb_first_name = formdata['fb_first_name['+str(xy)+']']
                else:
                    fb_first_name = None
                if 'fb_middle_name['+str(xy)+']' in formdata:
                    fb_middle_name = formdata['fb_middle_name['+str(xy)+']']
                else:
                    fb_middle_name = None
                if 'fb_name_ext['+str(xy)+']' in formdata:
                    fb_name_ext = formdata['fb_name_ext['+str(xy)+']']
                else:
                    fb_name_ext = None
                if 'fb_occupation['+str(xy)+']' in formdata:
                    fb_occupation = formdata['fb_occupation['+str(xy)+']']
                else:
                    fb_occupation = None
                if 'fb_employer_business_name['+str(xy)+']' in formdata:
                    fb_employer_business_name = formdata['fb_employer_business_name['+str(xy)+']']
                else:
                    fb_employer_business_name = None
                if 'fb_business_address['+str(xy)+']' in formdata:
                    fb_business_address = formdata['fb_business_address['+str(xy)+']']
                else:
                    fb_business_address = None
                if 'fb_contact_no['+str(xy)+']' in formdata:
                    fb_contact_no = formdata['fb_contact_no['+str(xy)+']']
                else:
                    fb_contact_no = None
                if 'fb_date_of_birth['+str(xy)+']' in formdata:
                    fb_date_of_birth = formdata['fb_date_of_birth['+str(xy)+']']
                else:
                    fb_date_of_birth = None
                if 'fb_maiden_name['+str(xy)+']' in formdata:
                    fb_maiden_name = formdata['fb_maiden_name['+str(xy)+']']
                else:
                    fb_maiden_name = None
                if 'fb_relationship['+str(xy)+']' in formdata:
                    fb_relationship = formdata['fb_relationship['+str(xy)+']']
                else:
                    fb_relationship = None

                new_family_bg = Family_Background(
                fb_last_name = fb_last_name,
                fb_first_name = fb_first_name,
                fb_middle_name = fb_middle_name,
                fb_name_ext = fb_name_ext,
                fb_occupation = fb_occupation,
                fb_employer_business_name = fb_employer_business_name,
                fb_business_address = fb_business_address,
                fb_contact_no = fb_contact_no,
                fb_date_of_birth = fb_date_of_birth,
                fb_maiden_name = fb_maiden_name,
                fb_relationship = fb_relationship,
                user_id = emp_id
                    )
                db.session.add(new_family_bg)
                db.session.commit()

                # except KeyError as e:
                #     print(e)
                #     formdata[e] = None



        return jsonify('Successfully submitted')
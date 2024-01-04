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
# import pprint

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
                if 'fb_id['+str(xy)+']' in formdata:
                    fb_id = formdata['fb_id['+str(xy)+']']
                else:
                    fb_id = None
                if 'fb_id_no['+str(xy)+']' in formdata:
                    fb_id_no = formdata['fb_id_no['+str(xy)+']']
                else:
                    fb_id_no = None
                if 'fb_deceased['+str(xy)+']' in formdata:
                    fb_deceased = formdata['fb_deceased['+str(xy)+']']
                else:
                    fb_deceased = None
                if 'fb_date_issued['+str(xy)+']' in formdata:
                    fb_date_issued = formdata['fb_date_issued['+str(xy)+']']
                else:
                    fb_date_issued = None
                


                new_family_bg = Family_Background(
                fb_last_name = str(fb_last_name).upper(),
                fb_first_name = str(fb_first_name).upper(),
                fb_middle_name = str(fb_middle_name).upper(),
                fb_name_ext = str(fb_name_ext).upper(),
                fb_occupation = str(fb_occupation).upper(),
                fb_employer_business_name = str(fb_employer_business_name).upper(),
                fb_business_address = str(fb_business_address).upper(),
                fb_contact_no = fb_contact_no,
                fb_date_of_birth = fb_date_of_birth,
                fb_maiden_name = str(fb_maiden_name).upper(),
                fb_relationship = str(fb_relationship).upper(),
                fb_id = str(fb_id).upper(),
                fb_id_no = str(fb_id_no).upper(),
                fb_date_issued = str(fb_date_issued).upper(),
                fb_deceased = str(fb_deceased),
                user_id = emp_id
                    )

                if fb_last_name is not None and fb_first_name is not None:
                    db.session.add(new_family_bg)
                    db.session.commit()

                # except KeyError as e:
                #     print(e)
                #     formdata[e] = None



        return jsonify('Successfully Saved Family Background - add')

# ---------------------------------------------------------------------------- #
#                                 ADD FAMILY BG                                #
# ---------------------------------------------------------------------------- #
@familyBg.route('update-familyBg/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def update_family_background(emp_id):

    formdata = request.form.to_dict()
    # print('UPDATE FAMILY BG: ', formdata)
    pprint(formdata)
    for xy in range(1, int(formdata['child_count'])+5):
        if 'id['+str(xy)+']' in formdata:
            id = formdata['id['+str(xy)+']']
        else:
            id = None
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
        if 'fb_id['+str(xy)+']' in formdata:
            fb_id = formdata['fb_id['+str(xy)+']']
        else:
            fb_id = None
        if 'fb_id_no['+str(xy)+']' in formdata:
            fb_id_no = formdata['fb_id_no['+str(xy)+']']
        else:
            fb_id_no = None
        if 'fb_deceased['+str(xy)+']' in formdata:
            if formdata['fb_deceased['+str(xy)+']']:
                fb_deceased = formdata['fb_deceased['+str(xy)+']']
        else:
            fb_deceased = 'unchecked' 
        if 'fb_date_issued['+str(xy)+']' in formdata:
            fb_date_issued = formdata['fb_date_issued['+str(xy)+']']
        else:
            fb_date_issued = None
    
        familyBg = Family_Background.query.filter_by(id = id)
        familyBg.update(dict(
                        fb_last_name = str(fb_last_name).upper(),
                        fb_first_name = str(fb_first_name).upper(),
                        fb_middle_name = str(fb_middle_name).upper(),
                        fb_name_ext = str(fb_name_ext).upper(),
                        fb_occupation = str(fb_occupation).upper(),
                        fb_employer_business_name = str(fb_employer_business_name).upper(),
                        fb_business_address = str(fb_business_address).upper(),
                        fb_contact_no = fb_contact_no,
                        fb_date_of_birth = fb_date_of_birth,
                        fb_maiden_name = str(fb_maiden_name).upper(),
                        fb_relationship = str(fb_relationship).upper(),
                        fb_id = str(fb_id).upper(),
                        fb_id_no = str(fb_id_no).upper(),
                        fb_deceased = str(fb_deceased),
                        fb_date_issued = str(fb_date_issued).upper(),
                        ))

    db.session.commit()
    return jsonify("Successfully Updated Family Background")


# ---------------------------------------------------------------------------- #
#                              DELETE FAMILY BG                                #
# ---------------------------------------------------------------------------- #
@familyBg.route('delete-familyBg/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def delete_family_background(emp_id):
    formdata  = json.loads(request.data)
		
    delete_child = Family_Background.query.get(formdata['id'])

    db.session.delete(delete_child)
    db.session.commit()

    return jsonify('Child Removed!')

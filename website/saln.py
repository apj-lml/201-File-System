from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app, send_file
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Real_Property, Personal_Property, Liability, Business_Interest, Relatives_In_Government, User, UserSchema
from . import db
import datetime
import time
from .myhelper import allowed_file, my_random_string
from werkzeug.utils import secure_filename
from io import BytesIO
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
import json
import os, os.path

saln = Blueprint('saln', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@saln.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------- #
#                              add real property                               #
# ---------------------------------------------------------------------------- #
@saln.route('add-rp/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_rp(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        formdata["user_id"] = emp_id

        add_rp = Real_Property(**formdata)

        db.session.add(add_rp)
        db.session.commit()
        db.session.flush()

        print(formdata)
        return jsonify(**formdata)

 # ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                              add personal property                           #
# ---------------------------------------------------------------------------- #
@saln.route('add-pp/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_pp(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        formdata["user_id"] = emp_id

        add_rp = Personal_Property(**formdata)

        db.session.add(add_rp)
        db.session.commit()
        db.session.flush()

        print(formdata)
        return jsonify(**formdata)

 # ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                             add liability property                           #
# ---------------------------------------------------------------------------- #
@saln.route('add-liability/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_liability(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        formdata["user_id"] = emp_id

        new_liability = Liability(**formdata)

        db.session.add(new_liability)
        db.session.commit()
        db.session.flush()

        print(formdata)
        return jsonify(**formdata)

 # ---------------------------------------------------------------------------- #

 # ---------------------------------------------------------------------------- #
#                             add liability property                           #
# ---------------------------------------------------------------------------- #
@saln.route('add-business-interest/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_business_interest(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        formdata["user_id"] = emp_id

        new_business_interest = Business_Interest(**formdata)

        db.session.add(new_business_interest)
        db.session.commit()
        db.session.flush()

        print(formdata)
        return jsonify(**formdata)

 # ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                             add liability property                           #
# ---------------------------------------------------------------------------- #
@saln.route('add-relative-in-government/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_relative_in_government(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        formdata["user_id"] = emp_id

        new_relative_in_government = Relatives_In_Government(**formdata)

        db.session.add(new_relative_in_government)
        db.session.commit()
        db.session.flush()

        print(formdata)
        return jsonify(**formdata)

# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                PRINT SALN                                    #
# ---------------------------------------------------------------------------- #
@saln.route('print/<emp_id>', methods=['POST', 'GET'])
@login_required
def print_saln(emp_id):
    # formdata  = json.loads(request.data)
    template = os.path.join(current_app.root_path, 'static/templates', 'SALN_Form.docx')   

    document = from_template(template, emp_id)
    document.seek(0)
    
    return send_file(
        document, mimetype='application/vnd.openxmlformats-'
        'officedocument.wordprocessingml.document', as_attachment=True,
        attachment_filename='SALN.docx')

 # ---------------------------------------------------------------------------- #

def from_template(template, emp_id):
    target_file = BytesIO()
    
    template = DocxTemplate(template)
    context = get_context(emp_id)  # gets the context used to render the document
    
    target_file = BytesIO()
    template.render(context, autoescape=True)
    template.save(target_file)
    return target_file

def get_context(id):
    user = db.session.query(User).get(id)
    user_profile = user

    # # Update the position_title to title case
    # user_profile.position_title = user_profile.position_title.title()
    # user_profile.employment_status = user_profile.employment_status.title()

    middle_name = user_profile.middle_name[:1] + "." if user_profile.middle_name and user_profile.middle_name != "N/A" else ""
    name_extn = user_profile.name_extn if user_profile.name_extn and user_profile.name_extn != "N/A" else ""

    # Calculate and set the full_name field in the serialized JSON
    user_profile_dict = UserSchema().dump(user_profile)
    user_profile_dict['full_name'] = user_profile.first_name + " " + middle_name + " " + user_profile.last_name + " " + name_extn
    user_profile_dict['address'] = user_profile.p_house_block_lot + ", " + user_profile.p_street + ", " + user_profile.p_subdivision_village + ", " + user_profile.p_barangay + ", " + user_profile.p_city_municipality + ", "+ user_profile.p_province + ", "+ user_profile.p_zip_code
    # user_profile_dict['spouse_last_name'] = user_profile.familyBg.filter_by(fb_relationship='SPOUSE').first()

    spouse = None
    for relative in user_profile.familyBg:
        if relative.fb_relationship == 'SPOUSE':
            spouse = relative
            break

    user_profile_dict['spouse_last_name'] = spouse.fb_last_name if spouse else "N/A"
    user_profile_dict['spouse_first_name'] = spouse.fb_first_name if spouse else "N/A"
    user_profile_dict['spouse_middle_name'] = spouse.fb_middle_name if spouse else "N/A"
    user_profile_dict['spouse_middle_initial'] = spouse.fb_middle_name[0] + "." if spouse else "N/A"
    user_profile_dict['spouse_full_name'] = spouse.fb_first_name + " " + spouse.fb_middle_name[0] + ". " + spouse.fb_last_name if spouse else "N/A"
    # user_profile_dict['spouse_last_name'] = user_profile.familyBg.filter_by(fb_relationship='SPOUSE').first().last_name if user_profile.familyBg else None


    user_profile_dict['spouse_position'] = spouse.fb_occupation if spouse else "N/A"
    user_profile_dict['spouse_agency'] = spouse.fb_employer_business_name if spouse else "N/A"
    user_profile_dict['spouse_office_address'] = spouse.fb_business_address if spouse else "N/A"
    user_profile_dict["checkmark"] = "✓"

    print("====================>>>>>>>>>>>>: ", user_profile_dict)
    # Return the modified serialized data
    return user_profile_dict
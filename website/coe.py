from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app, send_file
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import User, UserSchema
from . import db
import os
from io import BytesIO
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from flask_login import current_user, login_required
import json

from datetime import datetime, date

coe = Blueprint('coe', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@coe.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

def add_comma(number):
    return ("{:,.2f}".format(number))

def get_day(date_obj):
    return date_obj.day

def format_current_date():
    current_date = datetime.now().date()

    # day = current_date.strftime("%d").lstrip("0").rstrip("0")
    day = current_date.strftime("%e")

    suffix = "th" if 11 <= int( get_day(current_date)) % 100 <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(int( get_day(current_date)) % 10, "th")
    formatted_date = current_date.strftime(f"{day}{suffix} day of %B, %Y")
    return formatted_date


def get_context(id, salary):
    """ You can generate your context separately since you may deal with a lot 
        of documents. You can carry out computations, etc in here and make the
        context look like the sample below.
    """
    user = db.session.query(User).get(id)
    user_profile = user

    # Update the position_title to title case
    user_profile.position_title = user_profile.position_title.title()
    user_profile.employment_status = user_profile.employment_status.title()

    middle_name = user_profile.middle_name[:1] + "." if user_profile.middle_name and user_profile.middle_name != "N/A" else ""
    name_extn = user_profile.name_extn if user_profile.name_extn and user_profile.name_extn != "N/A" else ""

    # Calculate and set the full_name field in the serialized JSON
    user_profile_dict = UserSchema().dump(user_profile)
    user_profile_dict['full_name'] = user_profile.first_name + " " + middle_name + " " + user_profile.last_name + " " + name_extn
    user_profile_dict['salary'] = salary

    conv_salary = user_profile_dict['salary'].split()
    if len(conv_salary) == 2:
        
        salary_string = conv_salary[1].replace(',', '')  # Removing commas from the string
 
        if user_profile_dict['employment_status'] == "Job Order" or user_profile_dict['employment_status'] == "Casual":
            basic_salary = (float(salary_string) * 22) 
        else:
            basic_salary = float(salary_string)

    user_profile_dict['basic_salary'] = float(basic_salary) * 12
    user_profile_dict['pera'] = 2000.00 * 12
    user_profile_dict['midyear'] = float(basic_salary) * 2
    user_profile_dict['uniform'] = 6000.00
    user_profile_dict['cash_gift'] = 5000.00
    user_profile_dict['pei'] = 5000.00

    user_profile_dict['total_gross'] = add_comma(float(user_profile_dict['basic_salary']) + float(user_profile_dict['pera']) +  float(user_profile_dict['midyear']) + float(user_profile_dict['uniform']) + float(user_profile_dict['cash_gift']) + float(user_profile_dict['pei']))
    user_profile_dict['basic_salary'] = add_comma(user_profile_dict['basic_salary'])
    user_profile_dict['pera'] = add_comma(user_profile_dict['pera'])
    user_profile_dict['midyear'] = add_comma(user_profile_dict['midyear'])
    user_profile_dict['uniform'] = add_comma(user_profile_dict['uniform'])
    user_profile_dict['cash_gift'] = add_comma(user_profile_dict['cash_gift'])
    user_profile_dict['pei'] = add_comma(user_profile_dict['pei'])

    user_profile_dict['current_date'] = format_current_date()

    # Return the modified serialized data
    return user_profile_dict


def from_template(template, emp_id, salary):
    target_file = BytesIO()
    
    template = DocxTemplate(template)
    context = get_context(emp_id, salary)  # gets the context used to render the document
    
    target_file = BytesIO()
    template.render(context, autoescape=True)
    template.save(target_file)

    return target_file

@coe.route("/without-compensation/<emp_id>", methods=['GET', 'POST'])
def coe_without_compensation(emp_id):

    formdata  = json.loads(request.data)
    template = os.path.join(current_app.root_path, 'static/templates', 'coe-without-compensation.docx')   

    document = from_template(template, emp_id, formdata['monthly_daily_salary'])
    document.seek(0)
    
    return send_file(
        document, mimetype='application/vnd.openxmlformats-'
        'officedocument.wordprocessingml.document', as_attachment=True,
        attachment_filename='WES_TEMPLATE_NEW.docx')

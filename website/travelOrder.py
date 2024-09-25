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
from pprint import pprint

from datetime import datetime, date

travelOrder = Blueprint('travelOrder', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@travelOrder.errorhandler(403)
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


def get_context(id, formdata):
    """ You can generate your context separately since you may deal with a lot 
        of documents. You can carry out computations, etc in here and make the
        context look like the sample below.
    """

    user_schema = UserSchema(many=True)

    # Convert selected IDs to integers if needed
    ids = [int(id) for id in formdata['selectedIds']]
    
    is_outside_ilocos = formdata['is_outside_ilocos']
    date_from = formdata['date_from']
    date_to = formdata['date_to']
    location = formdata['location']
    purpose = formdata['purpose']

    # Query the users by their IDs
    creators = db.session.query(User).filter(User.id.in_(ids)).all()

    my_rows = json.loads(jsonify(row_contents=user_schema.dump(creators)).get_data(True))
    for idx, item in enumerate(my_rows["row_contents"]):
        middle_name = item['middle_name'][:1]+"." if item['middle_name'] != "" or item['middle_name'] is not None or item['middle_name'] != "N/A" else ""
        name_extn = item['name_extn'] if item['name_extn'] != "" and item['name_extn'] is not None and item['name_extn'] != "N/A" else ""

        item['full_name'] = item['first_name'] + " " + middle_name + " " + item['last_name'] + " " + name_extn

    creator = db.session.query(User).get(id)

    middle_name = creator.middle_name[:1] + "." if creator.middle_name not in ["", None, "N/A"] else ""
    name_extn = creator.name_extn if creator.name_extn not in ["", None, "N/A"] else ""

    creator.myfullname = f"{creator.first_name} {middle_name} {creator.last_name} {name_extn}"

    # creators = db.session.query(User).filter(User.id.in_(ids)).all()

    # Update the position_title to title case

    # for creator in creators:
    #     creator.position_title = creator.position_title.title()
    #     creator.employment_status = creator.employment_status.title()

    creator_dict = UserSchema().dump(creator)
    creator_dict['myfullname'] = f"{creator.first_name} {middle_name} {creator.last_name} {name_extn}"

    return {
        'row_contents': my_rows["row_contents"],
        'creator': creator_dict,
        'enumerate': enumerate,  # Add enumerate to the context
        'is_outside_ilocos' : is_outside_ilocos,
        'date_from' : date_from,
        'date_to' : date_to,
        'location' : location,
        'purpose' : purpose
    }



def from_template(template, creator_id, formdata):
    target_file = BytesIO()
    
    template = DocxTemplate(template)
    context = get_context(creator_id, formdata)  # gets the context used to render the document
    
    target_file = BytesIO()
    template.render(context, autoescape=True)
    template.save(target_file)

    return target_file



@travelOrder.route("/print-to/<creator_id>", methods=['GET', 'POST'])
def printTravelOrder(creator_id):

    formdata = json.loads(request.data)
    template = os.path.join(current_app.root_path, 'static/templates', 'TRAVEL_ORDER_TEMPLATE.docx')   

    document = from_template(template, creator_id, formdata)
    document.seek(0)
    
    return send_file(
        document, mimetype='application/vnd.openxmlformats-'
        'officedocument.wordprocessingml.document', as_attachment=True,
        attachment_filename='TRAVEL_ORDER_TEMPLATE.docx')
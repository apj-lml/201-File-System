from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app, send_file
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import User, UserSchema, Travel_Order
from . import db
import os
from io import BytesIO
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from flask_login import current_user, login_required
import json
from pprint import pprint

from datetime import datetime, timedelta
from .myhelper import format_mydatetime, format_user_names, proper_datetime

from sqlalchemy import func


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


def addTravelOrder(creator_id, formdata):
    ids = [int(id) for id in formdata['selectedIds']]

    ids.append(creator_id)
    is_outside_ilocos = formdata['is_outside_ilocos'] == '1'
    date_from = formdata['date_from']
    date_to = formdata['date_to']
    location = formdata['location']
    purpose = formdata['purpose']

    for to_user_id in ids:
        existing_to = Travel_Order.query.filter_by(user_id=to_user_id).first()  # Use .first() to get the record or None
        
        if existing_to:  # Check if a record was found
            existing_to.user_id = to_user_id
            existing_to.date_from = date_from
            existing_to.date_to = date_to
            existing_to.location = location
            existing_to.purpose = purpose
            existing_to.is_outside_ilocos = is_outside_ilocos
            existing_to.creator = creator_id
        else:
            new_to = Travel_Order(
                user_id=to_user_id,
                date_from=date_from,
                date_to=date_to,
                location=location,
                purpose=purpose,
                is_outside_ilocos=is_outside_ilocos,
                creator=creator_id,
            )
            db.session.add(new_to)

    db.session.commit()

    return jsonify('Successfully Added to database!'), 200


def get_context(id, formdata):
    """ You can generate your context separately since you may deal with a lot 
        of documents. You can carry out computations, etc in here and make the
        context look like the sample below.
    """

    user_schema = UserSchema(many=True)

    # Convert selected IDs to integers if needed
    ids = [int(id) for id in formdata['selectedIds']]
    
    is_outside_ilocos = formdata['is_outside_ilocos']
    date_from = proper_datetime(formdata['date_from'])
    date_to = proper_datetime(formdata['date_to'])
    location = formdata['location']
    purpose = formdata['purpose']

    # Query the users by their IDs
    to_users = db.session.query(User).filter(User.id.in_(ids)).all()

    my_rows = json.loads(jsonify(row_contents=user_schema.dump(to_users)).get_data(True))
    for idx, item in enumerate(my_rows["row_contents"]):
        middle_name = item['middle_name'][:1]+"." if item['middle_name'] != "" or item['middle_name'] is not None or item['middle_name'] != "N/A" else ""
        name_extn = item['name_extn'] if item['name_extn'] != "" and item['name_extn'] is not None and item['name_extn'] != "N/A" else ""

        item['full_name'] = item['first_name'] + " " + middle_name + " " + item['last_name'] + " " + name_extn
        item['position_title'] = item['position_title'].lower().title()

    creator = db.session.query(User).get(id)

    middle_name = creator.middle_name[:1] + "." if creator.middle_name not in ["", None, "N/A"] else ""
    name_extn = creator.name_extn if creator.name_extn not in ["", None, "N/A"] else ""

    creator_dict = UserSchema().dump(creator)
    creator_dict['myfullname'] = f"{creator.first_name} {middle_name} {creator.last_name} {name_extn}"
    creator_dict['position_title'] = creator.position_title.title()

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
    
    addTravelOrder(creator_id, formdata)

    document = from_template(template, creator_id, formdata)
    document.seek(0)
    
    return send_file(
        document, mimetype='application/vnd.openxmlformats-'
        'officedocument.wordprocessingml.document', as_attachment=True,
        attachment_filename='TRAVEL_ORDER_TEMPLATE.docx')


# ---------------------------------------------------------------------------- #
#                          GET CAL ACTIVITIES IDS                              #
# ---------------------------------------------------------------------------- #
@travelOrder.route('/get-all-to-events', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_all_to_events():
    if request.method == "GET":
        # calendarEvents = db.session.query(Travel_Order).all()

        calendarEvents = db.session.query(
            Travel_Order
        ).group_by(
            Travel_Order.creator, 
            Travel_Order.date_from, 
            Travel_Order.date_to
        ).all()
        
        formattedEvents = []

        calendarEvents

        for ev in calendarEvents:

            calendarEvents = db.session.query(
                Travel_Order
            ).group_by(
                Travel_Order.creator, 
                Travel_Order.date_from, 
                Travel_Order.date_to
            ).all()

            calendarUsers = Travel_Order.query.filter(
                Travel_Order.creator == ev.creator, 
                Travel_Order.date_from == ev.date_from, 
                Travel_Order.date_to == ev.date_to
            ).all()

            formattedCalendarUsers = []
            for calendarUser in calendarUsers:
                selectedUser = User.query.filter(
                    User.id == calendarUser.user_id
                ).first()

                formattedCalendarUsers.append({
                    'id' : selectedUser.id,
                    'fullname' : selectedUser.proper_fullname,
                    })
                
            # Sort the array to make ev.creator the first element
            formattedCalendarUsers.sort(key=lambda user: 0 if user['id'] == ev.creator else 1)

            formattedEvents.append({
                'id' : ev.id,
                'title' : format_user_names(formattedCalendarUsers),
                'location' : ev.location,
                'is_outside_ilocos' : ev.is_outside_ilocos,
                'purpose' : ev.purpose,
                'creator' : ev.creator,
                'start' : ev.date_from.strftime('%Y-%m-%d'),
                # 'end' : ev.date_to.strftime('%Y-%m-%d'),
                'end': str((ev.date_to + timedelta(days=1)).strftime('%Y-%m-%d')),
                'allDay': True,
                'date_created' : ev.date_created,
                'toUsers' : formattedCalendarUsers
            })

        # raise Exception(formattedEvents)

              
        return jsonify(formattedEvents)

@travelOrder.route('/get-specific-to-events/<date_from>/<date_to>/<creator>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_specific_to_events(date_from, date_to, creator):
    if request.method == "GET":
        # calendarEvents = db.session.query(Travel_Order).all()

        date_to_datetime = datetime.strptime(date_to, '%Y-%m-%d')

        # Subtract 1 day
        adjusted_date_to = (date_to_datetime - timedelta(days=1)).strftime('%Y-%m-%d')

        travelOrders = Travel_Order.query.filter(
            Travel_Order.date_from == date_from,
            Travel_Order.date_to == adjusted_date_to,
            Travel_Order.creator == creator
        ).all()
        
        formattedEvents = []
 

        for ev in travelOrders:
            formattedEvents.append({
                'id' : ev.id,
                'user_id' : ev.user_id,
                'date_from' : ev.date_from.strftime('%Y-%m-%d'),
                'date_to' : ev.date_to.strftime('%Y-%m-%d'),
                # 'date_to' : ev.date_to.strftime('%Y-%m-%d'),
                'purpose' : ev.purpose,
                'location' : ev.location,
                'is_outside_ilocos' : ev.is_outside_ilocos,
                'creator' : ev.creator,
                'date_created' : ev.date_created,
            })

            
        return jsonify(formattedEvents)
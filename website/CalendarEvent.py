
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from sqlalchemy import extract
from .models import Calendar_Events, User
import datetime
import json
from dateutil.relativedelta import relativedelta
from . import db

# import pprint

calendarEvent = Blueprint('calendarEvent', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@calendarEvent.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------- #
#                           ADD CALENDAR ACTIVITIES                            #
# ---------------------------------------------------------------------------- #
@calendarEvent.route('/add-event', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_event():
    if request.method == "POST":
        formdata = request.form.to_dict()

        formattedEvents = []

        # if formdata['e_all_day'] == 'on':
        if 'e_all_day' in formdata:
            formdata['e_all_day'] = True
        else:
            formdata['e_all_day'] = False

        newCalendarEvent = Calendar_Events(
            **formdata
        )

        db.session.add(newCalendarEvent)

        db.session.commit()

        last_inserted_id = newCalendarEvent.id

        date_to_string = formdata['e_date_to']

        try:
            # Try parsing with time component
            date_to = datetime.datetime.strptime(date_to_string, '%Y-%m-%dT%H:%M').date()
        except ValueError:
            # Parsing failed, try parsing without time component
            date_to = datetime.datetime.strptime(date_to_string, '%Y-%m-%d').date()

        
        # e_date_to_modified = ev.e_date_to + datetime.timedelta(days=1)
        formattedEvents.append({
                'id' : last_inserted_id,
                'title' : formdata['e_title'],
                'description' : None,
                'start' : formdata['e_date_from'],
                'end' : (date_to + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                'allDay': formdata['e_all_day'],
            })

        # return jsonify('Successfully Added Event')
        return jsonify(formattedEvents)
        # return jsonify(**formdata)


# ---------------------------------------------------------------------------- #
#                           UPDATE CAL ACTIVITIES                              #
# ---------------------------------------------------------------------------- #

@calendarEvent.route('/update-event', methods=['POST'])
@login_required
#@admin_permission.require(http_exception=403)
def update_event():
    if request.method == "POST":
        # formdata = request.form.to_dict()
        formdata = request.json  # Access JSON data from the request body
        print('======>', formdata)
        eventToUpdate = Calendar_Events().query.filter_by(id = formdata['id']).first()

        # try:
        # Try parsing with time component
        # date_to = datetime.datetime.strptime(formdata['start'], '%Y-%m-%d %H:%M:%S').date()
        # date_from = datetime.datetime.strptime(formdata['end'], '%Y-%m-%d %H:%M:%S').date()
        # except ValueError:
        #     # Parsing failed, try parsing without time component
        #     date_to = datetime.datetime.strptime(formdata['start'], '%Y-%m-%d').date()
        #     date_from = datetime.datetime.strptime(formdata['end'], '%Y-%m-%d').date()
            

        eventToUpdate.e_date_from = formdata['start']
        eventToUpdate.e_date_to = formdata['end']
        db.session.commit()
        
    return jsonify('Event Successfully Updated!'), 200


# ---------------------------------------------------------------------------- #
#                          GET CAL ACTIVITIES IDS                              #
# ---------------------------------------------------------------------------- #
@calendarEvent.route('/get-all-events', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_all_events():
    if request.method == "GET":
        calendarEvents = db.session.query(Calendar_Events).all()

        formattedEvents = []

        for ev in calendarEvents:
            if ev.e_all_day:
                e_date_to_modified = ev.e_date_to + datetime.timedelta(days=1)
            else:
                e_date_to_modified = ev.e_date_to

            e_date_to_modified_final = e_date_to_modified.strftime('%Y-%m-%d %H:%M:%S')
                
            formattedEvents.append({
                'id' : ev.id,
                'title' : ev.e_title,
                'description' : ev.e_description,
                'start' : ev.e_date_from.strftime('%Y-%m-%d %H:%M:%S'),
                'end' : e_date_to_modified_final,
                'allDay': ev.e_all_day,
                # 'rrule': {
                #     'freq': 'yearly',
                #     'dtstart': ev.e_date_from.strftime('%Y-%m-%d %H:%M:%S'),
                #     'until': e_date_to_modified_final
                #     # 'until': e_date_to_modified_final
                # }
            })
        

        # print("=========>", formattedEvents)

              
        return jsonify(formattedEvents)

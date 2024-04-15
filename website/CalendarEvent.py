
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

        # new_family_bg = Family_Background(
        #     e_description = str(fb_last_name),
        #     e_type = str(fb_first_name).upper(),
        #     e_date_from = str(fb_middle_name).upper(),
        #     e_date_to = str(fb_name_ext).upper(),
        #     start_recurring_date = str(fb_occupation).upper(),
        #     end_recurring_date = str(fb_employer_business_name).upper(),
        #     last_updated = str(fb_business_address).upper()
        #         )
        db.session.add(newCalendarEvent)

        db.session.commit()

        date_to_string = formdata['e_date_to']

        try:
            # Try parsing with time component
            date_to = datetime.datetime.strptime(date_to_string, '%Y-%m-%dT%H:%M').date()
        except ValueError:
            # Parsing failed, try parsing without time component
            date_to = datetime.datetime.strptime(date_to_string, '%Y-%m-%d').date()

        
        # e_date_to_modified = ev.e_date_to + datetime.timedelta(days=1)
        formattedEvents.append({
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
            if ev.e_date_from != ev.e_date_to:
                # allDay = True
                e_date_to_modified = ev.e_date_to + datetime.timedelta(days=1)
            else:
                # allDay = False
                e_date_to_modified = ev.e_date_to

            e_date_to_modified_final = e_date_to_modified.strftime('%Y-%m-%d %H:%M:%S')
                
            formattedEvents.append({
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
        

        print("=========>", formattedEvents)

              
        return jsonify(formattedEvents)


from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from sqlalchemy import extract
from .models import Calendar_Events, User
import datetime
import json
from dateutil.relativedelta import relativedelta
from . import db


calendarEvent = Blueprint('calendarEvent', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

color = {
    'MEETING':'#A4E9D5',
    'SPECIAL HOLIDAY':'#a7d4e8',
    'REGULAR HOLIDAY':'#f0a8a8',
    'OTHERS':'#CCCCFF',
    'DEADLINE':'#FCCB06',
    'TRAINING':'#340336',
    'WORK SUSPENSION':'#fccbc7',
}

textColor = {
    'MEETING':'#194015',
    'SPECIAL HOLIDAY':'#1b495e',
    'REGULAR HOLIDAY':'#731717',
    'OTHERS':'#28283b',
    'DEADLINE':'#917503',
    'TRAINING':'#fdd6ff',
    'WORK SUSPENSION':'#300400',
}


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
            date_to = date_to_string
            # date_to = datetime.datetime.strptime(date_to_string, '%Y-%m-%dT%H:%M')
        except ValueError:
            # Parsing failed, try parsing without time component
            date_to = (datetime.datetime.timedelta(days=1)).strptime(date_to_string, '%Y-%m-%d').date()
            

        rrule = None
        if formdata['e_repeat'] is not None and formdata['e_repeat'] != "":
            rrule = {
                'freq': formdata['e_repeat'],
                # 'byweekday': ["su", "mo", "tu", "we", "th", "fr"],
                'dtstart': formdata['e_date_from'].strftime('%Y-%m-%d %H:%M:%S')
            }

        if formdata['e_type'] == 'WORK SUSPENSION':
                background = 'background'
        else:
            background = ''
        
        # e_date_to_modified = ev.e_date_to + datetime.timedelta(days=1)
        formattedEvents.append({
                'id' : last_inserted_id,
                'title' : formdata['e_title'],
                'description' : formdata['e_description'],
                'repeat' : formdata['e_repeat'],
                'e_type' : formdata['e_type'],
                'venue' : formdata['e_venue'],
                'start' : formdata['e_date_from'],
                # 'end' : (date_to + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                'end' : date_to,
                'allDay': formdata['e_all_day'],
                'color' : color[formdata['e_type']],
                'textColor' : textColor[formdata['e_type']],
                'display': background,
                'rrule': rrule
                
            })

        # return jsonify('Successfully Added Event')
        return jsonify(formattedEvents)
        # return jsonify(**formdata)



# ---------------------------------------------------------------------------- #
#                           ADD CALENDAR ACTIVITIES                            #
# ---------------------------------------------------------------------------- #
@calendarEvent.route('/update-event-all', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def update_event_all():
    if request.method == "POST":
        formdata = request.form.to_dict()

        formattedEvents = []

        # if formdata['e_all_day'] == 'on':
        if 'e_all_day' in formdata:
            formdata['e_all_day'] = True
        else:
            formdata['e_all_day'] = False

        updateEvent = Calendar_Events.query.filter_by(id = formdata['e_id'])
        updateEvent.update(dict(
                        e_title = formdata['e_title'], 
                        e_venue = formdata['e_venue'], 
                        e_all_day = formdata['e_all_day'],
                        e_type = formdata['e_type'], 
                        e_repeat = formdata['e_repeat'],
                        e_date_from = formdata['e_date_from'],
                        e_date_to = formdata['e_date_to'],
                        e_description = formdata['e_description'],
                        ))

        db.session.commit()

        date_to_string = formdata['e_date_to']
        date_from_string = formdata['e_date_from']

        try:
            # Try parsing with time component
            date_to = datetime.datetime.strptime(date_to_string, '%Y-%m-%dT%H:%M').date()
            date_from = datetime.datetime.strptime(date_from_string, '%Y-%m-%dT%H:%M').date()
        except ValueError:
            # Parsing failed, try parsing without time component
            date_to = datetime.datetime.strptime(date_to_string, '%Y-%m-%d').date()
            date_from = datetime.datetime.strptime(date_from_string, '%Y-%m-%d').date()


        rrule = None
        if formdata['e_repeat'] is not None and formdata['e_repeat'] != "":
            rrule = {
                'freq': formdata['e_repeat'],
                # 'byweekday': ["su", "mo", "tu", "we", "th", "fr"],
                'dtstart': date_from.strftime('%Y-%m-%d %H:%M:%S')
            }

        if formdata['e_type'] == 'WORK SUSPENSION':
                background = 'background'
        else:
            background = ''


        # e_date_to_modified = ev.e_date_to + datetime.timedelta(days=1)
        formattedEvents.append({
                'id' : formdata['e_id'],
                'title' : formdata['e_title'],
                'description' : formdata['e_description'],
                'venue' : formdata['e_venue'],
                'start' : formdata['e_date_from'],
                'end' : (date_to + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
                'allDay': formdata['e_all_day'],
                'color' : color[formdata['e_type']],
                'textColor' : textColor[formdata['e_type']],
                'display': background,
                'rrule': rrule
                
            })

        # return jsonify('Successfully Added Event')
        return jsonify(formattedEvents)



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
                # e_date_to_modified = ev.e_date_to + datetime.timedelta(days=1)
                e_date_to_modified = ev.e_date_to + datetime.timedelta(days=1)
            else:
                e_date_to_modified = ev.e_date_to

            e_date_to_modified_final = e_date_to_modified.strftime('%Y-%m-%d %H:%M:%S')

            rrule = None
            if ev.e_repeat is not None and ev.e_repeat != "":
                rrule = {
                    'freq': ev.e_repeat,
                    # 'byweekday': ["su", "mo", "tu", "we", "th", "fr"],
                    'dtstart': ev.e_date_from.strftime('%Y-%m-%d %H:%M:%S')
                }
            if ev.e_type == 'WORK SUSPENSION':
                background = 'background'
            else:
                background = ''

            formattedEvents.append({
                'id' : ev.id,
                'title' : ev.e_title,
                'description' : ev.e_description,
                'e_type' : ev.e_type,
                'repeat' : ev.e_repeat,
                'venue' : ev.e_venue,
                'start' : ev.e_date_from.strftime('%Y-%m-%d %H:%M:%S'),
                'end' : e_date_to_modified_final,
                'allDay': ev.e_all_day,
                'color' : color[ev.e_type],
                'textColor' : textColor[ev.e_type],
                'display': background,
                'rrule': rrule
            })

              
        return jsonify(formattedEvents)


@calendarEvent.route('/remove-event', methods=['POST'])
@login_required
#@admin_permission.require(http_exception=403)
def remove_event():
    if request.method == "POST":
        # formdata = request.form.to_dict()
        formdata = request.json  # Access JSON data from the request body

        eventToRemove = Calendar_Events.query.get(formdata['id'])

        db.session.delete(eventToRemove)
        db.session.commit()
    
        
    return jsonify('Event Successfully Updated!'), 200

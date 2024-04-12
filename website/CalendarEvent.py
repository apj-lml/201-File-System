
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

        # new_family_bg = Family_Background(
        #     e_description = str(fb_last_name),
        #     e_type = str(fb_first_name).upper(),
        #     e_date_from = str(fb_middle_name).upper(),
        #     e_date_to = str(fb_name_ext).upper(),
        #     start_recurring_date = str(fb_occupation).upper(),
        #     end_recurring_date = str(fb_employer_business_name).upper(),
        #     last_updated = str(fb_business_address).upper()
        #         )
        # db.session.add(new_family_bg)

        # db.session.commit()

        
        return jsonify('Successfully Saved Family Background - add')


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
                allDay = True
            else:
                allDay = False
                formattedEvents.append({
                    'title' : ev.e_title,
                    'description' : ev.e_description,
                    'start' : ev.e_date_from.strftime('%Y-%m-%d %H:%M:%S'),
                    'end' : ev.e_date_to.strftime('%Y-%m-%d %H:%M:%S'),
                    'allDay': allDay
                })
        

        print("=========>", formattedEvents)

              
        return jsonify(formattedEvents)

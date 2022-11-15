import dbm
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from sqlalchemy import extract
from .models import Career_Service, User
import datetime
import json
from dateutil.relativedelta import relativedelta
from . import db

# import pprint

listOfExpiry = Blueprint('listOfExpiry', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@listOfExpiry.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------- #
#                               GET EXPIRING IDS                               #
# ---------------------------------------------------------------------------- #
@listOfExpiry.route('/', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_list_of_expiry():
    if request.method == "GET":
        date_now_plus_6_mos = datetime.date.today() + relativedelta(months=+6)
        date_now = datetime.date.today()

        get_expiry = db.session.query(User, Career_Service)\
            .filter(User.id == Career_Service.user_id)\
            .filter(Career_Service.date_of_validity > date_now)\
            .filter(Career_Service.date_of_validity <= date_now_plus_6_mos)\
            .filter(extract("day", Career_Service.date_of_validity) <= 31)\
            .filter(User.status_remarks == "ACTIVE")\
            .order_by(Career_Service.date_of_validity).all()

        get_expired = db.session.query(User, Career_Service)\
            .filter(User.id == Career_Service.user_id)\
            .filter(Career_Service.date_of_validity < date_now)\
            .filter(extract("day", Career_Service.date_of_validity) <= 31)\
            .filter(User.status_remarks == "ACTIVE")\
            .order_by(Career_Service.date_of_validity).all()

        # get_expiry_drivers = db.session.query(User, Career_Service)\
        #     .filter(User.id == Career_Service.user_id)\
        #     .filter(Career_Service.date_of_validity >= date_now)\
        #     .filter(Career_Service.date_of_validity <= date_now_plus_6_mos)\
        #     .filter(extract("day", Career_Service.date_of_validity) <= 31)\
        #     .filter(User.position_title.like("%DRIVER%") )\
        #     .filter(User.status_remarks == "ACTIVE")\
        #     .order_by(Career_Service.date_of_validity).all()

        
        return render_template('list_of_expiring_ids.html', expiring_ids = get_expiry, expired_ids = get_expired)
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


listOfLoyaltyAwardees = Blueprint('listOfLoyaltyAwardees', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@listOfLoyaltyAwardees.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------- #
#                               GET EXPIRING IDS                               #
# ---------------------------------------------------------------------------- #
@listOfLoyaltyAwardees.route('/', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_list_of_expiry():
    if request.method == "GET":

        getListOfawardees = User.query.filter(User.status_remarks == "ACTIVE").filter(User.employment_status != "JOB ORDER").all()

        
        return render_template('list-of-loyalty-awardees.html', getListOfawardees = getListOfawardees)
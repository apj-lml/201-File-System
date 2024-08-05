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


listOfStepIncrement = Blueprint('listOfStepIncrement', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@listOfStepIncrement.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------- #
#                               GET EXPIRING IDS                               #
# ---------------------------------------------------------------------------- #
@listOfStepIncrement.route('/', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_list_of_expiry():
    if request.method == "GET":

        getListOfStepIncrement = User.query.filter(User.status_remarks == "ACTIVE").filter(User.employment_status != "JOB ORDER").filter(User.employment_status != "CONTRACT OF SERVICE").filter(User.employment_status != "CASUAL").all()

        return render_template('list-of-next-step-inc.html', getListOfStepIncrement = getListOfStepIncrement)
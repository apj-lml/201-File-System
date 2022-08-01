from pprint import pprint
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Family_Background
from . import db
import datetime
import time
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import json
import os, os.path
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
        get_bday_celebs = User.query.filter(extract("month", User.birthdate) == month).filter(extract("day", User.birthdate) <= 31).order_by(extract("day", User.birthdate)).all()
        return render_template('list_of_expiring_ids.html')
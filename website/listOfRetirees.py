from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import User
from datetime import datetime, timedelta
import json
from dateutil.relativedelta import relativedelta
from . import db

# import pprint
listOfRetirees = Blueprint('listOfRetirees', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@listOfRetirees.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------- #
#                               GET RETIREES                                   #
# ---------------------------------------------------------------------------- #
@listOfRetirees.route('/', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_list_of_expiry():
    if request.method == "GET":

        today = datetime.now().date()
        sixty_years_ago = today - relativedelta(years=60)
        sixty_four_years_ago = today - relativedelta(years=64)

        getListOfRetirees = User.query.filter(User.birthdate <= sixty_years_ago).filter(User.birthdate > sixty_four_years_ago).filter(User.status_remarks == "ACTIVE").all()
        getListOfCompulsoryRetirees = User.query.filter(User.birthdate <= sixty_years_ago).filter(User.birthdate < sixty_four_years_ago).filter(User.status_remarks == "ACTIVE").all()

        # getListOfRetirees = User.query.filter(User.birthdate <= sixty_years_ago).filter(User.status_remarks == "ACTIVE").all()

    
        return render_template('list-of-retirees.html', getListOfRetirees = getListOfRetirees, getListOfCompulsoryRetirees = getListOfCompulsoryRetirees)
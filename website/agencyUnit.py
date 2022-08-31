from pprint import pprint
from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Agency_Unit
from . import db

agencyUnit = Blueprint('agencyUnit', __name__)

admin_permission = Permission(RoleNeed('admin'))

@agencyUnit.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

# ---------------------------------------------------------------------------- #
#                         GET LIST OF UNITS IN SECTION                         #
# ---------------------------------------------------------------------------- #
@agencyUnit.route('/get-agencyUnit/<agencySection>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_agencyUnit(agencySection):
  
    if request.method == "GET":
        list_of_units = Agency_Unit.query.filter_by(agency_section = agencySection).all()

        pprint(list_of_units)

        column_keys = Agency_Unit.__table__.columns.keys()
	# Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
	# Iterate through the returned output data set
        for row in list_of_units:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
			# print(rows_dic)
        return jsonify(rows_dic)

# ---------------------------------------------------------------------------- #
#                         GET LIST OF UNITS IN SECTION                         #
# ---------------------------------------------------------------------------- #
@agencyUnit.route('/get-all-agencyUnit/', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_all_agencyUnit():
  
    if request.method == "GET":
        list_of_units = Agency_Unit.query.all()

        pprint(list_of_units)

        column_keys = Agency_Unit.__table__.columns.keys()
	# Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
	# Iterate through the returned output data set
        for row in list_of_units:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
			# print(rows_dic)
        return jsonify(rows_dic)
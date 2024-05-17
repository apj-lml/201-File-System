from pprint import pprint
from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Agency_Unit
from . import db

payslip = Blueprint('payslip', __name__)

admin_permission = Permission(RoleNeed('admin'))

@payslip.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

# ---------------------------------------------------------------------------- #
#                         GET LIST OF UNITS IN SECTION                         #
# ---------------------------------------------------------------------------- #
@payslip.route('/payslips/<userId>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_payslip(userId):
  
    if request.method == "GET":
        list_of_units = Agency_Unit.query.filter_by(agency_section = userId).order_by(Agency_Unit.unit_title.asc()).all()

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
@payslip.route('/get-all-payslip/', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_all_payslip():
  
    if request.method == "GET":
        list_of_units = Agency_Unit.query.all()

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

        db.session.close()
        return jsonify(rows_dic)
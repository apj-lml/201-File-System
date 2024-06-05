from pprint import pprint
from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app, send_from_directory
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Agency_Unit, User, Payslip
from . import db
from werkzeug.utils import secure_filename
import os, os.path
import re

payslipControl = Blueprint('payslipControl', __name__)

admin_permission = Permission(RoleNeed('admin'))

@payslipControl.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------- #
#                                 UPLOAD FILES                                 #
# ---------------------------------------------------------------------------- #
@payslipControl.route('/upload-payslips/<userId>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def upload_payslips(userId):
    if request.method == "POST":
        for afile in request.files:
            files = request.files.getlist(afile)
            for myfile in files:
                filename = secure_filename(myfile.filename)
                id_part = filename.split('_')[0]

                pattern = r'(\d{4}-\d{2}-\d{2})_to_(\d{4}-\d{2}-\d{2})'
                match = re.search(pattern, filename)
                if match:
                    start_date = match.group(1)
                    end_date = match.group(2)

                user = db.session.query(User).filter_by(employee_id=id_part).first()
                
                if user:

                    payslipDupe = db.session.query(Payslip).filter_by(user_id=user.id, period_from=start_date, period_to=end_date).first()
                
                if payslipDupe:
                    existing_file_path = os.path.join(current_app.config['UPLOAD_FOLDER_PAYSLIP'], payslipDupe.filename)
                    # Delete the existing file if it exists
                    if os.path.exists(existing_file_path):
                        os.remove(existing_file_path)

                    payslipDupe.period_from = start_date
                    payslipDupe.period_to = end_date
                    payslipDupe.filename = filename
                    myfile.save(os.path.join(current_app.config['UPLOAD_FOLDER_PAYSLIP'], filename))

                else:
                    if user:
                        new_payslip = Payslip(
                            user_id = user.id,
                            period_from = start_date,
                            period_to = end_date,
                            filename = filename
                            )

                        db.session.add(new_payslip)
                        myfile.save(os.path.join(current_app.config['UPLOAD_FOLDER_PAYSLIP'], filename))

                db.session.commit()

        return jsonify('')


# ---------------------------------------------------------------------------- #
#                         GET LIST OF UNITS IN SECTION                         #
# ---------------------------------------------------------------------------- #
@payslipControl.route('/payslips/<userId>', methods=['POST', 'GET'])
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
@payslipControl.route('/download-payslip/<filename>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def download_payslip(filename):
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER_PAYSLIP'], filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
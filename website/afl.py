from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app, Response
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Learning_Development, User, Afl
from . import db
from datetime import date, datetime
import time
from .myhelper import allowed_file, my_random_string
from werkzeug.utils import secure_filename
import json
import os, os.path

afl = Blueprint('afl', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@afl.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------------------------------------------------------------------- #
#                                    GET AFL                                   #
# ---------------------------------------------------------------------------- #
@afl.route('get-afl/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def get_afl(emp_id):
    if request.method == "GET":
        get_afl = Afl.query.filter_by(user_id = emp_id).all()
        column_keys = Afl.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
    # Iterate through the returned output data set
        for row in get_afl:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
            print(rows_dic)

        return jsonify(rows_dic)

    # if request.method == "POST":
        
    #     return "ok", 200
 # ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                   EDIT AFL                                   #
# ---------------------------------------------------------------------------- #
@afl.route('edit-afl/<id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def edit_ld(id):
    afl_instance = Afl.query.get_or_404(id)

    if request.method == "GET":
        # Serialize the AFL instance to JSON
        serialized_afl = {
            'id': afl_instance.id,
            'date_of_filing': afl_instance.filing_date,
            'leave_id': afl_instance.leave_id,
            'no_working_days_applied_for': afl_instance.no_working_days_applied_for,
            'date_range': afl_instance.date_range,
            'date_start': afl_instance.date_start,
            'date_end': afl_instance.date_end
            # Add other fields as needed
        }

        return jsonify(serialized_afl)

    elif request.method == 'POST':

        formdata = request.form.to_dict()
        blob_data = request.files['blob_file'].read()

        formatted_date_start = datetime.strptime(formdata['date_start'], '%a %b %d %Y %H:%M:%S GMT%z (%Z)')
        formatted_date_end = datetime.strptime(formdata['date_end'], '%a %b %d %Y %H:%M:%S GMT%z (%Z)')

        afl_instance.user_id = emp_id,
        afl_instance.leave_id = formdata['leave_id'],
        afl_instance.no_working_days_applied_for = formdata['no_working_days_applied_for'],
        afl_instance.date_range = formdata['date_from'],
        afl_instance.date_start = datetime.strftime(formatted_date_start, "%Y-%m-%d"),
        afl_instance.date_end = datetime.strftime(formatted_date_end, "%Y-%m-%d"),
        afl_instance.filing_date = formdata['date_of_filing'],
        afl_instance.blob_file = blob_data

        db.session.commit()

        return jsonify({'message': 'AFL instance updated successfully'})

 # ---------------------------------------------------------------------------- #



 # ---------------------------------------------------------------------------- #
 #                                    ADD AFL                                   #
 # ---------------------------------------------------------------------------- #
@afl.route('add-afl/<emp_id>', methods=['POST', 'GET'])
@login_required
def print_afl(emp_id):
    formdata = request.form.to_dict()
    if request.method == "POST":
        blob_data = request.files['blob_file'].read()

        formatted_date_start = datetime.strptime(formdata['date_start'], '%a %b %d %Y %H:%M:%S GMT%z (%Z)')
        formatted_date_end = datetime.strptime(formdata['date_end'], '%a %b %d %Y %H:%M:%S GMT%z (%Z)')
        afl = Afl(
                    user_id = emp_id,
                    leave_id = formdata['leave_id'],
                    no_working_days_applied_for = formdata['no_working_days_applied_for'],
                    date_range = formdata['date_from'],
                    date_start = datetime.strftime(formatted_date_start, "%Y-%m-%d"),
                    date_end = datetime.strftime(formatted_date_end, "%Y-%m-%d"),
                    filing_date = formdata['date_of_filing'],
                    blob_file = blob_data
                    )
        db.session.add(afl)
        db.session.flush()
        db.session.commit()
        
    #     formdata['user_id'] = emp_id

    #     for k,v in formdata.items():
    #         if type(v) is str:
    #             formdata.update({k: v.upper()})
    #         else:
    #             formdata.update({k: v})
    return jsonify('Success!')

 # ---------------------------------------------------------------------------- #
 #                                 DELETE AFL                                   #
 # ---------------------------------------------------------------------------- #
@afl.route('delete-afl', methods=['POST', 'GET'])
@login_required
def delete_afl_log():
	if request.method == "POST":
		formdata  = json.loads(request.data)
		
		afl = Afl.query.get(formdata['id'])

		db.session.delete(afl)
		db.session.commit()
	# return jsonify('{data:AFL Deleted Successfully}')
	return jsonify('AFL Deleted Successfully')


@afl.route('/download_blob/<id>')
def download_blob(id):
    # Query the database to retrieve the blob data by ID
    my_model = Afl.query.get(id)
    user = User.query.get(my_model.user_id)

    if my_model is None:
        return "Blob not found", 404

    # Get the blob data from the model
    blob_data = my_model.blob_file  # Replace 'blob_field' with your actual field name

    # Set the response headers for download
    response = Response(blob_data)

    content_type_pdf = 'application/pdf'
    content_type_word = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename=ALF_{user.last_name}.pdf'  # Set the filename

    return response
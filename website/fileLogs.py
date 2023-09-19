from .models import File_Logs
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app, session, Response
from . import db
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
import datetime
from .myhelper import allowed_file, my_random_string
from werkzeug.utils import secure_filename
import os, os.path

FileLogs = Blueprint('FileLogs', __name__)

admin_permission = Permission(RoleNeed('admin'))

@FileLogs.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))

@FileLogs.route('/download_blob/<id>')
def download_blob(id):
    # Query the database to retrieve the blob data by ID
    my_model = File_Logs.query.get(id)

    if my_model is None:
        return "Blob not found", 404

    # Get the blob data from the model
    blob_data = my_model.blob_file  # Replace 'blob_field' with your actual field name

    # Set the response headers for download
    response = Response(blob_data)

    content_type_pdf = 'application/pdf'
    content_type_word = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={my_model.file_name}.{my_model.file_type}'  # Set the filename

    return response



@FileLogs.route('/add-log/<emp_id>', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def add_log(emp_id):
# ---------------------------------------------------------------------------- #
#                              UPLOADING OF FILE                               #
# ---------------------------------------------------------------------------- #
    formdata = request.form.to_dict()

    try:
        # Get the BLOB data from the request
        blob_data = request.files['blob_file'].read()

        # Create a new FileLog object and set the BLOB data
        new_file_log = File_Logs(user_id=emp_id, file_name=formdata['fileName'], file_tag='AFL', file_type=formdata['fileTag'], blob_file=blob_data, file_path='N/A')

        # Add and commit the new FileLog object to the database
        db.session.add(new_file_log)
        db.session.commit()

        return jsonify({'message': 'File uploaded and saved to the database successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ---------------------------------------------------------------------------- #
#                              END OF FILE UPLOAD                              #
# ---------------------------------------------------------------------------- #

    return jsonify(''), 200


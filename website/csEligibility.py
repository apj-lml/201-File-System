from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Career_Service, Service_Record, User, Uploaded_File
from . import db
from datetime import datetime
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import os, os.path
import json

cse = Blueprint('cse', __name__)

ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@cse.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------------------------------------------------------------------- #
#                      Add eligibility from update profile                     #
# ---------------------------------------------------------------------------- #
@cse.route('add-eligibility', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def add_eligibility():
    if request.method == 'POST':
        formdata = request.form.to_dict()
        new_cse = Career_Service(**formdata)
        db.session.add(new_cse)
        db.session.commit()
        return redirect(request.referrer)

    return jsonify({})

# ---------------------------------------------------------------------------- #
#                          Add eligibility from signup                         #
# ---------------------------------------------------------------------------- #
@cse.route('add-eligibility-sign-up', methods=['POST', 'GET'])
def add_eligibility_sign_up():
    if request.method == 'POST':
        formdata = request.form.to_dict()
        cs_no_fields = formdata['cs_no_fields']
        for x  in range(1, int(cs_no_fields)+1):
            new_cs_eligibility = Career_Service(cs_eligibility = formdata['cs_eligibility['+str(x)+']'], cs_rating = formdata['cs_rating['+str(x)+']'],
                            date_of_examination = formdata['date_of_examination['+str(x)+']'], place_of_examination_conferment = formdata['place_of_examination_conferment['+str(x)+']'],
                            license_no = formdata['license_no['+str(x)+']'], date_of_validity = formdata['date_of_validity['+str(x)+']'], user_id = formdata.id)
            db.session.add(new_cs_eligibility)
            db.session.flush()
            db.session.commit()
    # ---------------------------------------------------------------------------- #
	#                            this is for file upload                           #
	# ---------------------------------------------------------------------------- #
            final_name = ''
            for afile in request.files:
                file = request.files[afile]

                print(f'print file: {afile}')
                if afile not in request.files:
                    print('No file selected part')
                    return redirect(request.url)

                if not file and allowed_file(file.filename):
                    print('Invalid file submitted')
                    return redirect(request.url)
                else:
                    file_extension = file.filename.rsplit('.', 1)[1].lower()
                    file_name = file.filename.rsplit('.', 1)[0]
                    final_name = secure_filename(afile+'_'+ formdata['last_name']+'_'+formdata['first_name'] + '_' + round(datetime.time() * 1000) +'_' + file_name +'.'+file_extension)
                    if os.path.isfile(current_app.config['UPLOAD_FOLDER']):
                        print('path does not exist... creating path')
                        os.mkdir(current_app.config['UPLOAD_FOLDER'])
                    else:
                        print('path exist!')
                        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], final_name))

                        #saving upload info to database
                        files_to_upload = Uploaded_File(file_name = final_name, file_path = '\\static\\files\\' + final_name, file_tag = afile, user_id = current_user.id)
                        db.session.add(files_to_upload)
                        db.session.commit()

    return jsonify({})

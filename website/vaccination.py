from .models import Token_Verifier, Uploaded_File, User
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app, session
import json
from . import db
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Vaccine
import datetime
from .myhelper import allowed_file, my_random_string
from werkzeug.utils import secure_filename
import os, os.path

vaccine = Blueprint('vaccine', __name__)

admin_permission = Permission(RoleNeed('admin'))

@vaccine.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))


@vaccine.route('add-vaccine/<user_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_vaccine(user_id):
    if request.method == 'POST':
        new_formdata = request.form.to_dict()

        # ---------------------------------------------------------------------------- #
        #                                CAPITALIZE DATA                               #
        # ---------------------------------------------------------------------------- #
        for k,v in new_formdata.items():
            if type(v) is str:
                new_formdata.update({k: v.upper()})
            else:
                new_formdata.update({k: v})

        print('VAX',new_formdata)
        if 'booster_id_no' in new_formdata and new_formdata['booster_id_no'] != "" and 'booster_brand' in new_formdata and new_formdata['booster_brand'] != "" and 'booster_date' in new_formdata and new_formdata['booster_date'] != "":

            new_vaccine = Vaccine(
                                    vac_id_no = new_formdata['vac_id_no'],
                                    vac_brand = new_formdata['vac_brand'],
                                    vac_place = new_formdata['vac_place'],
                                    vac_first_dose = new_formdata['vac_first_dose'],
                                    vac_second_dose = new_formdata['vac_second_dose'], 
                                    booster_id_no = new_formdata['booster_id_no'],
                                    booster_brand = new_formdata['booster_brand'], 
                                    booster_place = new_formdata['booster_place'],
                                    booster_date = datetime.datetime.strptime(new_formdata['booster_date'], '%Y-%m-%d').date(), 
                                    user_id = user_id
                            )
        else:
            new_vaccine = Vaccine(
                                    vac_id_no = new_formdata['vac_id_no'], 
                                    vac_brand = new_formdata['vac_brand'], 
                                    vac_place = new_formdata['vac_place'],
                                    vac_first_dose = new_formdata['vac_first_dose'], 
                                    vac_second_dose = new_formdata['vac_second_dose'], 
                                    booster_date = datetime.datetime.strptime('1900-01-01', '%Y-%m-%d').date(), 
                                    user_id = user_id
                            )

# ---------------------------------------------------------------------------- #
#                              UPLOADING OF FILE                               #
# ---------------------------------------------------------------------------- #

        user = User.query.get(user_id)

        final_name = ''
        for afile in request.files:
            files = request.files.getlist(afile)
            for file in files:

            #print(f'print file: {afile}')
                if file.filename == "":
                #if afile not in request.files:
                    print('No file selected')
                    #return redirect(request.url)
                else:
                    if not file and allowed_file(file.filename):
                        print('Invalid file submitted')
                        return jsonify('Invalid file submitted. Only PDF files are allowed'), 406
                    else:
                        today_is = datetime.datetime.today().strftime('%Y-%m-%d-%H%M%S')
                        file_extension = file.filename.rsplit('.', 1)[1].lower()
                        file_name = file.filename.rsplit('.', 1)[0]
                        final_name = secure_filename(afile+'_'+ current_user.last_name+'_' + '_' + file_name + f'_{my_random_string()}' +'.'+file_extension)
                        

                        if os.path.isfile(current_app.config['UPLOAD_FOLDER']):
                            print('path does not exist... creating path')
                            os.mkdir(current_app.config['UPLOAD_FOLDER'])
                        else:
                            print('path exist!')
                            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], final_name))

                            #saving upload info to database
                            files_to_upload = Uploaded_File(file_name = final_name, file_path = "\\static\\files\\", file_tag = afile, user_id = user_id)
                            db.session.add(files_to_upload)
                            db.session.commit()
# ---------------------------------------------------------------------------- #
#                              END OF FILE UPLOAD                              #
# ---------------------------------------------------------------------------- #


        db.session.add(new_vaccine)
        db.session.flush()
        db.session.commit()
    return jsonify({'id': new_vaccine.id})

@vaccine.route('update-vaccine/<user_id>', methods=['POST', 'GET'])
@login_required
def update_vaccine(user_id):
    formdata = request.form.to_dict()
   
    if 'vac_id' in formdata:
        if 'booster_id_no' in formdata and 'booster_brand' in formdata:
            if 'booster_id_no2' in formdata and 'booster_brand' in formdata:
                print (formdata)
                select_vaccine = Vaccine.query.filter_by(id = formdata['vac_id'])
                select_vaccine.update(dict(vac_id_no = formdata['vac_id_no'],
                                            vac_brand = formdata['vac_brand'], 
                                            vac_place = formdata['vac_place'],
                                            vac_first_dose = formdata['vac_first_dose'], 
                                            vac_second_dose = formdata['vac_second_dose'], 
                                            booster_id_no = formdata['booster_id_no'],
                                            booster_brand = formdata['booster_brand'], 
                                            booster_place = formdata['booster_place'],
                                            booster_date = datetime.datetime.strptime(formdata['booster_date'], '%Y-%m-%d').date(),

                                            booster_id_no2 = formdata['booster_id_no2'],
                                            booster_brand2 = formdata['booster_brand2'], 
                                            booster_place2 = formdata['booster_place2'],
                                            booster_date2 = datetime.datetime.strptime(formdata['booster_date2'], '%Y-%m-%d').date()
                                            ))
            else:
                print (formdata)
                select_vaccine = Vaccine.query.filter_by(id = formdata['vac_id'])
                select_vaccine.update(dict(vac_id_no = formdata['vac_id_no'],
                                            vac_brand = formdata['vac_brand'], 
                                            vac_place = formdata['vac_place'],
                                            vac_first_dose = formdata['vac_first_dose'], 
                                            vac_second_dose = formdata['vac_second_dose'], 
                                            booster_id_no = formdata['booster_id_no'],
                                            booster_brand = formdata['booster_brand'], 
                                            booster_place = formdata['booster_place'],
                                            booster_date = datetime.datetime.strptime(formdata['booster_date'], '%Y-%m-%d').date()
                                            ))
        else:
            select_vaccine = Vaccine.query.filter_by(id = formdata['vac_id'])
            select_vaccine.update(dict(vac_id_no = formdata['vac_id_no'],
                                        vac_brand = formdata['vac_brand'], 
                                        vac_place = formdata['vac_place'],
                                        vac_first_dose = formdata['vac_first_dose'], 
                                        vac_second_dose = formdata['vac_second_dose']
                                        ))


# ---------------------------------------------------------------------------- #
#                              UPLOADING OF FILE                               #
# ---------------------------------------------------------------------------- #

        user = User.query.get(user_id)
        final_name = ''
        
        for afile in request.files:
            files = request.files.getlist(afile)
            for file in files:

                #print(f'print file: {afile}')
                if file.filename == "":
                #if afile not in request.files:
                    print('No file selected')
                    #return redirect(request.url)
                else:
                    if not file and allowed_file(file.filename):
                        print('Invalid file submitted')
                        return jsonify('Invalid file submitted. Only PDF files are allowed'), 406
                    else:
                        today_is = datetime.datetime.today().strftime('%Y-%m-%d-%H%M%S')
                        file_extension = file.filename.rsplit('.', 1)[1].lower()
                        file_name = file.filename.rsplit('.', 1)[0]
                        final_name = secure_filename(afile+'_'+ current_user.last_name+'_' + '_' + file_name + f'_{my_random_string()}' +'.'+file_extension)
                        
                        # my_file = Path(current_app.config['UPLOAD_FOLDER']+'\\'+final_name)
                        # if my_file.is_file():
                        # 	print('file already exist')

                        if os.path.isfile(current_app.config['UPLOAD_FOLDER']):
                            print('path does not exist... creating path')
                            os.mkdir(current_app.config['UPLOAD_FOLDER'])
                        else:
                            print('path exist!')
                            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], final_name))

                            #saving upload info to database
                            files_to_upload = Uploaded_File(file_name = final_name, file_path = "\\static\\files\\", file_tag = afile, user_id = user_id)
                            db.session.add(files_to_upload)
                            db.session.commit()
# ---------------------------------------------------------------------------- #
#                              END OF FILE UPLOAD                              #
# ---------------------------------------------------------------------------- #

    db.session.commit()
    return jsonify('Successfully Updated!'), 200

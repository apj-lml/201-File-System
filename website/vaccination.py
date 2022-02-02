from .models import Token_Verifier
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app, session
import json
from . import db
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Vaccine
import datetime

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
            # print('else pumasok')
        db.session.add(new_vaccine)
        db.session.flush()
        db.session.commit()
    return jsonify({'id': new_vaccine.id})

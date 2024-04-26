from pprint import pprint
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app, session
from sqlalchemy import null
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user, login_required
import datetime
import time
from .models import Agency_Section, Agency_Unit, Career_Service, User, Vaccine, Vocational_Course
from . import db
import os, os.path
import json
from flask_principal import identity_changed, Identity, AnonymousIdentity

ALLOWED_EXTENSIONS = {'pdf'}

auth = Blueprint('auth', __name__)

@auth.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))

@auth.route('/', methods=['GET', 'POST'])
def login():
    logout_user()
    session.clear()
    if request.method == 'POST':
        # print("Received data:", request.data)  # Add this line to inspect the request data
        
        # try:
        formdata = json.loads(request.data)
        employee_id = formdata['email'].lstrip('0')
        password = formdata['password']

        user = User.query.filter_by(employee_id=employee_id).first()

        if user:
            if check_password_hash(user.password, password) and user.status_remarks != 'INACTIVE':
                session['user_id'] = user.id
                session['password'] = password
                # print('sessio var===========>>>', session['user_id'])
                return redirect(url_for('views.dataPrivacyAct'))
            else:
                return jsonify("incorrect_or_deactivated")
        else:
                return jsonify("incorrect_or_deactivated")

            
    return render_template('login.html', user=current_user)
    # return render_template('500.html', user=current_user)
    

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(), identity = AnonymousIdentity())

    return redirect(url_for('auth.login'))



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/check-token', methods=['GET', 'POST'])
def check_token():

    return render_template('check_token.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    #if 'token-verified' in session:
    if request.method == 'POST':
        #logout_user()
        #formdata = json.loads(request.data) <-- use this if receiving json request
        formdata = request.form.to_dict()
        #pprint(formdata)

        employee_id = formdata['employee_id']
        password1 = formdata['password']
        password2 = formdata['confirm_password']

        user = User.query.filter_by(employee_id=employee_id).first()

        if user:
            print('User already exists')
        elif password1 != password2:
            print('Password does not match')

        else:
            formdata['password'] = generate_password_hash(password1)
            formdata['birthdate'] = datetime.datetime.strptime(formdata['birthdate'], '%Y-%m-%d').date()

            new_formdata = formdata.copy()
            # cs_no_fields = new_formdata['cs_no_fields']
            # vocational_no_fields = new_formdata['vocational_no_fields']
            # ld_no_fields = new_formdata['ld_no_fields']
            # vac_no_fields = new_formdata['vac_no_fields']

# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#              popping unnecessary data before saving to database              #
# ---------------------------------------------------------------------------- #

            # formdata.pop('vac_id_no')
            # formdata.pop('vac_brand')
            # formdata.pop('vac_place')
            # formdata.pop('vac_first_dose')
            # formdata.pop('vac_second_dose')
            # formdata.pop('booster_date')
            
            # if 'booster_id_no' in formdata and formdata['booster_id_no'] is not None and 'booster_brand' in formdata and formdata['booster_brand'] is not None and 'booster_date' in formdata and formdata['booster_date'] is not None:
            # 	formdata.pop('booster_id_no')
            # 	formdata.pop('booster_brand')
            # 	formdata.pop('booster_place')
            # 	formdata.pop('booster_date')

            # for y in range(1, int(vocational_no_fields)+1):
            # 	formdata.pop('v_school['+str(y)+']')
            # 	formdata.pop('vocational_trade_course['+str(y)+']')
            # 	formdata.pop('v_period_of_attendance_from['+str(y)+']')
            # 	formdata.pop('v_period_of_attendance_to['+str(y)+']')
            # 	formdata.pop('v_highest_level['+str(y)+']')
            # 	formdata.pop('v_scholarship_academic_honor['+str(y)+']')
            
            # for x in range(1, int(cs_no_fields)+1):
            # 	formdata.pop('cs_eligibility['+str(x)+']')
            # 	formdata.pop('cs_rating['+str(x)+']')
            # 	formdata.pop('date_of_examination['+str(x)+']')
            # 	formdata.pop('place_of_examination_conferment['+str(x)+']')
            # 	formdata.pop('license_no['+str(x)+']')
            # 	formdata.pop('date_of_validity['+str(x)+']')
            
            formdata.pop('confirm_password')

# ---------------------------------------------------------------------------- #
#                    saving employee info to the databse                       #
# ---------------------------------------------------------------------------- #

            finaldata = User(**formdata)
            db.session.add(finaldata)
            db.session.flush()
            #session.refresh(f)
            db.session.commit()
# ---------------------------------------------------------------------------- #
#                              for cs eligibility                              #
# ---------------------------------------------------------------------------- #

            # for x in range(1, int(cs_no_fields)+1):

            # 	new_cs_eligibility = Career_Service(cs_eligibility = new_formdata['cs_eligibility['+str(x)+']'], cs_rating = new_formdata['cs_rating['+str(x)+']'],
            # 		date_of_examination = new_formdata['date_of_examination['+str(x)+']'], place_of_examination_conferment = new_formdata['place_of_examination_conferment['+str(x)+']'],
            # 		license_no = new_formdata['license_no['+str(x)+']'], date_of_validity = new_formdata['date_of_validity['+str(x)+']'], user_id = finaldata.id)
            # 	db.session.add(new_cs_eligibility)
            # 	db.session.flush()
            # 	db.session.commit()

# ---------------------------------------------------------------------------- #
#                            for vocational courses                            #
# ---------------------------------------------------------------------------- #

            # for y in range(1, int(vocational_no_fields)+1):

            # 	new_cs_eligibility = Vocational_Course(v_school = new_formdata['v_school['+str(y)+']'], vocational_trade_course = new_formdata['vocational_trade_course['+str(y)+']'],
            # 		v_period_of_attendance_from = new_formdata['v_period_of_attendance_from['+str(y)+']'], v_period_of_attendance_to = new_formdata['v_period_of_attendance_to['+str(y)+']'],
            # 		v_highest_level = new_formdata['v_highest_level['+str(y)+']'], v_scholarship_academic_honor = new_formdata['v_scholarship_academic_honor['+str(y)+']'], user_id = finaldata.id)
            # 	db.session.add(new_cs_eligibility)
            # 	db.session.flush()
            # 	db.session.commit()


            return jsonify(finaldata.id)
    else:
        my_agency_section = db.session.query(Agency_Section).order_by(Agency_Section.section_title.asc()).all()
        # my_agency_unit = db.session.query(Agency_Unit).all()

        agency_section = my_agency_section
        # agency_unit = my_agency_unit
        return render_template('signup.html', agency_section=agency_section)
        
    #return redirect(url_for('auth.login'))


@auth.route('/home')
def home():

    return 'HOME'
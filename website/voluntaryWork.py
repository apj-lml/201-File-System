from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Voluntary_Work
from . import db
from datetime import datetime
from .myhelper import allowed_file
from werkzeug.utils import secure_filename
import json

voluntaryWork = Blueprint('voluntaryWork', __name__)


admin_permission = Permission(RoleNeed('admin'))

@voluntaryWork.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))

# @workExperience.template_filter()
# def format_datetime(value, format='medium'):
#     if format == 'full':
#         format="EEEE, d. MMMM y 'at' HH:mm"
#     elif format == 'medium':
#         format="EE dd.MM.y HH:mm"
#     return babel.dates.format_datetime(value, format)



# ---------------------------------------------------------------------------- #
#                           ADD VW IN EMPLOYEE PROFILE                        #
# ---------------------------------------------------------------------------- #
@voluntaryWork.route('add-voluntary-work/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_voluntary_work(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        
        for k,v in formdata.items():
            if type(v) is str:
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})

        if 'sf_present' in formdata:
            formdata['date_to'] = 'PRESENT'
            formdata.pop('sf_present')

        formdata['user_id'] = emp_id
        formdata = {k:v.upper() for k,v in formdata.items()}
        # for key, value in formdata.items(): 
        #     setattr(formdata, key, value.upper())

        new_work_exp = Voluntary_Work(**formdata)

        db.session.add(new_work_exp)
        db.session.flush()
        db.session.commit()
            
    return jsonify("Successfully Added Voluntary Work!"), 200


 # ---------------------------------------------------------------------------- #
 #                                 DELETE VW                                   #
 # ---------------------------------------------------------------------------- #
@voluntaryWork.route('delete-voluntary-work', methods=['POST', 'GET'])
@login_required
def delete_voluntary_work():
    if request.method == "POST":
        formdata  = json.loads(request.data)
        we = Voluntary_Work.query.get(formdata['work_exp_id'])

        db.session.delete(we)
        db.session.commit()
    return jsonify('Work Experience Deleted Successfully')

 # ---------------------------------------------------------------------------- #
 #                                    GET VW                                   #
 # ---------------------------------------------------------------------------- #
@voluntaryWork.route('view-voluntary-work', methods=['POST', 'GET'])
@login_required
def view_voluntary_work():
    if request.method == "POST":
        formdata  = json.loads(request.data)
        get_we = Voluntary_Work.query.filter_by(id = formdata['work_exp_id']).all()
        column_keys = Voluntary_Work.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
    # Iterate through the returned output data set
        for row in get_we:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
            print(rows_dic)
        return jsonify(rows_dic)

 # ---------------------------------------------------------------------------- #
 #                                   Save VW                                   #
 # ---------------------------------------------------------------------------- #
@voluntaryWork.route('save-voluntary-work', methods=['POST', 'GET'])
@login_required
def update_voluntary_work():
    if request.method == "POST":
        formdata = request.form.to_dict()

        if 'sf_present' in formdata:
            formdata['date_to'] = 'PRESENT'
            formdata.pop('sf_present')


        get_we = Voluntary_Work.query.get(formdata['id'])
        formdata.pop('id')

        #code for automated update
        print(formdata)
        for key, value in formdata.items(): 
            setattr(get_we, key, value.upper())
        db.session.commit()

        return jsonify('Successfully Saved Changes.')

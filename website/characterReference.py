from itertools import count
from pprint import pprint
from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Assignatory, Character_Reference
from . import db
from datetime import datetime
import json

characterReference = Blueprint('characterReference', __name__)


admin_permission = Permission(RoleNeed('admin'))

@characterReference.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------- #
#                                    ADD CHAR REF                              #
# ---------------------------------------------------------------------------- #
@characterReference.route('add/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_character_reference(emp_id):
    if request.method == "POST":

        formdata = request.form.to_dict()
        # for k,v in formdata.items():
        #     formdata.update({k: v.upper()})
        pprint(formdata)
        count_char_ref = Character_Reference.query.filter_by(user_id = emp_id).count()
        if count_char_ref < 3 :
            for xy in range(1, 4):
                formdata['user_id'] = emp_id
                # char_ref = Character_Reference(**formdata)
                char_ref = Character_Reference(
                    fullname = formdata['fullname['+ str(xy) +']'].upper(),
                    address = formdata['address['+ str(xy) +']'].upper(),
                    contact_no = formdata['contact_no['+ str(xy) +']'],
                    user_id = emp_id
                    )
                db.session.add(char_ref)
            db.session.flush()
            db.session.commit()
                
            return jsonify("Successfully Added Character Reference!"), 200
        else:
            return jsonify("You can only add up to three (3) Character References!")


 # ---------------------------------------------------------------------------- #
 #                                 DELETE WES                                   #
 # ---------------------------------------------------------------------------- #
@characterReference.route('delete', methods=['POST', 'GET'])
@login_required
def delete_character_reference():
    if request.method == "POST":
        formdata  = json.loads(request.data)
        cr = Character_Reference.query.get(formdata['id'])

        db.session.delete(cr)
        db.session.commit()
    return jsonify('Character Reference Deleted Successfully')

 # ---------------------------------------------------------------------------- #
 #                                    GET WES                                   #
 # ---------------------------------------------------------------------------- #
@characterReference.route('get/<emp_id>', methods=['POST', 'GET'])
@login_required
def view_character_reference(emp_id):
    if request.method == "GET":
    # formdata  = json.loads(request.data)
        get_cr = Character_Reference.query.filter_by(user_id = emp_id).all()
        column_keys = Character_Reference.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
    # Iterate through the returned output data set
        for row in get_cr:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
            # print(rows_dic)
        return jsonify(rows_dic)
    if request.method == "POST":
        formdata  = json.loads(request.data)
        get_cr = Character_Reference.query.filter_by(id = formdata['id']).all()
        column_keys = Character_Reference.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
    # Iterate through the returned output data set
        for row in get_cr:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
            # print(rows_dic)
        return jsonify(rows_dic)

 # ---------------------------------------------------------------------------- #
 #                                   Save WES                                   #
 # ---------------------------------------------------------------------------- #
@characterReference.route('save', methods=['POST', 'GET'])
@login_required
def update_work_experience():
    if request.method == "POST":
        formdata = request.form.to_dict()
        
        # formdata.pop('id')

        for xy in range(1, 4):
            get_we = Character_Reference.query.filter_by(id = formdata['id['+str(xy)+']'])
            get_we.update(dict(
                fullname = formdata['fullname['+ str(xy) +']'].upper(),
                address = formdata['address['+ str(xy) +']'].upper(),
                contact_no = formdata['contact_no['+ str(xy) +']'],
            ))

        # # print(formdata)
        # for key, value in formdata.items(): 
        #     setattr(get_we, key, value.upper())


        db.session.commit()

        return jsonify('Successfully Saved Changes.')

# ---------------------------------------------------------------------------- #
#                              UPDATE ASSIGNATORY                              #
# ---------------------------------------------------------------------------- #
@characterReference.route('assignatory/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def update_assignatory(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        get_assig = Assignatory.query.filter_by(user_id = emp_id)
        get_assig.update(dict(
                assignatory = formdata['assignatory'].upper(),
                position_title = formdata['position_title'],
                ))
        db.session.commit()
    return redirect(request.referrer)


# ---------------------------------------------------------------------------- #
#                                ADD ASSIGNATORY                               #
# ---------------------------------------------------------------------------- #
@characterReference.route('add-assignatory/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_assignatory(emp_id):
    if request.method == "POST":
        #formdata = request.form.to_dict()

        new_assignatory = Assignatory(assignatory = 'ENGR. JOHN N. MOLANO, MSME', user_id = emp_id)
        db.session.add(new_assignatory)
        db.session.commit()

    return redirect(request.referrer)


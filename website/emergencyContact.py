from itertools import count
from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Emergency_Contact
from . import db
from datetime import datetime
import json

emergencyContact = Blueprint('emergencyContact', __name__)


admin_permission = Permission(RoleNeed('admin'))

@emergencyContact.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------- #
#                                ADD CHAR REF                                  #
# ---------------------------------------------------------------------------- #
@emergencyContact.route('add/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_emergency_contact(emp_id):
    if request.method == "POST":

        formdata = request.form.to_dict()
        for k,v in formdata.items():
            formdata.update({k: v.upper()})

        count_char_ref = Emergency_Contact.query.filter_by(user_id = emp_id).count()
        
        if count_char_ref < 1 :
            formdata['user_id'] = emp_id
            char_ref = Emergency_Contact(
                fullname = formdata['fullname[1]'].upper(),
                relationship = formdata['relationship[1]'].upper(),
                address = formdata['address[1]'].upper(),
                contact_no = formdata['contact_no[1]'],
                user_id = emp_id
            )

            db.session.add(char_ref)
            db.session.flush()
            db.session.commit()
            
            return jsonify("Successfully Added Emergency Contact!"), 200
        else:
            return jsonify("You can only add up to one Emergency Contact only!"), 200


 # ---------------------------------------------------------------------------- #
 #                                 DELETE WES                                   #
 # ---------------------------------------------------------------------------- #
@emergencyContact.route('delete', methods=['POST', 'GET'])
@login_required
def delete_emergency_contact():
    if request.method == "POST":
        formdata  = json.loads(request.data)
        cr = Emergency_Contact.query.get(formdata['id'])

        db.session.delete(cr)
        db.session.commit()
    return jsonify('Emergency Contact Deleted Successfully')

 # ---------------------------------------------------------------------------- #
 #                                    GET WES                                   #
 # ---------------------------------------------------------------------------- #
@emergencyContact.route('get/<emp_id>', methods=['POST', 'GET'])
@login_required
def view_emergency_contact(emp_id):
    if request.method == "GET":
    # formdata  = json.loads(request.data)
        get_cr = Emergency_Contact.query.filter_by(user_id = emp_id).all()
        column_keys = Emergency_Contact.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
    # Iterate through the returned output data set
        for row in get_cr:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
            print(rows_dic)
        return jsonify(rows_dic)

 # ---------------------------------------------------------------------------- #
 #                                   Save WES                                   #
 # ---------------------------------------------------------------------------- #
@emergencyContact.route('update/<id>', methods=['POST', 'GET'])
@login_required
def udpate_emergency_contact(id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        print("ANDITO AKO")
        # get_we = Emergency_Contact.query.get(formdata['id'])

        # for xy in range(1, 4):
        get_we = Emergency_Contact.query.filter_by(id = formdata['id[1]'])
        get_we.update(dict(
            fullname = formdata['fullname[1]'].upper(),
            relationship = formdata['relationship[1]'].upper(),
            address = formdata['address[1]'].upper(),
            contact_no = formdata['contact_no[1]'],
        ))
        # formdata.pop('id')

        # for key, value in formdata.items(): 
        #     setattr(get_we, key, value.upper())
        db.session.commit()

    return jsonify('Successfully Saved Changes.')


@emergencyContact.route('edit/<id>', methods=['POST', 'GET'])
@login_required
def edit_emergency_contact(id):
    if request.method == "GET":
    # formdata  = json.loads(request.data)
        get_cr = Emergency_Contact.query.filter_by(id = id).all()
        column_keys = Emergency_Contact.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
    # Iterate through the returned output data set
        for row in get_cr:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
        return jsonify(rows_dic)

from pprint import pprint
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from sqlalchemy import desc
from .models import Work_Experience
from . import db
from datetime import datetime
from .myhelper import format_mydatetime
import json

workExperience = Blueprint('workExperience', __name__)


admin_permission = Permission(RoleNeed('admin'))

@workExperience.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------- #
#                           ADD WES IN EMPLOYEE PROFILE                        #
# ---------------------------------------------------------------------------- #
@workExperience.route('add-work-experience/<emp_id>', methods=['POST', 'GET'])
@login_required
# @admin_permission.require(http_exception=403)
def add_work_experience(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        formdata['user_id'] = emp_id
        
        for k,v in formdata.items():
            if type(v) is str:
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})

        if 'sg' not in formdata:
            formdata['sg'] = 'N/A'
        
        if 'step' not in formdata:
            formdata['step'] = 'N/A'

        if 'sf_present' in formdata:
            get_we = Work_Experience.query.filter_by(user_id = emp_id, date_to = "PRESENT").all()
            if get_we:
                return jsonify('You Can\'t Enter Overlapping Dates!'), 406
            else:
                formdata['date_to'] = 'PRESENT'
                formdata.pop('sf_present')
        else:
            get_we = Work_Experience.query.filter_by(user_id = emp_id).order_by(desc(Work_Experience.date_from)).all()
            for we in get_we:
                pprint(we.date_from)
                
                we_date_from = format_mydatetime(we.date_from)
                date_from = format_mydatetime(formdata['date_from'])
                date_to = format_mydatetime(formdata['date_to'])
                if we.date_to == "PRESENT":
                    we_date_to = datetime.utcnow()
                else:
                    we_date_to = format_mydatetime(we.date_to)

                if we_date_from <= date_from <= we_date_to or we_date_from <= date_to <= we_date_to:    
                    return jsonify('You Can\'t Enter Overlapping Dates!'), 406


        if 'nia_pimo' in formdata:
            formdata['department_agency_office_company'] = 'NATIONAL IRRIGATION ADMINISTRATION - PANGASINAN IRRIGATION MANAGEMENT OFFICE'
            formdata.pop('nia_pimo')
    
        new_work_exp = Work_Experience(**formdata)

        db.session.add(new_work_exp)
        db.session.flush()
        db.session.commit()
            
    return jsonify("Successfully Added Work Experience!"), 200


 # ---------------------------------------------------------------------------- #
 #                                 DELETE WES                                   #
 # ---------------------------------------------------------------------------- #
@workExperience.route('delete-work-experience', methods=['POST', 'GET'])
@login_required
def delete_work_experience():
    if request.method == "POST":
        formdata  = json.loads(request.data)
        we = Work_Experience.query.get(formdata['work_exp_id'])

        db.session.delete(we)
        db.session.commit()
    return jsonify('Work Experience Deleted Successfully')

 # ---------------------------------------------------------------------------- #
 #                                    GET WES                                   #
 # ---------------------------------------------------------------------------- #
@workExperience.route('view-work-experience', methods=['POST', 'GET'])
@login_required
def view_work_experience():
    if request.method == "POST":
        formdata  = json.loads(request.data)
        get_we = Work_Experience.query.filter_by(id = formdata['work_exp_id']).all()
        column_keys = Work_Experience.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
    # Iterate through the returned output data set
        for row in get_we:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp= {}
            # print(rows_dic)
        return jsonify(rows_dic)

 # ---------------------------------------------------------------------------- #
 #                                   Save WES                                   #
 # ---------------------------------------------------------------------------- #
@workExperience.route('save-work-experience/<emp_id>', methods=['POST', 'GET'])
@login_required
def update_work_experience(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        for k,v in formdata.items():
            if type(v) is str:
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})
        # pprint(formdata)
        # get_we = Work_Experience.query.get(formdata['id'])

        if 'sf_present' in formdata:
            # if get_we.date_to == "PRESENT":
            #     return jsonify('You Can\'t Enter Overlapping Dates! 111'), 406
            # else:
            formdata['date_to'] = 'PRESENT'
            formdata.pop('sf_present')
            
        
        if 'sg' not in formdata:
            formdata['sg'] = 'N/A'
        
        if 'step' not in formdata:
            formdata['step'] = '1'
            
        get_we_all = Work_Experience.query.filter_by(user_id = emp_id).order_by(desc(Work_Experience.date_from)).all()
        get_we = Work_Experience.query.get(formdata['id'])
        for we in get_we_all:
            if we.id != int(formdata['id']):
                if formdata['date_to'] == "PRESENT":
                    we_date_to = datetime.utcnow()
                    date_to = datetime.utcnow()

                else:
                    we_date_to = format_mydatetime(we.date_to)
                    date_to = format_mydatetime(formdata['date_to'])


                we_date_from = format_mydatetime(we.date_from)
                date_from = format_mydatetime(formdata['date_from'])
                
                if we.date_to == "PRESENT":
                    we_date_to = datetime.utcnow()
                else:
                    we_date_to = format_mydatetime(we.date_to)
                

                if we_date_from <= date_from <= we_date_to or we_date_from <= date_to <= we_date_to:
                    return jsonify('You Can\'t Enter Overlapping Dates!'), 406
            # else:
            if 'nia_pimo' in formdata:
                formdata['department_agency_office_company'] = 'NATIONAL IRRIGATION ADMINISTRATION - PANGASINAN IRRIGATION MANAGEMENT OFFICE'
                formdata.pop('nia_pimo')

        formdata.pop('id')

        for key, value in formdata.items(): 
            setattr(get_we, key, value)
        db.session.commit()

        return jsonify('Successfully Saved Changes.'), 200

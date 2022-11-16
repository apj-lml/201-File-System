from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import WesDutiesAccomplishmentsSchema, Work_Experience
from .models import Wes_Duties_Accomplishments
import json
from . import db

wes = Blueprint('wes', __name__)

admin_permission = Permission(RoleNeed('admin'))

@wes.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))

 # ---------------------------------------------------------------------------- #
 #                                    ADD WES                                   #
 # ---------------------------------------------------------------------------- #
@wes.route('add-accomp', methods=['POST', 'GET'])
@login_required
def add_accomp():
    if request.method == "POST":
        formdata = request.form.to_dict()

        # print(formdata)
        new_accomp = Wes_Duties_Accomplishments(**formdata)

        db.session.add(new_accomp)
        db.session.commit()
        db.session.flush()

        # db.session.refresh(new_accomp)

        formdata["id"] = new_accomp.id
        print(formdata)
        return jsonify(**formdata)

 # ---------------------------------------------------------------------------- #
 #                                   edit WES                                   #
 # ---------------------------------------------------------------------------- #
@wes.route('edit-accomp/<accomp_id>', methods=['POST', 'GET'])
@login_required
def edit_accomp(accomp_id):
    if request.method == "POST":
        # formdata = request.form.to_dict()

        wda_schema = WesDutiesAccomplishmentsSchema()
        new_accomp = db.session.query(Wes_Duties_Accomplishments).get(accomp_id)

        # print("HERE: ", json.loads(jsonify(wda_schema.dump(new_accomp)).get_data(True)))

        return json.loads(jsonify(wda_schema.dump(new_accomp)).get_data(True))

        # return jsonify(**new_accomp)

 # ---------------------------------------------------------------------------- #
 #                                 UPDATE WES                                   #
 # ---------------------------------------------------------------------------- #
@wes.route('update-accomp', methods=['POST', 'GET'])
@login_required
def update_accomp():
    if request.method == "POST":
        formdata = request.form.to_dict()

        # print(formdata)
        get_we = Wes_Duties_Accomplishments.query.get(formdata['id'])

        formdata.pop('id')

        for key, value in formdata.items(): 
            setattr(get_we, key, value)
        db.session.commit()

        
        return jsonify(**formdata)


 # ---------------------------------------------------------------------------- #
 #                              REMOVE ACCOMP                                   #
 # ---------------------------------------------------------------------------- #
@wes.route('delete-accomp', methods=['POST', 'GET'])
@login_required
def delete_accomp():
    if request.method == "POST":
        formdata  = json.loads(request.data)
		
        delete_child = Wes_Duties_Accomplishments.query.get(formdata['accomp_id'])

        db.session.delete(delete_child)
        db.session.commit()
        return jsonify({})

 

from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import User, Other_Questions
from . import db
#from datetime import datetime


ALLOWED_EXTENSIONS = {'pdf'}

otherQuestions = Blueprint('otherQuestions', __name__)

admin_permission = Permission(RoleNeed('admin'))

@otherQuestions.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

@otherQuestions.route('add-answers/<emp_id>', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def add_answers(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        print(formdata)
        for xy in range(1, 3 + 1):
            finaldata = Other_Questions(question = formdata['q'+str(xy)], answer = formdata['answer'+str(xy)], user_id = emp_id)
            db.session.add(finaldata)
            db.session.commit()
        return jsonify('Successfully Updated Answers')

    return 'ok', 200

@otherQuestions.route('update-answers/<emp_id>', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def update_answers(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        #print(formdata)
        for xy in range(1, 3 + 1):
            select_q = Other_Questions.query.get(formdata['id'+str(xy)])
            select_q.answer = formdata['answer'+str(xy)]
            db.session.commit()
        return jsonify('Successfully Updated Answers')

    return 'ok', 200
    
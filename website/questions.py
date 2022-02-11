
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify, current_app
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import User, Questions
from . import db
#from datetime import datetime


ALLOWED_EXTENSIONS = {'pdf'}

questions = Blueprint('questions', __name__)

admin_permission = Permission(RoleNeed('admin'))

@questions.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

@questions.route('add-answers/<emp_id>', methods=['POST', 'GET'])
@login_required
#@admin_permission.require(http_exception=403)
def add_answers(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()
        print(formdata)
        for xy in range(1, 13 + 1):
            finaldata = Questions(answer = formdata['answer['+str(xy)+']'], user_id = emp_id)
            db.session.add(finaldata)
            db.session.commit()
        return jsonify('Successfully Added Answers')

    return 'ok', 200
    
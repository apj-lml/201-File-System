from .myhelper import my_random_string
from .models import Token_Verifier
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app, session
import json
from . import db
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed

tokenizer = Blueprint('tokenizer', __name__)

admin_permission = Permission(RoleNeed('admin'))

@tokenizer.errorhandler(403)
def page_not_found(e):
	session['redirected_from'] = request.url
	return redirect(url_for('auth.login'))

@tokenizer.route('add-token', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def add_token():
	if request.method == 'POST' :
		new_token = Token_Verifier(token = my_random_string(7))
		db.session.add(new_token)
		db.session.commit()
	return jsonify({})

@tokenizer.route('get-token/<id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_token(id):
	if request.method == 'GET' and id == '0':
		tokens = db.session.query(Token_Verifier).all()
	else:
		tokens = Token_Verifier.query.filter_by(id = id)

	column_keys = Token_Verifier.__table__.columns.keys()
	# Temporary dictionary to keep the return value from table
	rows_dic_temp = {}
	rows_dic = []
	# Iterate through the returned output data set
	for row in tokens:
		for col in column_keys:
			rows_dic_temp[col] = getattr(row, col)
		rows_dic.append(rows_dic_temp)
		rows_dic_temp= {}

	return jsonify(rows_dic)

@tokenizer.route('validate-token', methods=['POST', 'GET'])
def validate_token():
	formdata = json.loads(request.data)
	mytoken = formdata['mytoken']

	if request.method == 'POST':
		got_token = db.session.query(Token_Verifier).filter_by(token = mytoken).first()
		if got_token:
			#print(got_token.status)
			session['token-verified'] = True
			return redirect(url_for('auth.signup'))
		else:
			session['error_msg'] = 'token-error'
	return jsonify(session['error_msg'])
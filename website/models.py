# from email.policy import default
#from email.policy import default
from time import timezone
from tkinter.tix import Tree
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime, date
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
	employee_id = db.Column(db.Integer, unique=True, nullable=False)
	email = db.Column(db.String(150), unique=False, nullable=True)
	password = db.Column(db.String(150), nullable=False)
	last_name = db.Column(db.String(150))
	first_name = db.Column(db.String(150))
	middle_name = db.Column(db.String(150))
	name_extn = db.Column(db.String(150))
	#position_id = db.relationship("Position", back_populates="user", uselist = False)
	employment_status = db.Column(db.String(150))
	position_title = db.Column(db.String(150))
	salary_grade = db.Column(db.String(150))
	step = db.Column(db.String(150))

	item_no = db.Column(db.String(150))
	date_of_assumption = db.Column(db.String(150))
	original_station = db.Column(db.String(150))
	date_hired_in_nia = db.Column(db.String(150), nullable=True)
	date_of_last_step_increment = db.Column(db.String(150), nullable=True)
	date_of_original_appointment = db.Column(db.String(150), nullable=True)
	daily_rate = db.Column(db.String(150), nullable=True)
	monthly_rate = db.Column(db.String(150), nullable=True)
	# daily_rate = db.Column(db.Float(10, 2))
	# monthly_rate = db.Column(db.Float(10, 2))

	section = db.Column(db.String(150))
	unit = db.Column(db.String(150))
	birthdate = db.Column(db.Date())
	age = db.Column(db.String(150))
	place_of_birth = db.Column(db.String(150))
	sex = db.Column(db.String(150))
	civil_status = db.Column(db.String(150))
	height = db.Column(db.String(150))
	weight = db.Column(db.String(150))
	blood_type = db.Column(db.String(150))
	religion = db.Column(db.String(150))
	dependents = db.Column(db.String(150))
	mobile_no = db.Column(db.String(150))
	telephone_no = db.Column(db.String(150))
	gsis = db.Column(db.String(150))
	pagibig = db.Column(db.String(150))
	philhealth = db.Column(db.String(150))
	sss = db.Column(db.String(150))
	tin = db.Column(db.String(150))
	atm = db.Column(db.String(150))
	umid = db.Column(db.String(150))
	philsys = db.Column(db.String(150))
	citizenship = db.Column(db.String(150))
	dual_citizenship = db.Column(db.String(150))
	indicate_country = db.Column(db.String(150))
	p_house_block_lot = db.Column(db.String(150))
	p_street = db.Column(db.String(150))
	p_subdivision_village = db.Column(db.String(150))
	p_barangay = db.Column(db.String(150))
	p_city_municipality = db.Column(db.String(150))
	p_province = db.Column(db.String(150))
	p_zip_code = db.Column(db.String(150))
	pres_house_block_lot = db.Column(db.String(150))
	pres_street = db.Column(db.String(150))
	pres_subdivision_village = db.Column(db.String(150))
	pres_barangay = db.Column(db.String(150))
	pres_city_municipality = db.Column(db.String(150))
	pres_province = db.Column(db.String(150))
	pres_zip_code = db.Column(db.String(150))
	# highest_educational_attainment = db.Column(db.String(150))

	elementary_school = db.Column(db.String(150))
	e_period_of_attendance_from = db.Column(db.String(150))
	e_period_of_attendance_to = db.Column(db.String(150))
	e_highest_level = db.Column(db.String(150))
	e_highest_grade_year_units = db.Column(db.String(150))
	e_scholarship_academic_honor = db.Column(db.String(150))

	high_school = db.Column(db.String(150))
	hs_period_of_attendance_from = db.Column(db.String(150))
	hs_period_of_attendance_to = db.Column(db.String(150))
	hs_highest_level = db.Column(db.String(150))
	hs_highest_grade_year_units = db.Column(db.String(150))
	hs_scholarship_academic_honor = db.Column(db.String(150))

	type_of_user = db.Column(db.String(150), default='user')
	
	uploaded_files = db.relationship('Uploaded_File')
	service_record = db.relationship('Service_Record')
	career_service = db.relationship('Career_Service')
	vocational_course = db.relationship('Vocational_Course')
	learning_development = db.relationship('Learning_Development')
	vaccine = db.relationship('Vaccine')
	familyBg = db.relationship('Family_Background')
	college = db.relationship('College')
	shirt = db.relationship('Shirt')
	masteral = db.relationship('Masteral')
	doctoral = db.relationship('Doctoral')




	# emergency_contact = db.relationship('Emergency_Contact')

class Vocational_Course(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	v_school = db.Column(db.String(150))
	vocational_trade_course = db.Column(db.String(150))
	v_period_of_attendance_from = db.Column(db.String(150))
	v_period_of_attendance_to = db.Column(db.String(150))
	v_highest_level = db.Column(db.String(150))
	v_highest_grade_year_units = db.Column(db.String(150))
	v_scholarship_academic_honor = db.Column(db.String(150))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Career_Service(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cs_eligibility = db.Column(db.String(150))
	cs_rating = db.Column(db.String(150))
	date_of_examination = db.Column(db.String(150))
	place_of_examination_conferment = db.Column(db.String(150))
	license_no = db.Column(db.String(150))
	date_of_validity = db.Column(db.String(150))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Uploaded_File(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	file_name = db.Column(db.String(150))
	file_path = db.Column(db.String(150))
	file_tag = db.Column(db.String(150))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Token_Verifier(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	token = db.Column(db.String(50))
	status = db.Column(db.String(50), default = "active")
	timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

class Service_Record(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	service_from = db.Column(db.String(50))
	service_to = db.Column(db.String(50))
	designation = db.Column(db.String(150))
	status = db.Column(db.String(50))
	salary = db.Column(db.String(50))
	station_place = db.Column(db.String(50))
	leave_wo_pay = db.Column(db.String(50))
	separation_date = db.Column(db.String(50), nullable=True)
	separation_cause = db.Column(db.String(50), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Learning_Development(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	ld_program = db.Column(db.String(50))
	ld_date_from = db.Column(db.String(50))
	ld_date_to = db.Column(db.String(50))
	ld_no_hours = db.Column(db.String(50))
	ld_type = db.Column(db.String(50))
	ld_sponsored_by = db.Column(db.String(50))
	ld_attachment = db.Column(db.String(150))
	ld_attachment_file_name = db.Column(db.String(100))

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Vaccine(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)

	vac_id_no = db.Column(db.String(50))
	vac_brand = db.Column(db.String(50))
	vac_place = db.Column(db.String(50))
	vac_first_dose = db.Column(db.String(50))
	vac_second_dose = db.Column(db.String(50))

	booster_id_no = db.Column(db.String(50))
	booster_brand = db.Column(db.String(50))
	booster_place = db.Column(db.String(50))
	booster_date = db.Column(db.Date())

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Family_Background(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	fb_last_name = db.Column(db.String(50))
	fb_first_name = db.Column(db.String(50))
	fb_middle_name = db.Column(db.String(50))
	fb_name_ext = db.Column(db.String(50))
	fb_occupation = db.Column(db.String(50))
	fb_employer_business_name = db.Column(db.String(50))
	fb_business_address = db.Column(db.String(50))
	fb_contact_no = db.Column(db.String(50))
	fb_date_of_birth = db.Column(db.String(50))
	fb_maiden_name = db.Column(db.String(50))
	fb_relationship = db.Column(db.String(50))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class College(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	c_school = db.Column(db.String(150))
	c_degree_course = db.Column(db.String(150))
	c_period_of_attendance_from = db.Column(db.String(150))
	c_period_of_attendance_to = db.Column(db.String(150))
	c_highest_level_units_earned = db.Column(db.String(150))
	c_highest_grade_year_units = db.Column(db.String(150))
	c_scholarship_academic_honor = db.Column(db.String(150))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Masteral(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	gs_school = db.Column(db.String(150))
	gs_degree_course = db.Column(db.String(150))
	gs_period_of_attendance_from = db.Column(db.String(150))
	gs_period_of_attendance_to = db.Column(db.String(150))
	gs_highest_level_units_earned = db.Column(db.String(150))
	gs_highest_grade_year_units = db.Column(db.String(150))
	gs_scholarship_academic_honor = db.Column(db.String(150))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Doctoral(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	doc_school = db.Column(db.String(150))
	doc_degree_course = db.Column(db.String(150))
	doc_period_of_attendance_from = db.Column(db.String(150))
	doc_period_of_attendance_to = db.Column(db.String(150))
	doc_highest_level_units_earned = db.Column(db.String(150))
	doc_highest_grade_year_units = db.Column(db.String(150))
	doc_scholarship_academic_honor = db.Column(db.String(150))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Others(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	polo_shirt_size = db.Column(db.String(50))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
class Shirt(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	polo_shirt_size = db.Column(db.String(50))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
# class Graduate_Study(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	graduate_studies = db.Column(db.String(150))
# 	school = db.Column(db.String(150))
# 	degree_course = db.Column(db.String(150))
# 	period_of_attendance_to = db.Column(db.String(150))
# 	highest_level_units_earned = db.Column(db.String(150))
# 	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# class Position(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	position_title = db.Column(db.String(150))
# 	user_id = db.relationship('User', back_populates="position")

# class Emergency_Contact(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(150))
# 	relations = db.Column(db.String(150))
# 	complete_address = db.Column(db.String(150))
# 	contact_no = db.Column(db.String(150))
# 	user_id = db.relationship('user.id')
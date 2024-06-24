
from time import timezone

from sqlalchemy import asc, desc

from . import db, ma
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import column_property
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, date, timedelta
from sqlalchemy_serializer import SerializerMixin

import time, pytz
import os
import math

from dataclasses import dataclass

from sqlalchemy.inspection import inspect
from dateutil.relativedelta import relativedelta

UTC = pytz.utc
PST = pytz.timezone('Asia/Manila')


# ---------------------------------------------------------------------------- #
#                                     test                                     #
# ---------------------------------------------------------------------------- #
class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]
# --------------------------------- end test --------------------------------- #


@dataclass
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())
    status_remarks = db.Column(db.String(50))
    is_validated = db.Column(db.String(50), default="VALIDATED")
    desc_remarks = db.Column(db.String(999))
    comments_remarks = db.Column(db.String(999))
    employee_id = db.Column(db.Integer, unique=True, nullable=False)
    employee_id_date_issued = db.Column(db.Date())
    email = db.Column(db.String(150), unique=False, nullable=True)
    password = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    middle_name = db.Column(db.String(150))
    middle_initial = db.Column(db.String(150))
    name_extn = db.Column(db.String(150))
    maiden_name = db.Column(db.String(150))
    #position_id = db.relationship("Position", back_populates="user", uselist = False)
    employment_status = db.Column(db.String(150))
    position_title = db.Column(db.String(150))
    job_grade = db.Column(db.String(150))
    salary_grade = db.Column(db.String(150))
    step = db.Column(db.String(150))

    item_no = db.Column(db.String(150))
    item_location = db.Column(db.String(150))
    date_of_assumption = db.Column(db.String(150))

    # original_station = db.Column(db.String(150))
    date_hired_in_nia = db.Column(db.String(150), nullable=True)
    date_hired_in_nia_pimo = db.Column(db.String(150), nullable=True)
    no_of_years_in_nia = db.Column(db.String(150), nullable=True)
    first_day_in_service = db.Column(db.Date(), nullable=True)

    date_of_last_step_increment = db.Column(db.String(150), nullable=True)
    date_of_original_appointment = db.Column(db.String(150), nullable=True)
    date_of_last_promotion = db.Column(db.String(150), nullable=True)

    daily_rate = db.Column(db.String(150), nullable=True)
    monthly_rate = db.Column(db.String(150), nullable=True)
    # daily_rate = db.Column(db.Float(10, 2))
    # monthly_rate = db.Column(db.Float(10, 2))

    #section = db.Column(db.String(150))
    section = db.Column(db.Integer, db.ForeignKey('agency__section.id'))
    # section_rel = db.relationship("Agency_Section", backref="agency_section")

    unit = db.Column(db.Integer, db.ForeignKey('agency__unit.id'))
    #user_unit_rel = db.relationship("Agency_Unit")

    # uploaded_files = db.relationship('Uploaded_File')

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

    solo_parent = db.Column(db.String(150))
    voters_id_no = db.Column(db.String(150))
    pwd = db.Column(db.String(150))

    driver_license = db.Column(db.String(150))
    driver_license_validity = db.Column(db.String(150))
    security_guard = db.Column(db.String(150))
    security_guard_validity = db.Column(db.String(150))
    passport_no = db.Column(db.String(150))
    passport_validity = db.Column(db.String(150))

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

    same_as_permanent_address = db.Column(db.String(150))

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

    is_section_chief = db.Column(db.Integer, default=0)
    is_unit_head = db.Column(db.Integer, default=0)
    is_division_manager = db.Column(db.Integer, default=0)

    is_primary_afl_certifier = db.Column(db.Integer, default=0)
    is_secondary_afl_certifier = db.Column(db.Integer, default=0)

    is_primary_sr_certifier = db.Column(db.Integer, default=0)
    is_secondary_sr_certifier = db.Column(db.Integer, default=0)

    service_record_remarks = db.Column(db.String(999), default='')

    type_of_user = db.Column(db.String(150), default='user')
    #last_updated = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=datetime.now(PST))
    last_updated = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    data_privacy = db.Column(db.String(45), default='unchecked')
    is_spouse_saln_filer = db.Column(db.String(45), default='unchecked')
    acknowledgement = db.Column(db.String(45), default='unchecked')
    
    uploaded_files = db.relationship('Uploaded_File')
    # service_record = db.relationship('Service_Record')
    service_record = db.relationship('Service_Record', order_by=lambda: Service_Record.service_from)
    career_service = db.relationship('Career_Service', order_by="desc(Career_Service.date_of_examination)")
    vocational_course = db.relationship('Vocational_Course')
    learning_development = db.relationship('Learning_Development', order_by="desc(Learning_Development.ld_date_from)")
    familyBg = db.relationship('Family_Background', order_by=lambda: Family_Background.fb_date_of_birth)
    #college = db.relationship('College')
    college = db.relationship('College', backref='user')
    shirt = db.relationship('Shirt')
    masteral = db.relationship('Masteral')
    doctoral = db.relationship('Doctoral')
    work_experience = db.relationship('Work_Experience', order_by="desc(Work_Experience.date_from)")
    voluntary_work = db.relationship('Voluntary_Work', order_by="desc(Voluntary_Work.date_to)")
    other_information = db.relationship('Other_Information')
    questions = db.relationship('Questions')
    other_questions = db.relationship('Other_Questions')
    character_reference = db.relationship('Character_Reference')
    emergency_contact = db.relationship('Emergency_Contact') 
    staff_moved = db.relationship('Staff_Movement')
    assignatory = db.relationship('Assignatory')
    vaccine = db.relationship('Vaccine')
    afl = db.relationship('Afl')
    rol = db.relationship('Records_Of_Leave', backref='user')
    # saln_summary = db.relationship('Saln_Summary')
    saln_summary = db.relationship('Saln_Summary', back_populates='user', uselist=False)
    other_vaccine = db.relationship('Other_Vaccine', order_by="desc(Other_Vaccine.vac_date)")
    payslip = db.relationship('Payslip', order_by="desc(Payslip.period_from)")
    #section = db.relationship('Agency_Section')

    @hybrid_property
    def fullname(self):
        name_extn = ""
        middle_name = ""

        if self.name_extn != "N/A" and self.name_extn != "":
            name_extn = self.name_extn

        if self.middle_name != "N/A":
            middle_name = self.middle_name

        return f"{self.first_name} {middle_name} {self.last_name} {name_extn}".strip()

        
    @hybrid_property
    def proper_fullname(self):
        name_extn = ""
        middle_name = ""

        if self.name_extn != "N/A" and self.name_extn != "":
            name_extn = self.name_extn

        if self.middle_name != "N/A":
            middle_name = self.middle_name

        return f"{self.last_name}, {self.first_name} {name_extn} {middle_name}".strip()
    

    def as_dict(self):
       return {c.name: str((getattr(self, c.name))) for c in self.__table__.columns}

    @property
    def getAge(self):
        today = datetime.now().date()
        age = relativedelta(today, self.birthdate).years
        return age
    
    def effectivityOfSeparation(self):
        year_to_add = relativedelta(years=65)
        updated_date = self.birthdate + year_to_add

        return updated_date

    def getYearsInService(self):
        today = datetime.now().date()
        yearsInService = relativedelta(today, self.first_day_in_service).years
        return yearsInService

    def awardClaimingYear(self):
        one_year = relativedelta(years=1)
        year_to_add = 0
        claiming_years = []

        if self.first_day_in_service:
            # if self.getYearsInService() <= 10:
            #     year_to_add = relativedelta(years=10)
            # else:
            #     year_divided = math.ceil((self.getYearsInService() - 10) / 5) * 5
            #     year_to_add = relativedelta(years=10) + relativedelta(years=year_divided)
                
            for x in range(10, 45+5, 5):
                #checking if month is more than June
                if self.first_day_in_service.month > 6:
                    updated_date = self.first_day_in_service + relativedelta(years=x) + one_year
                    claiming_years.append(updated_date.strftime('%Y'))
                else:
                    updated_date = self.first_day_in_service + relativedelta(years=x)
                    claiming_years.append(updated_date.strftime('%Y'))
                
            return claiming_years

    def CscAwardClaimingYear(self):
        one_year = relativedelta(years=1)
        year_to_add = 0
        claiming_years = []

        if self.first_day_in_service:
                
            for x in range(15, 45+5, 5):
                #checking if month is more than June
                if self.first_day_in_service.month > 9:
                    updated_date = self.first_day_in_service + relativedelta(years=x) + one_year
                    claiming_years.append(updated_date.strftime('%Y'))
                else:
                    updated_date = self.first_day_in_service + relativedelta(years=x)
                    claiming_years.append(updated_date.strftime('%Y'))
                
            return claiming_years

    # emergency_contact = db.relationship('Emergency_Contact')

class Payslip(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    period_from = db.Column(db.Date())
    period_to = db.Column(db.Date())
    filename = db.Column(db.String(150), default=False)
    user = db.relationship('User')


class Calendar_Events(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    e_title = db.Column(db.String(150))
    e_venue = db.Column(db.String(150))
    e_all_day = db.Column(db.Boolean(), default=False)
    e_type = db.Column(db.String(150))
    e_repeat = db.Column(db.String(150))
    e_date_from = db.Column(db.DateTime())
    e_date_to = db.Column(db.DateTime())
    e_description = db.Column(db.String(150))


    # rp_total = db.Column(db.String(150))
    # pp_total = db.Column(db.String(150))
    # lia_total = db.Column(db.String(150))
    # networth = db.Column(db.String(150))
    # as_of = db.Column(db.Date())
    last_updated = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    # user = db.relationship('User')

class Saln_Summary(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rp_total = db.Column(db.String(150))
    pp_total = db.Column(db.String(150))
    lia_total = db.Column(db.String(150))
    networth = db.Column(db.String(150))
    as_of = db.Column(db.Date())
    last_updated = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    user = db.relationship('User')


class File_Logs(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    file_name = db.Column(db.String(150))
    file_path = db.Column(db.String(150))
    file_tag = db.Column(db.String(150))
    file_type = db.Column(db.String(150))
    blob_file = db.Column(db.LargeBinary(length=1000000))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    user = db.relationship('User', backref='user_file_logs', lazy=True)


class Real_Property(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rp_description = db.Column(db.String(150))
    rp_kind = db.Column(db.String(150))
    rp_exact_location = db.Column(db.String(150))
    rp_assessed_value = db.Column(db.String(150))
    rp_current_market_value = db.Column(db.String(150))
    rp_acquisition_year = db.Column(db.String(150))
    rp_acquisition_mode = db.Column(db.String(150))
    rp_acquisition_cost = db.Column(db.String(150))
    user = db.relationship('User', backref='user_real_property', lazy=True)


class Personal_Property(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pp_description = db.Column(db.String(150))
    pp_year_acquired = db.Column(db.String(150))
    pp_acquisition_cost = db.Column(db.String(150))
    user = db.relationship('User', backref='user_personal_property', lazy=True)


class Liability(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liability_nature = db.Column(db.String(150))
    liability_creditor = db.Column(db.String(150))
    liability_outstanding_balance = db.Column(db.String(150))
    user = db.relationship('User', backref='user_liability', lazy=True)

class Business_Interest(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    business = db.Column(db.String(150))
    business_address = db.Column(db.String(150))
    business_nature = db.Column(db.String(150))
    business_acquisition = db.Column(db.String(150))
    user = db.relationship('User', backref='user_business_interest', lazy=True)

class Relatives_In_Government(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    relative_name = db.Column(db.String(150))
    relative_relationship = db.Column(db.String(150))
    relative_position = db.Column(db.String(150))
    relative_agency_office = db.Column(db.String(150))
    relative_agency_office_address = db.Column(db.String(150))
    user = db.relationship('User', backref='user_relative_in_government', lazy=True)

class Records_Of_Leave(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vacation = db.Column(db.Numeric(precision=10, scale=3))
    sick = db.Column(db.Numeric(precision=10, scale=3))
    as_of = db.Column(db.Date())


class Afl(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    leave_id = db.Column(db.Integer)
    # other_remarks = db.Column(db.String(150), nullable=True)
    # wph = db.Column(db.Integer, nullable=True)
    # wph_remarks = db.Column(db.String(150), nullable=True)
    # abroad = db.Column(db.Integer, nullable=True)
    # abroad_remarks = db.Column(db.String(150), nullable=True)
    # in_hospital = db.Column(db.String(150), nullable=True)
    # out_patient = db.Column(db.Integer, nullable=True)
    # out_patient_illness = db.Column(db.String(150), nullable=True)
    # slbw_illness = db.Column(db.String(150), nullable=True)
    # masters = db.Column(db.Integer, nullable=True)
    # bar = db.Column(db.Integer, nullable=True)
    # monetization = db.Column(db.Integer, nullable=True)
    # terminal_leave = db.Column(db.Integer, nullable=True)
    no_working_days_applied_for = db.Column(db.String(150), nullable=True)
    date_range = db.Column(db.String(150), nullable=True)
    date_start = db.Column(db.Date(), nullable=True)
    date_end = db.Column(db.Date(), nullable=True)
    filing_date = db.Column(db.String(150), nullable=True)
    # approval = db.Column(db.Integer, nullable=True)
    # disapproval_remarks = db.Column(db.String(150), nullable=True)
    # commutation = db.Column(db.Integer, nullable=True)
    blob_file = db.Column(db.LargeBinary(length=1000000))

class Agency_Section(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    section_title = db.Column(db.String(150))
    section_chief = db.Column(db.String(150))
    user = db.relationship('User', backref='user_section', lazy=True)
    agency_unit = db.relationship('Agency_Unit')
    # user = db.relationship('User', back_populates="section_rel")

class Agency_Unit(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    unit_title = db.Column(db.String(150))
    unit_head = db.Column(db.String(150))
    agency_address = db.Column(db.String(150))
    agency_section = db.Column(db.Integer, db.ForeignKey('agency__section.id'))
    user = db.relationship('User', backref='user_unit', lazy=True)

class Vocational_Course(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    v_school = db.Column(db.String(150))
    vocational_trade_course = db.Column(db.String(150))
    v_period_of_attendance_from = db.Column(db.String(150))
    v_period_of_attendance_to = db.Column(db.String(150))
    v_highest_level = db.Column(db.String(150))
    v_highest_grade_year_units = db.Column(db.String(150))
    v_scholarship_academic_honor = db.Column(db.String(150))
    v_date_of_validity = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Career_Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cs_eligibility = db.Column(db.String(150))
    cs_rating = db.Column(db.String(150))
    date_of_examination = db.Column(db.String(150))
    date_of_examination_to = db.Column(db.String(150))
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
    service_from = db.Column(db.String(150))
    service_to = db.Column(db.String(150))
    designation = db.Column(db.String(150))
    status = db.Column(db.String(50))
    salary = db.Column(db.String(50))
    per = db.Column(db.String(50))
    station_place = db.Column(db.String(150))
    leave_wo_pay = db.Column(db.String(50), nullable=True)
    separation_date = db.Column(db.String(150), nullable=True)
    separation_cause = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def serialize(self):
        return {
            'id': self.id,
            'service_from': self.service_from,
            'service_to': self.service_to,
            'designation': self.designation,
            'status': self.status,
            'salary': self.salary,
            'per': self.per,
            'station_place': self.station_place,
            'leave_wo_pay': self.leave_wo_pay,
            'separation_date': self.separation_date,
            'separation_cause': self.separation_cause,
            'user_id': self.user_id
        }

class Appointment(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    service_from = db.Column(db.String(50))
    service_to = db.Column(db.String(50))
    designation = db.Column(db.String(150))
    status = db.Column(db.String(50))
    salary = db.Column(db.String(50))
    station_place = db.Column(db.String(150))
    leave_wo_pay = db.Column(db.String(50))
    separation_date = db.Column(db.String(50), nullable=True)
    separation_cause = db.Column(db.String(50), nullable=True)
    appointment_attachment = db.Column(db.String(150))
    appointment_attachment_file_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Learning_Development(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    ld_program = db.Column(db.String(250))
    ld_date_from = db.Column(db.String(50))
    ld_date_to = db.Column(db.String(50))
    ld_no_hours = db.Column(db.String(50))
    ld_type = db.Column(db.String(50))
    ld_sponsored_by = db.Column(db.String(250))
    ld_attachment = db.Column(db.String(250))
    ld_attachment_file_name = db.Column(db.String(250))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Vaccine(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    vac_id_no = db.Column(db.String(150))
    vac_brand = db.Column(db.String(150))
    vac_place = db.Column(db.String(150))
    vac_first_dose = db.Column(db.String(150))
    vac_second_dose = db.Column(db.String(150))
    booster_id_no = db.Column(db.String(150))
    booster_brand = db.Column(db.String(150))
    booster_place = db.Column(db.String(150))
    booster_date = db.Column(db.String(150))

    booster_id_no2 = db.Column(db.String(150))
    booster_brand2 = db.Column(db.String(150))
    booster_place2 = db.Column(db.String(150))
    booster_date2 = db.Column(db.String(150))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Other_Vaccine(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    vac_brand = db.Column(db.String(150))
    vac_type = db.Column(db.String(150))
    vac_place = db.Column(db.String(150))
    vac_date = db.Column(db.Date())
    vac_year = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Staff_Movement(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    employment_status = db.Column(db.String(50))
    date_of_effectivity = db.Column(db.String(50))
    section = db.Column(db.String(50))
    unit = db.Column(db.String(50))
    sg = db.Column(db.String(50))
    step = db.Column(db.String(50))
    position_title = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Family_Background(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    fb_last_name = db.Column(db.String(150))
    fb_first_name = db.Column(db.String(150))
    fb_middle_name = db.Column(db.String(150))
    fb_name_ext = db.Column(db.String(150))
    fb_occupation = db.Column(db.String(150))
    fb_employer_business_name = db.Column(db.String(250))
    fb_business_address = db.Column(db.String(250))
    fb_contact_no = db.Column(db.String(150))
    fb_date_of_birth = db.Column(db.String(150))
    fb_maiden_name = db.Column(db.String(150))
    fb_relationship = db.Column(db.String(150))
    fb_id = db.Column(db.String(150))
    fb_id_no = db.Column(db.String(150))
    fb_date_issued = db.Column(db.String(150))
    fb_deceased = db.Column(db.String(50), default="unchecked")
    fb_abroad = db.Column(db.String(50), default="unchecked")
    user = db.relationship('User', backref='user_family_background', lazy=True)
    # user = db.relationship('User', backref='user_family_background', lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def getAge(self):
        today = datetime.now().date()
        dob_object = datetime.strptime(self.fb_date_of_birth, "%Y-%m-%d").date()
        age = relativedelta(today, dob_object).years
        return age

    @hybrid_property
    def fullname(self):
        if self.fb_middle_name is None or self.fb_middle_name == "N/A" or self.fb_middle_name == "NONE" or self.fb_middle_name == "" :
            self.fb_middle_name = ""
        else:
            self.fb_middle_name = self.fb_middle_name[0] + "."
        if self.fb_last_name is None or self.fb_last_name == "N/A" or self.fb_last_name == "NONE":
            self.fb_last_name = ""
        if self.fb_name_ext is None or self.fb_name_ext == "N/A" or self.fb_name_ext == "NONE":
            self.fb_name_ext = ""
        fullname = str(self.fb_first_name + " " + self.fb_middle_name + " " + self.fb_last_name + " " + " "+ self.fb_name_ext).strip()

        return fullname
    
    def spouse(self):
        if self.fb_relationship == 'SPOUSE':
            # Assuming you have a foreign key relationship to the spouse in your User model
            return self.user.spouse  # Replace 'spouse' with the actual relationship name in your User model
        return None


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

class Work_Experience(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    date_from = db.Column(db.String(50))
    date_to = db.Column(db.String(50))
    position_title = db.Column(db.String(150))
    department_agency_office_company = db.Column(db.String(150))
    agency_address = db.Column(db.String(150))
    monthly_salary = db.Column(db.String(50))
    sg = db.Column(db.String(50))
    step = db.Column(db.String(50))
    status_of_appointment = db.Column(db.String(50))
    govt_service = db.Column(db.String(50))
    immediate_supervisor = db.Column(db.String(150))
    name_of_office_unit = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    wda = db.relationship('Wes_Duties_Accomplishments')
    # def __init__(self, id, date_from):
    #     self.id = id
    #     self.date_from = date_from

class Wes_Duties_Accomplishments(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    wda = db.Column(db.String(450))
    wda_type = db.Column(db.String(450))
    we = db.Column(db.Integer, db.ForeignKey('work__experience.id'))

class Voluntary_Work(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name_of_organization = db.Column(db.String(150))
    address = db.Column(db.String(150))
    date_from = db.Column(db.String(150))
    date_to = db.Column(db.String(150))
    no_hours = db.Column(db.String(150))
    position = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Other_Information(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(150))
    type = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Other_Questions(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(150))
    answer = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Questions(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(150))
    answer = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Character_Reference(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    name_ext = db.Column(db.String(100))
    address = db.Column(db.String(150))
    contact_no = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @hybrid_property
    def fullnamex(self):
        if self.middle_name is None or self.middle_name == "N/A" or self.middle_name == "NONE":
            self.middle_name = ""
        else:
            self.middle_name = self.middle_name[0] + "."
        if self.name_ext is None or self.name_ext == "N/A" or self.name_ext == "N/A" or self.name_ext == "NONE":
            self.name_ext = ""

        if self.last_name is None or self.last_name == "N/A" or self.last_name == "N/A" or self.last_name == "NONE":
            self.last_name = ""
        fullnamex = str(self.first_name + " " + self.middle_name + " " + self.last_name + " " + " "+ self.name_ext).strip()

        return fullnamex

class Emergency_Contact(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    # last_name = db.Column(db.String(100))
    # first_name = db.Column(db.String(100))
    # middle_name = db.Column(db.String(100))
    # name_ext = db.Column(db.String(100))
    fullname = db.Column(db.String(100))
    relationship = db.Column(db.String(50))
    address = db.Column(db.String(150))
    contact_no = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Assignatory(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    assignatory = db.Column(db.String(150), default='ENGR. JOHN N. MOLANO, MSME')
    position_title = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='user_assignatory', lazy=True)


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

# ---------------------------------------------------------------------------- #
#                   This is a working sample and used in WES                   #
# ---------------------------------------------------------------------------- #

class AgencySectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Agency_Section
        # load_instance = True
        # include_fk = True
    section_title = ma.auto_field()

class RealPropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Real_Property
        # load_instance = True
        # include_fk = True
    # rp_description = ma.auto_field()

class PersonalPropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Personal_Property
        # only = ("rp_kind")
        # load_instance = True
        # include_fk = True
    # pp_description = ma.auto_field()

class LiabilitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Liability
        # load_instance = True
        # include_fk = True
    # pp_description = ma.auto_field()

class BusinessInterestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Business_Interest
        # load_instance = True
        # include_fk = True
    # pp_description = ma.auto_field()

class RelativeInGovernmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Relatives_In_Government
        # load_instance = True
        # include_fk = True
    # pp_description = ma.auto_field()

class AgencyUnitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Agency_Unit

class FamilyBackgroundSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Family_Background

class AssignatorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Assignatory

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    agency_section = ma.Nested(AgencySectionSchema, attribute='user_section')
    agency_unit = ma.Nested(AgencyUnitSchema, attribute='user_unit')
    family_background = ma.Nested(FamilyBackgroundSchema, attribute='user_family_background', many=True)
    real_property = ma.Nested(RealPropertySchema, attribute='user_real_property', many=True)
    personal_property = ma.Nested(PersonalPropertySchema, attribute='user_personal_property', many=True)
    liability = ma.Nested(LiabilitySchema, attribute='user_liability', many=True)
    business_interest = ma.Nested(BusinessInterestSchema, attribute='user_business_interest', many=True)
    relative_in_government = ma.Nested(RelativeInGovernmentSchema, attribute='user_relative_in_government', many=True)
    assignatory = ma.Nested(AssignatorySchema, attribute='user_assignatory')

class WesDutiesAccomplishmentsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wes_Duties_Accomplishments
        include_fk = True

class WorkExperienceSchema(ma.SQLAlchemyAutoSchema):

    wda = ma.Nested(WesDutiesAccomplishmentsSchema, many=True)

    class Meta:
        model = Work_Experience
        # include_fk = True
        # fields = ('id', 'date_from')
        # id = ma.auto_field()
        # name = ma.auto_field()
        # books = ma.auto_field()


import calendar
import json
import os
from datetime import date, datetime


import pytz
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from flask import (Blueprint, current_app, redirect, render_template,
                   request, send_file, session, url_for, jsonify)
from flask_login import current_user, login_user, logout_user, login_required

#from flask.ext.principal import Principal, Permission, RoleNeed
from flask_principal import Permission, RoleNeed, identity_changed, Identity
from sqlalchemy import desc, extract
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, generateWes
from .models import (College, Family_Background, Masteral, Other_Information,
                     Uploaded_File, User, Vocational_Course, Work_Experience,
                     WorkExperienceSchema, Doctoral, Vocational_Course, Voluntary_Work,
                     Learning_Development, Shirt, Career_Service, Emergency_Contact, File_Logs, Afl, Saln_Summary, UserSchema)
from bs4 import BeautifulSoup 
import requests

from collections import defaultdict

UTC = pytz.utc
PST = pytz.timezone('Asia/Manila')

views = Blueprint('views', __name__)

admin_permission = Permission(RoleNeed('admin'))

@views.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))


def getdata(url): 
    r = requests.get(url) 
    return r.text

@views.route('/data-privacy-act', methods=['GET', 'POST'])
# @login_required
def dataPrivacyAct():
    
    employee_id = session.get('user_id')
    user = User.query.get(employee_id)

    if request.method == 'POST':
        # user = User.query.get(employee_id)
        if user:
            login_user(user)
                    # current_user.data_privacy = 0
            if user.type_of_user == 'admin':
                identity_changed.send(current_app._get_current_object(),
                                identity=Identity(user.id))
                return redirect(url_for('views.admin_dashboard'))
            elif user.type_of_user == 'super admin':
                return redirect(url_for('views.super_admin_dashboard'))
            else: #user access only
                return redirect(url_for('views.dashboard'))

        else:
                #session['error_msg'] = 'Employee ID number does not exist!'
            return jsonify("id_does_not_exist")
    elif request.method == 'GET':
        # users = db.session.query(User).options(db.defer('acknowledgement')).all()

        return render_template('data_privacy_act.html', user_profile = user,
                                                        date_now = datetime.now(PST))


@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # print('current_user_data======+++++++========================================>>', user.data_privacy)

    new_uploaded_File = Uploaded_File.query.filter_by(file_tag = 'dform').all()
    column_keys = Uploaded_File.__table__.columns.keys()
    # Temporary dictionary to keep the return value from table
    rows_dic_temp = {}
    rows_dic = []
    # Iterate through the returned output data set
    for row in new_uploaded_File:
        for col in column_keys:
            rows_dic_temp[col] = getattr(row, col)
        rows_dic.append(rows_dic_temp)
        rows_dic_temp= {}

    current_year = date.today().year
    print(current_year)
    month = date.today().month
    print(month)
    day = date.today().strftime("%d")
    print("today ",day)
    num_days = calendar.monthrange(current_year, month)
    print(num_days[1])
        
    get_bday_celebs = User.query.filter_by(status_remarks = "ACTIVE").filter(extract("month", User.birthdate) == month).filter(extract("day", User.birthdate) <= 31).order_by(extract("day", User.birthdate)).all()
    db.session.commit()

    htmldata = getdata("https://www.crfv-cpu.org/resources/category/weekly-value-focus") 
    soup = BeautifulSoup(htmldata, 'html.parser')
    
    for item in soup.find_all('img'):
        print(item['src'])


    
    blog_title = soup.find_all("a", {"class": "blog-title-link"})
    blog_content = soup.find_all("div", {"class": "blog-content"})

    for content in blog_content:
        blog_paragraph = content.find('div', {"class":"paragraph"})
        blog_image = content.find('img')

    return render_template('dashboard.html', dforms = rows_dic, bday_celebs = get_bday_celebs, blog_title = blog_title, blog_image = blog_image, blog_paragraph = blog_paragraph)

@views.route('/birthday-celebrators/<mydate>', methods=['GET', 'POST'])
def birthday_celebrators(mydate):
    current_year = date.today().year

    dateinput = date(int(current_year), int(mydate), 1)

    # month = dateinput.month
    # day = date.today().strftime("%d")

    # Extract month and day from the date
    month = dateinput.month
    day = dateinput.day

    get_bday_celebs = User.query.filter_by(status_remarks = "ACTIVE").filter(extract("month", User.birthdate) == month).filter(extract("day", User.birthdate) <= 31).order_by(extract("day", User.birthdate)).all()
    db.session.commit()

    user_schema = UserSchema(many=True)
    serialized_data = user_schema.dump(get_bday_celebs)

    return jsonify(serialized_data)

@views.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def admin_dashboard():
    users = db.session.query(User).options(db.defer('acknowledgement')).all()

    return render_template('admin-dashboard.html', user_profile = users,
                                                     User = User, 
                                                     College = College, 
                                                     Masteral = Masteral,
                                                     Doctoral = Doctoral,
                                                     Vocational_Course = Vocational_Course,
                                                     Work_Experience = Work_Experience,
                                                     Voluntary_Work = Voluntary_Work,
                                                     Learning_Development = Learning_Development,
                                                     Career_Service = Career_Service,
                                                     Shirt = Shirt,
                                                     Emergency_Contact = Emergency_Contact,
                                                     date_now = datetime.now(PST))

@views.route('/learning-development/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def learning_development(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(emp_id)
            db.session.commit()

            return render_template('learning_development.html', emp_id = emp_id, user_profile = user)

@views.route('/family-background/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def family_background(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            spouse = db.session.query(Family_Background).filter_by(user_id = emp_id, fb_relationship = "SPOUSE")
            spouse_count = spouse.count()
            db.session.commit()

            return render_template('family_bg.html', emp_id = emp_id, user_profile = user, spouse = spouse, spouse_count = spouse_count)

@views.route('/covid-vaccine/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def covid_vaccine(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()

            return render_template('vaccination.html', emp_id = emp_id, user_profile = user)

@views.route('/other-vaccine/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def other_vaccine(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()

            return render_template('other_vaccination.html', emp_id = emp_id, user_profile = user)

@views.route('/change-password/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def change_password(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()
            
            return render_template('change_password.html', emp_id = emp_id, user_profile = user)

@views.route('/tshirt-sizes/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def shirt_size(emp_id):
    user = db.session.query(User).get(int(emp_id))
    db.session.commit()
    return render_template('t_shirt_sizes.html', emp_id = emp_id, user_profile = user)

@views.route('/work-experience/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def work_experience(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()
            return render_template('work_experience.html', emp_id = emp_id, user_profile = user)

@views.route('/voluntary-work/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def voluntary_work(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()
            return render_template('voluntary_work.html', emp_id = emp_id, user_profile = user)

@views.route('/other-information/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def other_information(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()
            return render_template('other_information.html', emp_id = emp_id, user_profile = user)

@views.route('/questions/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def questions(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()
            return render_template('questions.html', emp_id = emp_id, user_profile = user)

@views.route('/other-questions/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def other_questions(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()
            return render_template('other-questions.html', emp_id = emp_id, user_profile = user)

@views.route('/character-reference/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def character_reference(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()
            return render_template('character_reference.html', emp_id = emp_id, user_profile = user)

@views.route('/person-administering/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def person_administering(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()
            return render_template('person-administering-oath.html', emp_id = emp_id, user_profile = user)

@views.route('/print-preview/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def print_preview(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            spouse = db.session.query(Family_Background).filter_by(user_id = emp_id, fb_relationship = "SPOUSE")
            father = db.session.query(Family_Background).filter_by(user_id = emp_id, fb_relationship = "FATHER")
            mother = db.session.query(Family_Background).filter_by(user_id = emp_id, fb_relationship = "MOTHER")
            child = db.session.query(Family_Background).filter_by(user_id = emp_id, fb_relationship = "CHILD").order_by(desc(Family_Background.fb_date_of_birth))
            vocation = db.session.query(Vocational_Course).filter_by(user_id = emp_id)
            college = db.session.query(College).filter_by(user_id = emp_id)
            masteral = db.session.query(Masteral).filter_by(user_id = emp_id)
            other = db.session.query(Other_Information).filter_by(user_id = emp_id, type="HOBBIES")
            recognition = db.session.query(Other_Information).filter_by(user_id = emp_id, type="RECOGNITION")
            membership = db.session.query(Other_Information).filter_by(user_id = emp_id, type="MEMBERSHIP")

            spouse_count = spouse.count()
            db.session.commit()

            return render_template('print_preview.html',
                emp_id = emp_id,
                user_profile = user,
                spouse = spouse, 
                child = child, 
                father = father, 
                mother = mother,
                vocation = vocation,
                college = college,
                masteral = masteral,
                spouse_count = spouse_count,
                other = other,
                recognition = recognition,
                membership = membership,
                )

@views.route('/emergency-contact/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def emergency_contact(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()
            return render_template('emergency_contact.html', emp_id = emp_id, user_profile = user)

@views.route('/appointment/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def appointment(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()
            return render_template('appointment.html', emp_id = emp_id, user_profile = user)

@views.route('/wes/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def wes(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()

            url_for('static', filename='my_pds_template2.pdf')

            return render_template('generate_wes.html', emp_id = emp_id, user_profile = user)

@views.route('/check-before-gen/<emp_id>', methods=['GET'])
def check_before_gen(emp_id):
    work_exp_schema = WorkExperienceSchema(many=True)

    get_we = Work_Experience.query.filter_by(user_id = emp_id).order_by(desc(Work_Experience.date_from)).all()

    my_rows = json.loads(jsonify(row_contents=work_exp_schema.dump(get_we)).get_data(True))

    my_empty_rows = []

    empty_accomp = 0
    empty_summary = 0
    empty_agency_address = 0
    empty_immediate_supervisor = 0
    empty_name_of_office_unit = 0
    wda_len = 0

    for idx, item in enumerate(my_rows["row_contents"]):
        if item["agency_address"] != "":
            empty_agency_address = empty_agency_address + 1
        if item["immediate_supervisor"] != "":
            empty_immediate_supervisor = empty_immediate_supervisor + 1
        if item["name_of_office_unit"] != "":
            empty_name_of_office_unit = empty_name_of_office_unit + 1

        for idx2, item2 in enumerate(my_rows["row_contents"][idx]["wda"]):

            if item2["wda_type"] == 'accomplishment':
                empty_accomp = empty_accomp + 1
                # print("HELLO WORLD acc: ", item2["wda_type"])

            elif item2["wda_type"] == 'summary':
                empty_summary = empty_summary + 1
                # print("HELLO WORLD SUMM: ", item2["wda_type"])

            # print("before IF acc: ", empty_accomp)
            print("before IF: ", empty_agency_address)
        if empty_accomp == 0 or empty_summary == 0 or empty_agency_address == 0 or empty_immediate_supervisor == 0 or empty_name_of_office_unit == 0:
            return my_rows["row_contents"][idx]
             
        empty_agency_address = 0
        
        empty_accomp = 0
        empty_summary = 0
        wda_len = 0
        
            # dt_obj_date_to = datetime.strptime(item['date_to'],'%Y-%m-%d')
            # new_value_date_to = datetime.strftime(dt_obj_date_to, "%B %d, %Y")
    
        # my_rows["row_contents"][idx]['date_from'] = new_value

    # return my_rows <- this is working
    return '200'


@views.route("/gen/<emp_id>", methods=['GET', 'POST'])
def gen_docx(emp_id):

    template = os.path.join(current_app.root_path, 'static/templates', 'WES_TEMPLATE.docx')   

    document = generateWes.from_template(template, emp_id)
    document.seek(0)
    
    return send_file(
        document, mimetype='application/vnd.openxmlformats-'
        'officedocument.wordprocessingml.document', as_attachment=True,
        attachment_filename='WES_TEMPLATE_NEW.docx')


@views.route('/afl/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def afl(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            primary_certifier = db.session.query(User).filter_by(is_primary_afl_certifier = 1).all()
            secondary_certifier = db.session.query(User).filter_by(is_secondary_afl_certifier = 1).all()
            files = File_Logs.query.filter_by(user_id=emp_id).all()

            current_year = datetime.now().year
            january_1 = datetime(current_year, 1, 1)
            december_31 = datetime(current_year, 12, 31)
            december_31_1 = datetime(current_year-1, 12, 31)
            # Fetch AFL data
            # get_afl = Afl.query.filter_by(user_id=emp_id).all()
            get_afl = Afl.query.filter(
                # db.extract('year', Afl.date_start) <= current_year,
                # db.extract('year', Afl.date_end) >= current_year,
                Afl.date_start >= december_31_1,
                Afl.date_end <= december_31,
                Afl.user_id == emp_id
            ).all()

            print("======>>>>>", get_afl)

            # Group AFLs by leave_id
            # grouped_afls = defaultdict(list)
            # for afl in get_afl:
            #     grouped_afls[afl.leave_id].append(afl)

            # grouped_afls_dict = dict(grouped_afls)


            # Group AFLs by leave_id and calculate the sum of no_working_days_applied_for
            grouped_afls2 = defaultdict(int)
            for afl2 in get_afl:
                grouped_afls2[afl2.leave_id] += int(afl2.no_working_days_applied_for) if afl2.no_working_days_applied_for else 0

            # Convert defaultdict to a regular dictionary
            grouped_afls_dict2 = dict(grouped_afls2)


            return render_template('afl.html', emp_id = emp_id, user_profile = user, primary_certifier = primary_certifier, secondary_certifier = secondary_certifier, files = files, grouped_afls_dict2 = grouped_afls_dict2)

@views.route('/afl-logs/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def afl_logs(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))

            current_year = datetime.now().year
            # Fetch AFL data

            get_afl = Afl.query.filter_by(user_id=emp_id).all()
            get_afl = Afl.query.filter_by(user_id=emp_id).order_by(desc(Afl.id)).all()

            # get_afl = Afl.query.filter(
            #     db.extract('year', Afl.date_start) == current_year,
            #     db.extract('year', Afl.date_end) == current_year,
            #     Afl.user_id == emp_id
            # ).all()

            db.session.commit()

            return render_template('afl-logs.html', emp_id = emp_id, user_profile = user, get_afl = get_afl)

@views.route('/rol/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def rol(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()

            return render_template('rol.html', emp_id = emp_id, user_profile = user)
        
@views.route('/coe-menu/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def coe(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(int(emp_id))
            db.session.commit()

            return render_template('coe.html', emp_id = emp_id, user_profile = user)
            

@views.route('/saln/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def saln(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(emp_id)
            db.session.commit()

            return render_template('saln.html', emp_id = emp_id, user_profile = UserSchema().dump(user))
            # return render_template('saln.html', emp_id = emp_id, user_profile = user)


@views.route('/saln-reports', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def salnReports():
    if request.method == 'GET':
        user = db.session.query(User).all()
        users_with_saln = User.query.join(Saln_Summary).filter(User.saln_summary != None, User.status_remarks == 'ACTIVE').all()
        db.session.commit()

        return render_template('saln-reports.html', user_profile = user, users_with_saln = users_with_saln)


@views.route('/file-log/<emp_id>', methods=['GET', 'POST'])
@login_required
# @admin_permission.require(http_exception=403)
def file_logs(emp_id):
    if request.method == 'GET':
        if str(current_user.id) != str(emp_id) and current_user.type_of_user == "user":
            return "YOU DO NOT HAVE ACCESS TO THIS PAGE! :P ", 404
        else:
            user = db.session.query(User).get(emp_id)
            files = File_Logs.query.filter_by(user_id=emp_id, file_tag='AFL').all()

            db.session.commit()

            return render_template('file_logs.html', emp_id = emp_id, user_profile = UserSchema().dump(user), files = files)
            # return render_template('saln.html', emp_id = emp_id, user_profile = user)


@views.route('/500', methods=['GET'])
# @login_required
# @admin_permission.require(http_exception=403)
def get500page():
    if request.method == 'GET':
        return render_template('500.html')

@views.route('/clear-cache', methods=['GET'])
# @login_required
# @admin_permission.require(http_exception=403)
def getClearCache():
    if request.method == 'GET':
        return render_template('clear-cache.html')

@views.route('/directories', methods=['GET'])
# @login_required
# @admin_permission.require(http_exception=403)
def directories():
    if request.method == 'GET':
        return render_template('directories.html')

@views.context_processor
def inject_today_date():
    return {'today_date': datetime.utcnow()}


@views.context_processor
def inject_today_date_formatted():
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    return {'today_date_formatted': today_date}

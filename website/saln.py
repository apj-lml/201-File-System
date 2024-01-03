from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app, send_file
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Real_Property, Personal_Property, Liability, Business_Interest, Relatives_In_Government,\
     User, UserSchema, PersonalPropertySchema, RealPropertySchema, LiabilitySchema, BusinessInterestSchema, RelativeInGovernmentSchema
from . import db
import datetime
import time
from .myhelper import allowed_file, my_random_string
from werkzeug.utils import secure_filename
from io import BytesIO
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from dateutil.relativedelta import relativedelta

import json
import os, os.path


saln = Blueprint('saln', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@saln.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------- #
#                              add real property                               #
# ---------------------------------------------------------------------------- #
@saln.route('add-rp/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_rp(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        for k,v in formdata.items():
            if type(v) is str:
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})

        formdata["user_id"] = emp_id

        for k,v in formdata.items():
            if type(v) is str and k != 'comments_remarks':
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})

        add_rp = Real_Property(**formdata)

        db.session.add(add_rp)
        db.session.commit()
        db.session.flush()

        print(formdata)
        return jsonify(**formdata)

 # ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                              add personal property                           #
# ---------------------------------------------------------------------------- #
@saln.route('add-pp/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_pp(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        for k,v in formdata.items():
            if type(v) is str:
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})

        formdata["user_id"] = emp_id

        add_rp = Personal_Property(**formdata)

        db.session.add(add_rp)
        db.session.commit()
        db.session.flush()

        print(formdata)
        return jsonify(**formdata)

 # ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                             add liability property                           #
# ---------------------------------------------------------------------------- #
@saln.route('add-liability/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_liability(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        for k,v in formdata.items():
            if type(v) is str:
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})

        formdata["user_id"] = emp_id

        new_liability = Liability(**formdata)

        db.session.add(new_liability)
        db.session.commit()
        db.session.flush()

        return jsonify(**formdata)

 # ---------------------------------------------------------------------------- #

 # ---------------------------------------------------------------------------- #
#                             add liability property                           #
# ---------------------------------------------------------------------------- #
@saln.route('add-business-interest/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_business_interest(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        for k,v in formdata.items():
            if type(v) is str:
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})

        formdata["user_id"] = emp_id

        new_business_interest = Business_Interest(**formdata)

        db.session.add(new_business_interest)
        db.session.commit()
        db.session.flush()

        return jsonify(**formdata)

 # ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                             add relative property                           #
# ---------------------------------------------------------------------------- #
@saln.route('add-relative-in-government/<emp_id>', methods=['POST', 'GET'])
@login_required
def add_relative_in_government(emp_id):
    if request.method == "POST":
        formdata = request.form.to_dict()

        for k,v in formdata.items():
            if type(v) is str:
                formdata.update({k: v.upper()})
            else:
                formdata.update({k: v})

        formdata["user_id"] = emp_id

        new_relative_in_government = Relatives_In_Government(**formdata)

        db.session.add(new_relative_in_government)
        db.session.commit()
        db.session.flush()

        return jsonify(**formdata)

# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                                PRINT SALN                                    #
# ---------------------------------------------------------------------------- #
@saln.route('print/<emp_id>/<filing_date>/<filing_type>', methods=['POST', 'GET'])
@login_required
def print_saln(emp_id, filing_date, filing_type):
    # formdata  = json.loads(request.data)
    template = os.path.join(current_app.root_path, 'static/templates', 'SALN_Form.docx')   

    document = from_template(template, emp_id, filing_date, filing_type)
    document.seek(0)
    
    return send_file(
        document, mimetype='application/vnd.openxmlformats-'
        'officedocument.wordprocessingml.document', as_attachment=True,
        attachment_filename='SALN.docx')

 # ---------------------------------------------------------------------------- #

def from_template(template, emp_id, filing_date, filing_type):
    target_file = BytesIO()
    
    template = DocxTemplate(template)
    context = get_context(emp_id, filing_date, filing_type)  # gets the context used to render the document
    
    target_file = BytesIO()
    template.render(context, autoescape=True)
    template.save(target_file)
    return target_file

def get_context(id, filing_date, filing_type):
    user = db.session.query(User).get(id)
    
    user_profile = user

    # user_profile.employee_id_date_issued = user_profile.employee_id_date_issued.strftime("%B %d, %Y")

    user_profile.user_real_property = sorted(user_profile.user_real_property, key=lambda x: x.rp_acquisition_year, reverse=True)
    user_profile.user_personal_property = sorted(user_profile.user_personal_property, key=lambda x: x.pp_year_acquired, reverse=True)

    middle_name = user_profile.middle_name[:1] + "." if user_profile.middle_name and user_profile.middle_name != "N/A" else ""
    name_extn = user_profile.name_extn if user_profile.name_extn and user_profile.name_extn != "N/A" else ""

    bi_list = []
    for bi in user_profile.user_business_interest:
        bi_acquistion_date_object = datetime.datetime.strptime(bi.business_acquisition, "%Y-%m-%d").date()
        bi.business_acquisition = bi_acquistion_date_object.strftime("%B %d, %Y")
        bi_list.append(bi)

    user_profile.user_business_interest = bi_list

    rg_list = []
    for rg in user_profile.user_relative_in_government:
        # rg_acquistion_date_object = datetime.datetime.strptime(rg.business_acquisition, "%Y-%m-%d").date()
        # rg.business_acquisition = rg_acquistion_date_object.strftime("%B %d, %Y")
        rg_list.append(rg)

    user_profile.user_relative_in_government = rg_list

    user_profile_dict = UserSchema().dump(user_profile)

    user_profile_dict['full_name'] = user_profile.first_name + " " + middle_name + " " + user_profile.last_name + " " + name_extn
    address = user_profile.p_house_block_lot + ", " + user_profile.p_street + ", " + user_profile.p_subdivision_village + ", " + user_profile.p_barangay + ", " + user_profile.p_city_municipality + ", "+ user_profile.p_province + ", "+ user_profile.p_zip_code
    final_address = address.replace('N/A,', '')
    user_profile_dict['address'] = " ".join(final_address.split())

    user_profile_dict_date_object = datetime.datetime.strptime(user_profile_dict['employee_id_date_issued'], "%Y-%m-%d").date()
    user_profile_dict['employee_id_date_issued'] = user_profile_dict_date_object.strftime("%B %d, %Y")

    # user_profile_dict['spouse_last_name'] = user_profile.familyBg.filter_by(fb_relationship='SPOUSE').first()

    children_list = []

    for child in user_profile.familyBg:
        if child.fb_relationship == 'CHILD':
            filing_date_object = datetime.datetime.strptime(filing_date, "%Y-%m-%d").date()
            dob_object = datetime.datetime.strptime(child.fb_date_of_birth, "%Y-%m-%d").date()
            age_based_on_input = relativedelta(filing_date_object, dob_object)

            if age_based_on_input.years < 18:
                if age_based_on_input.years <= 0:
                    child.childAge = str(age_based_on_input.months) + " MONTH/S OLD"
                else:
                    child.childAge = str(age_based_on_input.years)

                child.formattedBirthDate = dob_object.strftime("%B %d, %Y")
                children_list.append(child)

    spouse = None
    for relative in user_profile.familyBg:
        if relative.fb_relationship == 'SPOUSE':
            spouse = relative
            break

    user_profile_dict['spouse_last_name'] = spouse.fb_last_name if spouse else "N/A"
    user_profile_dict['spouse_first_name'] = spouse.fb_first_name if spouse else "N/A"
    user_profile_dict['spouse_middle_name'] = spouse.fb_middle_name if spouse else "N/A"
    user_profile_dict['spouse_middle_initial'] = spouse.fb_middle_name[0] + "." if spouse else "N/A"
    user_profile_dict['spouse_full_name'] = spouse.fb_first_name + " " + spouse.fb_middle_name[0] + ". " + spouse.fb_last_name if spouse else "N/A"
    # user_profile_dict['spouse_last_name'] = user_profile.familyBg.filter_by(fb_relationship='SPOUSE').first().last_name if user_profile.familyBg else None

    user_profile_dict['spouse_position'] = spouse.fb_occupation if spouse else "N/A"
    user_profile_dict['spouse_agency'] = spouse.fb_employer_business_name if spouse else "N/A"
    user_profile_dict['spouse_office_address'] = spouse.fb_business_address if spouse else "N/A"

    user_profile_dict['spouse_govt_issued_id'] = spouse.fb_id if spouse and spouse.fb_id != "" else "N/A"
    user_profile_dict['spouse_govt_issued_id_no'] = spouse.fb_id_no if spouse and spouse.fb_id_no != "" else "N/A"
    user_profile_dict['spouse_deceased'] = spouse.fb_deceased if spouse and spouse.fb_deceased != "checked" or spouse is None else "checked"
    print(user_profile_dict['spouse_deceased'])

    spouse_govt_issued_id_date_issued_date_obj = datetime.datetime.strptime(spouse.fb_date_issued, "%Y-%m-%d").date() if spouse and spouse.fb_date_issued != "" and spouse.fb_date_issued is not None else "N/A"

    user_profile_dict['spouse_govt_issued_id_date_issued'] = spouse_govt_issued_id_date_issued_date_obj.strftime("%B %d, %Y") if spouse and spouse.fb_date_issued != "" and spouse.fb_date_issued is not None else "N/A"

    user_profile_dict["checkmark"] = "✓"

    date_object = datetime.datetime.strptime(filing_date, "%Y-%m-%d")

    # Format the datetime object as "Month Day, Year"
    formatted_date = date_object.strftime("%B %d, %Y")

    user_profile_dict["filing_date"] = formatted_date
    user_profile_dict["filing_type"] = filing_type
    user_profile_dict["children_list"] = sorted(children_list, key=lambda x: x.childAge, reverse=True)

    user_profile_dict['total_rp_acquisition_cost_p1'] = formatNumber(getRpAcquisitionCostSubTotal(user, 0, 3) + getRpAcquisitionCostSubTotal(user, 3, 7)) if getRpAcquisitionCostSubTotal(user, 0, 3) != 0 else formatNumber(0.00)
    user_profile_dict['total_rp_acquisition_cost_p2'] = formatNumber(getRpAcquisitionCostSubTotal(user, 3, 7)) if getRpAcquisitionCostSubTotal(user, 3, 7) != 0 else formatNumber(0.00)

    user_profile_dict['total_pp_acquisition_cost_p1'] = formatNumber(getPpAcquisitionCostSubTotal(user, 0, 6) + getPpAcquisitionCostSubTotal(user, 6, 12)) if getPpAcquisitionCostSubTotal(user, 0, 6) != 0 else formatNumber(0.00)
    user_profile_dict['total_pp_acquisition_cost_p2'] = formatNumber(getPpAcquisitionCostSubTotal(user, 6, 12)) if getPpAcquisitionCostSubTotal(user, 6, 12) != 0 else formatNumber(0.00)

    user_profile_dict['total_liability_outstanding_balance_p1'] = formatNumber(getLiabilityOutstandingBalance(user, 0, 3) + getLiabilityOutstandingBalance(user, 3, 8)) if getLiabilityOutstandingBalance(user, 0, 3) != 0 else formatNumber(0.00)
    user_profile_dict['total_liability_outstanding_balance_p2'] = formatNumber(getLiabilityOutstandingBalance(user, 3, 8)) if getLiabilityOutstandingBalance(user, 3, 8) != 0 else formatNumber(0.00)
    
    user_profile_dict['total_assets_p1'] = formatNumber(getTotalAssets(getRpAcquisitionCostSubTotal(user, 0, 3), getPpAcquisitionCostSubTotal(user, 0, 6)) + getTotalAssets(getRpAcquisitionCostSubTotal(user, 3, 7), getPpAcquisitionCostSubTotal(user, 6, 12)))
    user_profile_dict['total_assets_p2'] = formatNumber(getTotalAssets(getRpAcquisitionCostSubTotal(user, 3, 7), getPpAcquisitionCostSubTotal(user, 6, 12)))

    user_profile_dict['networth'] = formatNumber(getNetworth(user_profile_dict['total_assets_p1'], user_profile_dict['total_liability_outstanding_balance_p1'], '0.00', '0.00'))

    user_profile_dict['signatory'] = user.assignatory[0].assignatory
    user_profile_dict['signatory_position_title'] = user.assignatory[0].position_title

    # if getRpAcquisitionCostSubTotal(user, 3, 7) != None or getPpAcquisitionCostSubTotal(user, 6, 12) != None or getLiabilityOutstandingBalance(user, 3, 8) != None or len(user_profile.user_business_interest) > 2:
    if getRpAcquisitionCostSubTotal(user, 3, 8) != 0.00 or getPpAcquisitionCostSubTotal(user, 6, 13) != 0.00 or getLiabilityOutstandingBalance(user, 3, 9) != 0.00:
        user_profile_dict['addtl_page'] = True
    else:
        user_profile_dict['addtl_page'] = False

    if len(user_profile.user_business_interest) > 2 or len(user_profile.user_relative_in_government) > 5:
        user_profile_dict['addtl_page_3'] = True
    else:
        user_profile_dict['addtl_page_3'] = False

    return user_profile_dict

def getNetworth(total_assets_p1 = 0.00, total_liability_p1 = 0.00, total_assets_p2 = 0.00, total_liability_p2 = 0.00):
    # if total_assets_p1:
    #     floatAssetsP1 = float(total_assets_p1.replace(',', ''))
    # else:
    #     floatAssetsP1 = 0.00

    # if total_assets_p2:
    #     floatAssetsP2 = float(total_assets_p2.replace(',', ''))
    # else:
    #     floatAssetsP2 = 0.00

    # if total_liability_p1:
    #     floatLiabilityP1 = float(total_liability_p1.replace(',', ''))
    # else:
    #     floatLiabilityP1 = 0.00

    # if total_liability_p2:
    #     floatLiabilityP2 = float(total_liability_p2.replace(',', ''))
    # else:
    #     floatLiabilityP2 = 0.00

    floatNetworth = float(total_assets_p1.replace(',', '')) + float(total_assets_p2.replace(',', '')) - float(total_liability_p1.replace(',', '')) + float(total_liability_p2.replace(',', ''))
    # floatNetworth = (floatAssetsP1 + floatAssetsP2) - (floatLiabilityP1 + floatLiabilityP2)
    formatted_networth = "{:,.2f}".format(floatNetworth)
    return floatNetworth

def getTotalAssets(subtotal1 = 0.00, subtotal2 = 0.00):
    # if subtotal1:
    #     floatSubtotal1 = float(subtotal1.replace(',', ''))
    # else:
    #     floatSubtotal1 = 0.00

    # if subtotal2:
    #     floatSubtotal2 = float(subtotal2.replace(',', ''))
    # else:
    #     floatSubtotal2 = 0.00

    # total = floatSubtotal1 + floatSubtotal2
    total = subtotal1 + subtotal2
    formatted_total = "{:,.2f}".format(total)

    return total
    # return formatted_total

def getLiabilityOutstandingBalance(user, d_start, d_end):
    # Extract the acquisition_cost values from the first four real properties (if available)
    outstanding_balances = []
    liabilities = user.user_liability
    if liabilities:
        for liability in liabilities[d_start:d_end]:
            liability_str = liability.liability_outstanding_balance
            if liability_str:
                # Remove commas and convert to a float
                outstanding_balance = float(liability_str.replace(',', ''))
                outstanding_balances.append(outstanding_balance)
            else:
                formatted_total_outstanding_balance = None


        # Calculate the sum of the first four acquisition_cost values
        total_outstanding_balance = sum(outstanding_balances) if sum(outstanding_balances) > 0 else 0
        formatted_total_outstanding_balance = "{:,.2f}".format(total_outstanding_balance) if sum(outstanding_balances) > 0 else None
    else:
        formatted_total_outstanding_balance = None
        total_outstanding_balance = 0.00
    
    return total_outstanding_balance
    # return formatted_total_outstanding_balance

def formatNumber(x):
        return "{:,.2f}".format(x)
     
def getRpAcquisitionCostSubTotal(user, d_start, d_end):
    # Extract the acquisition_cost values from the first four real properties (if available)
    acquisition_costs = []
    # real_properties = user.user_real_property
    real_properties = sorted(user.user_real_property, key=lambda x: x.rp_acquisition_year, reverse=True)

    if real_properties:
        for real_property in real_properties[d_start:d_end]:
            acquisition_cost_str = real_property.rp_acquisition_cost
            if acquisition_cost_str:
                # Remove commas and convert to a float
                acquisition_cost = float(acquisition_cost_str.replace(',', ''))
                acquisition_costs.append(acquisition_cost)
            else:
                formatted_total_acquisition_cost = 0

        # Calculate the sum of the first four acquisition_cost values
        total_acquisition_cost = sum(acquisition_costs) if sum(acquisition_costs) > 0 else 0
        formatted_total_acquisition_cost = "{:,.2f}".format(total_acquisition_cost) if sum(acquisition_costs) > 0 else None
    else:
        formatted_total_acquisition_cost = 0
        total_acquisition_cost = 0.00
    
    return total_acquisition_cost
    # return formatted_total_acquisition_cost


def getPpAcquisitionCostSubTotal(user, d_start, d_end):
    # Extract the acquisition_cost values from the first four real properties (if available)
    acquisition_costs = []
    personal_properties = user.user_personal_property
    # personal_properties = sorted(user.user_personal_property, key=lambda x: x.pp_year_acquired, reverse=True)

    if personal_properties:
        for personal_property in personal_properties[d_start:d_end]:
            acquisition_cost_str = personal_property.pp_acquisition_cost
            if acquisition_cost_str:
                # Remove commas and convert to a float
                acquisition_cost = float(acquisition_cost_str.replace(',', ''))
                acquisition_costs.append(acquisition_cost)
            else:
                formatted_total_acquisition_cost = None

        # Calculate the sum of the first four acquisition_cost values
        total_acquisition_cost = sum(acquisition_costs) if sum(acquisition_costs) > 0 else 0
        formatted_total_acquisition_cost = "{:,.2f}".format(total_acquisition_cost) if sum(acquisition_costs) > 0 else None
    else:
        formatted_total_acquisition_cost = None
        total_acquisition_cost = 0.00
    
    # return formatted_total_acquisition_cost
    return total_acquisition_cost

# ---------------------------------------------------------------------------- #
#                          delete liability property                           #
# ---------------------------------------------------------------------------- #
@saln.route('delete', methods=['POST', 'GET'])
@login_required
def delete_saln():
    if request.method == "POST":
        formdata  = json.loads(request.data)

        if formdata['type'] == "rp":
            dbObject = Real_Property
        if formdata['type'] == "pp":
            dbObject = Personal_Property
        if formdata['type'] == "liability":
            dbObject = Liability
        if formdata['type'] == "business":
            dbObject = Business_Interest
        if formdata['type'] == "relative":
            dbObject = Relatives_In_Government

        delete_saln = dbObject.query.get(formdata['id'])

        db.session.delete(delete_saln)
        db.session.commit()
        return jsonify({})

# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                            edit liability property                           #
# ---------------------------------------------------------------------------- #
@saln.route('edit', methods=['POST', 'GET'])
@login_required
def edit_saln():
    if request.method == "POST":
        formdata  = json.loads(request.data)

        if formdata['type'] == "rp":
            dbObject = Real_Property
            schema = RealPropertySchema()

        if formdata['type'] == "pp":
            dbObject = Personal_Property
            schema = PersonalPropertySchema()

        if formdata['type'] == "liability":
            dbObject = Liability
            schema = LiabilitySchema()
        
        if formdata['type'] == "business":
            dbObject = Business_Interest
            schema = BusinessInterestSchema()

        if formdata['type'] == "relative":
            dbObject = Relatives_In_Government
            schema = RelativeInGovernmentSchema()


        get_DATA = dbObject.query.get(formdata['id'])

        db.session.commit()
        data = schema.dump(get_DATA)
        return jsonify(data)

# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
#                          update liability property                           #
# ---------------------------------------------------------------------------- #
@saln.route('test', methods=['POST', 'GET'])
@login_required
def saln_test():
    if request.method == "POST":
        formdata = json.loads(request.data)

        # for k,v in formdata.items():
        #     if type(v) is str:
        #         formdata.update({k: v.upper()})
        #     else:
        #         formdata.update({k: v})

        if formdata['type'] == "rp":
            dbObject = Real_Property
        if formdata['type'] == "pp":
            dbObject = Personal_Property
        if formdata['type'] == "liability":
            dbObject = Liability
        if formdata['type'] == "business":
            dbObject = Business_Interest
        if formdata['type'] == "relative":
            dbObject = Relatives_In_Government

        get_DATA = dbObject.query.get(formdata['id'])

        for key, value in formdata.items():
            if type(value) is str:
                setattr(get_DATA, key, value.upper())
            else:
                setattr(get_DATA, key, value)


        db.session.commit()

    return jsonify('success')

# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                     get data                                 #
# ---------------------------------------------------------------------------- #
@saln.route('get-data/<saln_type>/<user_profile_id>', methods=['POST', 'GET'])
@login_required
def get_data(saln_type, user_profile_id):
    if saln_type == "rp":
        dbObject = Real_Property
        schema = RealPropertySchema()

    if saln_type == "pp":
        dbObject = Personal_Property
        schema = PersonalPropertySchema()

    if saln_type == "liability":
        dbObject = Liability
        schema = LiabilitySchema()
    
    if saln_type == "business":
        dbObject = Business_Interest
        schema = BusinessInterestSchema()
    
    if saln_type == "relative":
        dbObject = Relatives_In_Government
        schema = RelativeInGovernmentSchema()

    get_DATA = dbObject.query.filter_by(user_id=user_profile_id).all()
    data = schema.dump(get_DATA, many=True)

    return jsonify(data)
# ---------------------------------------------------------------------------- #
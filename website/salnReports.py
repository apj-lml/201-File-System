from flask import Blueprint, request, redirect, url_for, session, jsonify, current_app, send_file
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from .models import Real_Property, Personal_Property, Liability, Business_Interest, Relatives_In_Government,\
     User, UserSchema, PersonalPropertySchema, Real_Property, Personal_Property, Liability, RealPropertySchema, LiabilitySchema, BusinessInterestSchema, RelativeInGovernmentSchema
from . import db
import datetime
import time
from .myhelper import allowed_file, my_random_string
from werkzeug.utils import secure_filename
from io import BytesIO
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from sqlalchemy.sql import label 
import json
import os, os.path


salnReports = Blueprint('salnReports', __name__)
# ALLOWED_EXTENSIONS = {'pdf'}

admin_permission = Permission(RoleNeed('admin'))

@salnReports.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('auth.login'))


# ---------------------------------------------------------------------------- #
#                                PRINT salnReports                                    #
# ---------------------------------------------------------------------------- #
@salnReports.route('print/<emp_id>/<filing_date>/<filing_type>', methods=['POST', 'GET'])
@login_required
def print_salnReports(emp_id, filing_date, filing_type):
    # formdata  = json.loads(request.data)
    template = os.path.join(current_app.root_path, 'static/templates', 'salnReports_Form.docx')   

    document = from_template(template, emp_id, filing_date, filing_type)
    document.seek(0)
    
    return send_file(
        document, mimetype='application/vnd.openxmlformats-'
        'officedocument.wordprocessingml.document', as_attachment=True,
        attachment_filename='salnReports.docx')

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

    # Sort children_list in descending order based on child's age
    # children_list = sorted(children_list, key=lambda x: x.childAge, reverse=True)

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

    if spouse is not None:
        if spouse.fb_deceased == "unchecked":
            user_profile_dict['spouse_deceased'] = "unchecked"
        elif spouse.fb_deceased == "checked":
            user_profile_dict['spouse_deceased'] = "checked"

        if spouse.fb_abroad == "unchecked":
            user_profile_dict['spouse_abroad'] = "unchecked"
        elif spouse.fb_abroad == "checked":
            user_profile_dict['spouse_abroad'] = "checked"
    else:
        user_profile_dict['spouse_deceased'] = "unchecked"
        user_profile_dict['spouse_abroad'] = "unchecked"


    spouse_govt_issued_id_date_issued_date_obj = datetime.datetime.strptime(spouse.fb_date_issued, "%Y-%m-%d").date() if spouse and spouse.fb_date_issued != "" and spouse.fb_date_issued is not None else "N/A"

    user_profile_dict['spouse_govt_issued_id_date_issued'] = spouse_govt_issued_id_date_issued_date_obj.strftime("%B %d, %Y") if spouse and spouse.fb_date_issued != "" and spouse.fb_date_issued is not None else "N/A"

    user_profile_dict["checkmark"] = "✓"

    date_object = datetime.datetime.strptime(filing_date, "%Y-%m-%d")

    # Format the datetime object as "Month Day, Year"
    formatted_date = date_object.strftime("%B %d, %Y")

    user_profile_dict["filing_date"] = formatted_date
    user_profile_dict["filing_type"] = filing_type
    user_profile_dict["children_list"] = sorted(children_list, key=lambda x: x.fb_date_of_birth, reverse=False)

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
        total_outstanding_balance = sum(outstanding_balances) if sum(outstanding_balances) > 0 else 0.00
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
        total_acquisition_cost = sum(acquisition_costs) if sum(acquisition_costs) > 0 else 0.00
        formatted_total_acquisition_cost = "{:,.2f}".format(total_acquisition_cost) if sum(acquisition_costs) > 0 else None
    else:
        formatted_total_acquisition_cost = 0
        total_acquisition_cost = 0
    
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
        total_acquisition_cost = sum(acquisition_costs) if sum(acquisition_costs) > 0 else 0.00
        formatted_total_acquisition_cost = "{:,.2f}".format(total_acquisition_cost) if sum(acquisition_costs) > 0 else None
    else:
        formatted_total_acquisition_cost = None
        total_acquisition_cost = 0.00
    
    # return formatted_total_acquisition_cost
    return total_acquisition_cost

# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                     get data                                 #
# ---------------------------------------------------------------------------- #
@salnReports.route('get-data', methods=['POST', 'GET'])
@login_required
def get_data():
    user_profiles = User.query.all()

    user_list = []

    for user_profile in user_profiles:
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
            rg_list.append(rg)

        user_profile.user_relative_in_government = rg_list

        user_profile_dict = UserSchema().dump(user_profile)
        user_list.append(user_profile_dict)

    return jsonify(user_list)
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                     get data                                 #
# ---------------------------------------------------------------------------- #
@salnReports.route('get-data-test', methods=['POST', 'GET'])
@login_required
def get_data_test():
    # Define aliases for the subqueries
    rp_total = db.aliased(func.coalesce(Real_Property.rp_acquisition_cost, 0), name='rp_total')
    pp_total = db.aliased(func.coalesce(Personal_Property.pp_acquisition_cost, 0), name='pp_total')
    lia_total = db.aliased(func.coalesce(Liability.liability_outstanding_balance, 0), name='lia_total')

    user_query = db.session.query(
        User.id,
        User.employee_id,
        User.last_name,
        User.first_name,
        User.name_extn,
        User.middle_name,
        User.tin,
        User.position_title,
        User.employment_status,
        User.salary_grade,
        User.job_grade,
        rp_total.with_labels().label('rp_total'),
        pp_total.with_labels().label('pp_total'),
        lia_total.with_labels().label('lia_total')
    ).outerjoin(
        rp_total, User.id == rp_total.columns.user_id
    ).outerjoin(
        pp_total, User.id == pp_total.columns.user_id
    ).outerjoin(
        lia_total, User.id == lia_total.columns.user_id
    ).filter(User.status_remarks == 'ACTIVE').all()

    result = []

    for user_data in user_query:
        user_dict = dict(zip(user_query.keys(), user_data))
        result.append(user_dict)

    return jsonify(result)

# ---------------------------------------------------------------------------- #
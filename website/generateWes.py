from io import BytesIO
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from flask_login import current_user, login_required

from flask import request, jsonify

from sqlalchemy import desc
from .models import Work_Experience
from .models import WorkExperienceSchema
from .models import User
from . import db
from datetime import datetime, date
from .myhelper import format_mydatetime
import json

def get_context(id):
    """ You can generate your context separately since you may deal with a lot 
        of documents. You can carry out computations, etc in here and make the
        context look like the sample below.
    """

    work_exp_schema = WorkExperienceSchema(many=True)

    get_we = Work_Experience.query.filter_by(user_id = id).order_by(desc(Work_Experience.date_from)).all()
    user = db.session.query(User).get(id)
    user_profile = user
    my_rows = json.loads(jsonify(row_contents=work_exp_schema.dump(get_we)).get_data(True))
    #my_rows = jsonify(row_contents=work_exp_schema.dump(get_we)).get_data(True)

    middle_name = user_profile.middle_name[:1]+"." if user_profile.middle_name != "" or user_profile.middle_name is not None or user_profile.middle_name != "N/A" else ""
    name_extn = user_profile.name_extn if user_profile.name_extn != "" and user_profile.name_extn is not None and user_profile.name_extn != "N/A" else ""

    my_rows['full_name'] = user_profile.first_name + " " + middle_name + " " + user_profile.last_name + " " + name_extn


    for idx, item in enumerate(my_rows["row_contents"]):
        dt_obj = datetime.strptime(item['date_from'],'%Y-%m-%d')
        new_value = datetime.strftime(dt_obj, "%B %d, %Y")

        if item['date_to'] != 'PRESENT':
            dt_obj_date_to = datetime.strptime(item['date_to'],'%Y-%m-%d')
            new_value_date_to = datetime.strftime(dt_obj_date_to, "%B %d, %Y")
            my_rows["row_contents"][idx]['date_to'] = new_value_date_to
        else:
            my_rows["row_contents"][idx]['date_to'] = item['date_to']

        # print("NEW VAL: ", new_value)

        my_rows["row_contents"][idx]['date_from'] = new_value

    return my_rows




def from_template(template, emp_id):
    target_file = BytesIO()

    template = DocxTemplate(template)
    context = get_context(emp_id)  # gets the context used to render the document

    target_file = BytesIO()
    template.render(context)
    template.save(target_file)

    return target_file
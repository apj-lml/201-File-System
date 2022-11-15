from io import BytesIO
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage


from flask import request, jsonify

from sqlalchemy import desc
from .models import Work_Experience
from . import db
from datetime import datetime, date
from .myhelper import format_mydatetime
import json

def get_context(id):
    """ You can generate your context separately since you may deal with a lot 
        of documents. You can carry out computations, etc in here and make the
        context look like the sample below.
    """

    get_we = Work_Experience.query.filter_by(user_id = id).all()
    column_keys = Work_Experience.__table__.columns.keys()
# Temporary dictionary to keep the return value from table
    rows_dic_temp = {}
    rows_dic = []
# Iterate through the returned output data set
    for row in get_we:
        for col in column_keys:
            rows_dic_temp[col] = getattr(row, col)
        rows_dic.append(rows_dic_temp)
        rows_dic_temp= {}

    aDict = {}
    temp_dict = {}
    my_list = []

    print('ROWSDIC: ', rows_dic)

    for row in rows_dic:
        for key, value in row.items():
            temp_dict[key] = value if isinstance(value, int) or value == None else value.title() 
            if key == 'date_from' or key == 'date_to':
                if value != "PRESENT":
                    dt_obj = datetime.strptime(value,'%Y-%m-%d')
                    value = datetime.strftime(dt_obj, "%B %d, %Y")
                    temp_dict[key] = value
                else:
                    temp_dict[key] = value if isinstance(value, int) or value == None else value.title() 

        my_list.append(temp_dict)

    aDict['row_contents'] = my_list
    
    aDict['full_name'] = 'Aljohn P. Jacinto'
    aDict['date_now']  = date.today().strftime("%B %d, %Y")
        
    print("ADICT: ",aDict)

    return aDict


def from_template(template, emp_id):
    target_file = BytesIO()

    template = DocxTemplate(template)
    context = get_context(emp_id)  # gets the context used to render the document

    target_file = BytesIO()
    template.render(context)
    template.save(target_file)

    return target_file
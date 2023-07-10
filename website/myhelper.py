from datetime import datetime
import json
import uuid
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask.json import JSONEncoder


#ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename, allowed_ext={'pdf'}):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext

def my_random_string(string_length=4):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    #random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.

def format_mydatetime(value):
    if(value != "PRESENT" and value != "Present"):
        mydatetime = datetime.strptime(value, '%Y-%m-%d')
    else:
        mydatetime = ""
    return mydatetime

def join_to_nested_dict(join_result):
    """
    Takes a sqlalchemy result and converts it to a dictionary.
    The models must use the dataclass decorator.
    Adds results to the right in a key named after the table the right item is contained in.
    :param List[Tuple[dataclass]] join_result:
    :return dict:
    """
    if len(join_result) == 0:
        return join_result

    # couldn't be the result of a join without two entries on each row
    assert(len(join_result[0]) >= 2)

    right_name = join_result[0][1].__tablename__
    # if there are multiple joins recurse on sub joins
    if len(join_result[0]) > 2:
        right = join_to_nested_dict([res[1:] for res in join_result])
    elif len(join_result[0]) == 2:
        right = [
            json.loads(json.dumps(row[1], cls=JSONEncoder))
            for row in join_result if row[1] is not None
        ]
    right_items = {item['id']: item for item in right}

    items = {}
    for row in join_result:
        # in the case of a right outer join
        if row[0] is None:
            continue
        if row[0].id not in items:
            items[row[0].id] = json.loads(json.dumps(row[0], cls=JSONEncoder))
        # in the case of a left outer join
        if row[1] is None:
            continue
        if right_name not in items[row[0].id]:
            items[row[0].id][right_name] = []
        items[row[0].id][right_name].append(right_items[row[1].id])
    return list(items.values())

def ConvertToDict(lst):
    keys = lst[::2]  # slice the list to get keys
    values = lst[1::2]  # slice the list to get values
    res_dict = {keys[i]: values[i] for i in range(len(keys))}
    return res_dict
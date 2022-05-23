from datetime import datetime
import uuid



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
    if(value != "PRESENT"):
        mydatetime = datetime.strptime(value, '%Y-%m-%d')
    else:
        mydatetime = ""
    return mydatetime




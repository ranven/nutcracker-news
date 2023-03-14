import re
from app import app
import services.inputs as inputs

def validate_password(pw):
    if re.fullmatch(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])[A-Za-z\d]{6,128}$", pw) is None:
        return False
    else:
        return True
        
def validate_length(str, type):
    attributes = inputs.attributes.get(type)
    if len(attributes) > 0:
        if len(str) >= attributes["min"] and len(str) <= attributes["max"]:
            return True
    else:
        return False
    
import secrets
import string
from datetime import date

def generate_ref_number():
    length = 4
    letters = string.ascii_uppercase + string.digits
    result_str = ''.join(secrets.choice(letters) for i in range(length))
    today = date.today()
    d1 = today.strftime("%d%m%y")
    return f'INC-{d1}-{result_str}'

def generate_rep_ref_number():
    length = 4
    letters = string.ascii_uppercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    today = date.today()
    d1 = today.strftime("%d%m%y")
    return f'INR-{d1}-{result_str}'

def generate_verification_code():
    length = 4
    letters = string.ascii_uppercase+ string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return f'{result_str}'

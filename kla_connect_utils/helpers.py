import random
import string
from datetime import date

def generate_ref_number():
    length = 4
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    today = date.today()
    d1 = today.strftime("%d%m%y")
    return f'INC-{d1}-{result_str}'

def generate_rep_ref_number():
    length = 4
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    today = date.today()
    d1 = today.strftime("%d%m%y")
    return f'INR-{d1}-{result_str}'
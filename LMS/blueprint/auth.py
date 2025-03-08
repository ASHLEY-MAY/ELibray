from flask import Blueprint, render_template
from flask_mysqldb import MySQLdb
from werkzeug.security import check_password_hash, generate_password_hash
import re

def validate_fn(first_name, max_length=50, min_length=3):
    return (bool(re.match(r"^[a-zA-Z]", first_name)) and 
            len(first_name) <= max_length and 
            len(first_name) >= min_length)

def validate_mn(middle_name, max_length=50, min_length=3):
    return (bool(re.match(r"^[a-zA-Z]", middle_name)) and 
            len(middle_name) <= max_length and 
            len(middle_name) >= min_length)

def validate_ln(last_name, max_length=50, min_length=3):
    return (bool(re.match(r"^[a-zA-Z]", last_name)) and 
            len(last_name) <= max_length and 
            len(last_name) >= min_length)

def validate_email(email, max_length=50, min_length=3):
    return (bool(re.match(r"^[a-zA-Z]", email)) and 
            len(email) <= max_length and 
            len(email) >= min_length)

def validate_pass(password, max_length=50, min_length=3):
    if len(password) < min_length or len(password) > max_length:
        return False
    if (re.search(r"[A-Z]", password) and
        re.search(r"\d", password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
        return True
    return False

auth = Blueprint('auth', __name__, template_folder='blueprint/template', static_folder='blueprint/static')

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')

@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/forget')
def forget():
    return render_template('forget.html')


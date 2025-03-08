from flask import Blueprint, render_template, request, current_app, session, flash
from flask_mysqldb import MySQLdb
from werkzeug.security import check_password_hash, generate_password_hash
import re

def validate_fn(first_name, min_length=3):
    if not re.match(r"^[a-zA-Z]+$", first_name):
        flash('First name must contain letters only.')
        return False
    if len(first_name) < min_length:
        flash(f'First name must be at least {min_length} characters long.', 'errorfn')
        return False
    return True

def validate_mn(middle_name, min_length=0):
    if middle_name and not re.match(r"^[a-zA-Z]+$", middle_name):
        flash('Middle name must contain letters only.')
        return False
    if len(middle_name) < min_length:
        flash(f'Middle name must be at least {min_length} characters long.', 'errormn')
        return False
    return True

def validate_ln(last_name, min_length=3):
    if not re.match(r"^[a-zA-Z]+$", last_name):
        flash('Last name must contain letters only.')
        return False
    if len(last_name) < min_length:
        flash(f'Last name must be at least {min_length} characters long.', 'errorln')
        return False
    return True

def validate_email(email, min_length=3):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_regex, email):
        flash('Invalid email format.', 'errorfn')
        return False
    if len(email) < min_length:
        flash(f'Email must be at least {min_length} characters long.', 'erroremail')
        return False
    return True

def validate_pass(password, min_length=3):
    if len(password) < min_length:
        flash(f'Password must be at least {min_length} characters long.', 'errorpass')
        return False
    if (re.search(r"[A-Z]", password) or
        re.search(r"\d", password) or
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
        return True
    flash('Password must contain at one of the following: at least one uppercase letter, one number, or one special character.', 'errorpass')
    return False

auth = Blueprint('auth', __name__, template_folder='blueprint/template', static_folder='blueprint/static')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'log' in session:
        return render_template('home.html')
    
    if request.method == 'POST':
        username = request.form['user_id']
        password = request.form['password']
        
        admin_user = "ELUA101"
        admin_pass = "njsamiacortezanoashley"

        cursor = current_app.mysql.connection.cursor()
        cursor.execute("SELECT * FROM user_account WHERE user_id = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        try:
            if username == admin_user and password == admin_pass:
                session['log'] = True
                session['username'] = username
                session['user_id'] = username  # Assuming admin user_id is the same as username
                return render_template('admin/admin_dashboard.html') 
            if user and check_password_hash(user[2], password):
                session['log'] = True
                session['username'] = username
                session['user_id'] = user[0]
                return render_template('home.html')
            else:
                flash('Invalid Credentials', 'error')
                return render_template('login.html')
        except Exception as e:
                current_app.mysql.connection.rollback()
                flash(f'An unexpected error occurred: {str(e)}', 'error')
        finally:
            cursor.close()

    return render_template('login.html')

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        fn = request.form['first_name']
        mn = request.form.get('middle_name', '')
        ln = request.form['last_name']
        email = request.form['email']
        gender = request.form['gender']
        birthday = request.form['birthday']
        password = request.form['password']
        repassword = request.form['repassword']
        hashed_password = generate_password_hash(password)

        cursor = current_app.mysql.connection.cursor()

        # Check if the email already exists
        cursor.execute('SELECT * FROM user_profile WHERE email = %s', (email,))
        existing_email = cursor.fetchone()

        if existing_email:
            flash('Email is already in use! Try another one.', 'error')
        else:
            # Validate user input
            if (validate_fn(fn) and validate_mn(mn) and validate_ln(ln) and
                validate_email(email) and validate_pass(password) and
                password == repassword):  # Fixed the condition here

                try:
                    # Count existing users to generate a new user ID
                    cursor.execute('SELECT COUNT(*) FROM USER_PROFILE')
                    user_count = cursor.fetchone()[0]

                    # Generate a new user ID
                    new_user_id = f'ELU-{str(user_count + 1).zfill(3)}'

                    # Insert the new user into USER_PROFILE
                    cursor.execute('''
                        INSERT INTO USER_PROFILE (user_id, first_name, middle_name, last_name, email, gender, birthday)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (new_user_id, fn, mn, ln, email, gender, birthday))

                    # Insert the new user into USER_ACCOUNT
                    cursor.execute('''
                        INSERT INTO USER_ACCOUNT (user_id, password)
                        VALUES (%s, %s)
                    ''', (new_user_id, hashed_password))

                    current_app.mysql.connection.commit()
                    flash('Registered successfully! Please login.', 'success')
                    return render_template('login.html')
                except MySQLdb.IntegrityError:
                    current_app.mysql.connection.rollback() 
                    flash('An error occurred while registering. Please try again!', 'error')
                except Exception as e:
                    current_app.mysql.connection.rollback()
                    flash(f'An unexpected error occurred: {str(e)}', 'error')
                finally:
                    cursor.close()
            else:
                flash('Please ensure all fields are valid and passwords match.', 'error')

    return render_template('register.html')

@auth.route('/forget')
def forget():
    return render_template('forget.html')

@auth.route('/base')
def base():
    return render_template('base.html')


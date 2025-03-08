from flask import Flask
from flask_mysqldb import MySQL


mysql = MySQL()

def create_app():
    app = Flask(__name__, template_folder='template', static_folder='static')
    
    app.config['SECRET_KEY'] = 'ElibraryNamin'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'elibrary_db'

    mysql.init_app(app)

    app.mysql = mysql

    with app.app_context():
        try:
            db = mysql.connection
            cursor = db.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("Database connection is successful!" if result else "Database connection failed!")
            cursor.close()
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    from .views import views
    from .auth import auth
    from .admin import admin
    from .user import user




    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(user, url_prefix='/user')


    return app



'''
 USE elibrary_db;
 
 CREATE TABLE USER_PROFILE(
     id INT AUTO_INCREMENT PRIMARY KEY,
     user_id VARCHAR(10) NOT NULL UNIQUE,
     first_name VARCHAR(50) NOT NULL,
     middle_name VARCHAR(50),
     last_name VARCHAR(50) NOT NULL,
     email VARCHAR(100) NOT NULL UNIQUE,
     sex ENUM('male', 'demale', 'others', 'prefer not to say') NOT NULL,
     birthday DATE NOT NULL,
     full_name VARCHAR(150) AS (CONCAT(first_name, '', middle_name, '', last_name)) STORED
    );

CREATE TABLE USER_ACCOUNT (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(10) NOT NULL UNIQUE,
    password VARCHAR(350) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES USER_PROFILE(user_id) ON DELETE CASCADE
);
 
DELIMITER //

CREATE PROCEDURE AddUser  (
    IN p_password VARCHAR(50),
    IN p_first_name VARCHAR(50),
    IN p_middle_name VARCHAR(50),
    IN p_last_name VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_sex ENUM('male', 'female', 'others', 'prefer not to say'),
    IN p_birthday DATE
)
BEGIN
    DECLARE new_user_id VARCHAR(10);
    DECLARE user_count INT;

    SELECT COUNT(*) INTO user_count FROM USER_PROFILE;

    SET new_user_id = CONCAT('ELU-', LPAD(user_count + 1, 3, '0'));

<<<<<<< HEAD
    INSERT INTO USER_PROFILE (user_id, first_name, middle_name, last_name, email, age, birthday)
=======
    INSERT INTO USER_PROFILE (user_id, first_name, middle_name, last_name, email, sex, birthday)
>>>>>>> 6589c5f2e976b08e038f850fa79118d2d48754aa
    VALUES (new_user_id, p_first_name, p_middle_name, p_last_name, p_email, p_sex, p_birthday);

    INSERT INTO USER_ACCOUNT (user_id, password)
    VALUES (new_user_id, p_password);
END //

DELIMITER ;
'''

"""
DELIMITER //

CREATE PROCEDURE age(IN user_input INT)
BEGIN

DECLARE userBirthday DATE;
DECLARE userAge INT;

SELECT birthday INTO userBirthday FROM users WHERE id = userId;

    SET userAge = YEAR(CURDATE()) - YEAR(userBirthday) - 
                  (DATE_FORMAT(CURDATE(), '%m%d') < DATE_FORMAT(userBirthday, '%m%d'));
    
    SELECT userAge AS Age;

END//
"""

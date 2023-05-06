from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    DB = 'billing'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.phone_number = data['phone_number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.incomes = []
        self.bills = []
    @staticmethod
    def validate_registration(user):
        is_valid = True
        query = " SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.DB).query_db(query, user)
        allowed = re.compile("^[A-Za-z ]*$")
        phone_allowed = re.compile("^[0-9 ]*$")
        check_first = bool(re.match(allowed, user['first_name']))
        check_last = bool(re.match(allowed, user['last_name']))
        check_number = bool(re.match(phone_allowed, user['phone_number']))
        false_pass = " "
        # ------
        if ((len(user['first_name']) - (user['first_name'].count(' ')) == 0) and (len(user['last_name']) - (user['last_name'].count(' ')) == 0)
            and (len(user['email']) - (user['email'].count(' ')) == 0) and (len(user['password']) == 0)) and (len(user['phone_number']) - (user['phone_number'].count(' ')) == 0):
            flash("All fields required")
            is_valid = False
# ------- FIRST NAME VALIDATION

        elif len(user['first_name']) - (user['first_name'].count(' ')) == 0:
            flash("First name is required")
            is_valid = False
        elif len(user['first_name']) - (user['first_name'].count(' ')) < 2:
            flash("First name must be atleast 2 characters")
            is_valid = False
        elif len(user['first_name']) - (user['first_name'].count(' ')) > 100:
            flash("First name must less than 255 characters")
            is_valid = False
        elif check_first == False:
            flash("First name must only contains letters")
            is_valid = False
# ------- LAST NAME VALIDATION

        elif len(user['last_name']) - (user['last_name'].count(' ')) == 0:
            flash("Last name is required")
            is_valid = False
        elif len(user['last_name']) - (user['last_name'].count(' ')) < 2:
            flash("Last name must be atleast 2 characters")
            is_valid = False
        elif len(user['last_name']) - (user['last_name'].count(' ')) > 100:
            flash("Last name must less than 255 characters")
            is_valid = False
        elif check_last == False:
            flash("Last name must only contain letters")
            is_valid = False
# ------- EMAIL VALIDATION

        elif len(results) > 0:
            flash("Email is already in use. Please try another email")
            is_valid = False
        elif len(user['email']) - (user['email'].count(' ')) == 0:
            flash("Email is required")
            is_valid = False
        elif len(user['last_name']) - (user['last_name'].count(' ')) > 100:
            flash("Last name must less than 255 characters")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email format")
            is_valid = False
# ------- PASSWORD VALIDATION

        elif len(user['password']) == 0:
            flash("Password is required")
            is_valid = False
        elif len(user['password']) < 8:
            flash("Password must contain atleast 8 characters")
            is_valid = False
        elif len(user['password']) > 100:
            flash("Password must be less than 100 characters")
            is_valid = False
# ------- PHONE NUMBER VALIDATION

        elif len(user['phone_number']) - (user['phone_number'].count(' ')) == 0:
            flash("Phone number is required")
            is_valid = False
        elif len(user['phone_number']) < 10:
            flash("Phone number must be 10 characters long")
            is_valid = False
        elif len(user['phone_number']) > 10:
            flash("Phone number must be 10 characters long")
            is_valid = False
        elif check_number == False:
            flash("Phone number must only consist of digits")
            is_valid = False
        return is_valid
    @staticmethod
    def validate_login(user):
        is_valid = True
        existing_user = User.get_with_email(user)
        # ------
        if (len(user['email']) - user['email'].count(' ') == 0) and (len(user['password']) - user['password'].count(' ') == 0):
            flash("All fields required")
            is_valid = False
        elif len(user['email']) - user['email'].count(' ') == 0:
            flash("Email is required")
            is_valid = False
        elif not existing_user:
            flash("No account associated with this email")
            is_valid = False
        elif len(user['password']) - user['password'].count(' ') == 0:
            flash("Password is required")
            is_valid = False
        elif not bcrypt.check_password_hash(existing_user.password, user['password']):
            flash("Invalid Email or Password")
            is_valid = False
        return is_valid
    @classmethod
    def add_user(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password, phone_number, created_at, updated_at)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(phone_number)s, NOW(), NOW());"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def get_with_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    @classmethod
    def get_with_id(cls, data):
        query = """SELECT * FROM users
                WHERE id = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

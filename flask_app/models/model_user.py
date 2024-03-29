from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

DATABASE = "users_and_listings"

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


 
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters", "error_users_first_name")
            is_valid = False

        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters", "error_users_last_name")
            is_valid = False
 
        # print(user['email'])
        if len(user['email']) < 5:
            flash("Email must be at least 5 characters", "error_users_email")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address", "error_users_email")
            is_valid = False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "error_users_password")

        if user['password'] != user['confirm_password']:
            flash("Passwords do not match", "error_users_password")
            is_valid = False

        def email_unique(email):
            is_valid = True
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(DATABASE).query_db(query, {'email':email})
            if len(results) > 0:
                is_valid = False
            return is_valid

        if not email_unique(user['email']):
            flash("This email is already in use", "error_users_email")
            is_valid = False
        return is_valid
 





#CRUD!!
#C
    @classmethod
    def write_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    


    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, {'id':id})
        one_user = cls(results[0])
        return one_user


    @classmethod
    def login(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password=data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def save(cls, data):
        query = ''' INSERT INTO users (username,email,password)
        VALUES (%(username)s,%(email)s,%(password)s);
        '''
        results= connectToMySQL('project').query_db(query,data)
        return results
    


    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['username']) <= 1:
            flash("Username must be more than one character!")
            is_valid = False
        if len(data['email']) == 0:
            flash("Email is required!")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False
        query = "SELECT * FROM users WHERE email=%(email)s"
        results = connectToMySQL('project').query_db(query, data)
        if len(results) != 0:
            flash("Email is already in use!")
            is_valid = False
        if len(data['password']) == 0:
            flash("Password is required!")
            is_valid = False

        return is_valid
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results= connectToMySQL('project').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

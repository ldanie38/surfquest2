from flask import Flask,render_template,request,session,redirect
from flask_app import app
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from datetime import datetime
from flask import flash
import os
from pprint import pprint


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['POST'])
def register():
        if not User.validate_user(request.form):
            return redirect('/')
    #pw_hash is a variable
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
        "username": request.form["username"],
        "email":request.form["email"],
        "password":pw_hash
    
    }


        user_id=User.save(data)
        session['user_id'] = user_id
        print(user_id)
        return redirect('/home')
    

@app.route('/login_user',methods=["POST"])
def login_user():
        
    user_in_db= User.get_by_email(request.form)
    

    if not user_in_db:
        flash('Invalid email/password')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Ivalid email/password !!!!')
        return redirect('/')
    session['user_id'] = user_in_db.id
    

    return redirect ('/home')
    
from flask import Flask,render_template,request,session,redirect
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.latest_model import LatestPost
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
    latest_posts = LatestPost.get_all()[:3]      # grab the 3 newest
    username     = session.get('username')
    return render_template('home.html',latest_posts=latest_posts,username=username)


@app.route('/register', methods=['POST'])
def register():
    """Handle user registration with validation and duplicate checks."""

    if not User.validate_user(request.form):
        return redirect('/')

    # Check for existing username and email
    existing_user = User.get_by_username({"username": request.form["username"]})
    existing_email = User.get_by_email({"email": request.form["email"]})

    if existing_user:
        flash("Username is already taken. Please choose another.")
        return redirect('/')

    if existing_email:
        flash("Email is already registered. Try logging in or use another email.")
        return redirect('/')

    # Hash password securely
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        "username": request.form["username"],
        "email": request.form["email"],
        "password": pw_hash
    }
    
    

    user_id = User.save(data)
    session['user_id'] = user_id
    session['username'] = request.form["username"]  # Store username in session
    session['is_admin'] = False

    flash("Account created successfully!")
    return redirect('/home')


 

    

@app.route('/login_user', methods=["POST"])
def login_user():
    # Retrieve user from DB using the form data
    user_in_db = User.get_by_email(request.form)
    
    if not user_in_db:
        flash('Invalid email/password')
        return redirect('/')
    
    # Check if the password hash matches the form password
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid email/password')
        return redirect('/')
  
    # Set session variables for the logged in user
    session['user_id'] = user_in_db.id
    session['username'] = user_in_db.username # Store the username from the DB
    session['is_admin']  = user_in_db.is_admin 
    
    return redirect('/home')



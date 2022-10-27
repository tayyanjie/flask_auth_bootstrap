from curses.ascii import isdigit
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/login', methods=['POST'])
def login_post():
    # Retrieve information from login form
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    if not email:
        flash('Please input an email address!')
        return redirect(url_for('auth.login')) 

    if not password:
        flash('Please input a password!')
        return redirect(url_for('auth.login')) 
    
    # Find the user with the email
    user = User.query.filter_by(email=email).first()

    # If user does not exist or password incorrect, tell user to try again
    if not user or not check_password_hash(user.password, password):
        flash('Email does not exist or incorrect password!')
        return redirect(url_for('auth.login')) 
    
    # Logs the user in
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/signup', methods=['POST'])
def signup_post():
    # Retrieve user data from form submitted
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # Checks whether user exists by looking at email address
    user = User.query.filter_by(email=email).first()

    # If user already exists, ask user to signup with new email
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    
    # Check password met requirements
    # Check password at least 8 char
    if len(password) < 8:
        flash('Password must have at least 8 characters!')
        return redirect(url_for('auth.signup'))
    
    lower_flag, upper_flag, has_alpha, has_digit = False, False, False, False

    for char in password:
        if char.isalpha():
            has_alpha = True
        if char.isdigit():
            has_digit = True
        if char.islower():
            lower_flag = True
        if char.isupper():
            upper_flag = True
        if lower_flag and upper_flag and has_alpha and has_digit:
            break
    if not (lower_flag and upper_flag and has_alpha and has_digit):
        flash("Password must have upper and lowercase characters and have both numbers and alphabets!")
        return redirect(url_for('auth.signup'))
    
    # Otherwise add user to database
    new_user = User(email=email, name=name, 
                    password=generate_password_hash(password, method='sha256'))

    # Add new user
    db.session.add(new_user)
    db.session.commit()

    return render_template('signup_post.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
#redirect and url_for are for redirecting the user to certain webpages
#werkzeug puts a hash on a password so we never have to read a password
#import User so we can create users from sign-in
#flash is to flash messages
#auth.py is basically the backend for the verification pages 
#and manages the user's login
auth = Blueprint('auth', __name__)
#blueprint means it has a bunch of routes inside of it

#defining the login page
#this receives GET and POST
@auth.route('/login', methods=['GET','POST'])
def login():
    #if there's a post from submit button, check if email and password match
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #search the table user by email
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Incorrect email', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

####note to self, adding food page with adding food front end
@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    #if request method is a post, set a bunch of variables
    #to the fields
    if request.method =='POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #this is just to check if the info submitted is all there
        #and the passwords match
        #we must first check if the user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account already exists with this email', category='error')
        elif len(email) < 1:
            flash('Please fill in email', category='error')
        elif len(first_name) < 1:
            flash('Please fill in first name', category='error')
        elif len(password1) < 1:
            flash ('Please create a password', category='error')
        elif password1 != password2:
            flash('Passwords must match', category='error')
        else:
            #create user, and redirect them to home page
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created. Welcome', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

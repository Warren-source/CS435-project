from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Buyer, Seller, Location
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
    #if there's a post from submit button, check if user name and password match
    if request.method == 'POST':
        user_name = request.form.get('userName')
        password = request.form.get('password')
        #search the table user by user name
        user = User.query.filter_by(user_name=user_name).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Incorrect user name', category='error')

    return render_template("login.html", user=current_user)

#this logs the user out
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#this displays and tskes posts from the sign up page
@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    #if request method is a post, set a bunch of variables
    #to take from each of the fields
    if request.method =='POST':
        user_name = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        address = request.form.get('address')
        zipcode = request.form.get('zipcode')
        phone = request.form.get('phone')
        card = request.form.get('card')
        license = request.form.get('license')
        town = request.form.get('town')
        state = request.form.get('state')
        #this is just to check if the info submitted is all there
        #and the passwords match
        #we must first check if the user already exists
        user = User.query.filter_by(user_name=user_name).first()

        #and this is just error checking
        if user:
            flash('This username is already taken', category='error')
        elif len(user_name) < 1:
            flash('Please fill in user name', category='error')
        elif len(password1) < 1:
            flash ('Please create a password', category='error')
        elif password1 != password2:
            flash('Passwords must match', category='error')
        elif len(address) < 5:
            flash('Please give an address', category='error')
        elif len(town) < 1:
            flash('Please give a town', category='error')
        elif len(state) < 1:
            flash('Please give a state', category='error')
        elif len(zipcode) < 5:
            flash('Please give a zip code', category='error')
        elif len(phone) < 10:
            flash('Please give a valid phone number', category='error')
        else:
            #create user, and redirect them to home page
            new_user = User(user_name=user_name, password=generate_password_hash(password1, method='sha256'),
                            address=address, zipcode=zipcode, phone=phone)
            db.session.add(new_user)
            db.session.commit()
            #now we have to query to see if the zipcode already exists in location table
            location_exists = Location.query.filter_by(zipcode=zipcode).first()
            if(location_exists == None):
                new_location = Location(town=town, state=state, zipcode=zipcode)
                db.session.add(new_location)
                db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created. Welcome', category='success')
            #give them a place in the buyer and/or seller table if they fill out
            #the proper forms 
            if len(card) > 0:
                new_buyer = Buyer(card=card, user_name=current_user.user_name)
                db.session.add(new_buyer)
                db.session.commit()
                flash('Your account has buyer priviledges', category='success')
            if len(license) > 0:
                new_seller = Seller(license=license, user_name=current_user.user_name)
                db.session.add(new_seller)
                db.session.commit()
                flash('Your account has seller priviledges', category='success')

            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

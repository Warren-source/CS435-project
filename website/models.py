# this is where our databases are defined
from . import db  # import from website, the database
from flask_login import UserMixin  # this helps us login
from sqlalchemy.sql import func  # deals with date creation for us


class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(100))
    price = db.Column(db.String(30))
    #date = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String(600))
    expiration = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   

# define the User table
# id is used as the primary key and will always be different


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    address = db.Column(db.String(300)) #include town and state after
    zipcode = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    sellers = db.relationship('Seller')  # access user's items for sale
    
    #USE CURRENT_USER TO INPUT STUFF
    #oh shoot should only show what's in my current zip code too
    #or "in your area table"
    #also nrating, then if they do crazy number, have if check if it's btwn 1 and 5
    #maybe sold option for my items
    #also quantity for seller
    #note: make it impossible to see your own items in general items list
    #note, make buyer history and seller history, since that's what we'll display anyway
    #and just have username of the other guy, they don't need to know the guy's id
    

#this is where our databases are defined
from . import db #import from website, the database
from flask_login import UserMixin #this helps us login
from sqlalchemy.sql import func #deals with date creation for us

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(100))
    #date = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String(600))
    expiration = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#define the User table
#id is used as the primary key and will always be different
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    sellers = db.relationship('Seller')#access user's items for sale

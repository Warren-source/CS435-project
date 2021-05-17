# this is where our databases are defined
from . import db  # import from website, the database
from flask_login import UserMixin  # this helps us login
from sqlalchemy.sql import func  # deals with date creation for us



#every table has a foreign key that connects back to the user_name
#this defines a food item
#has a foreign key to the user table
#this one intentionally has an id column because a user
# should be able to sell multiple copies of the same item
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(100))
    price = db.Column(db.String(30))
    description = db.Column(db.String(600))
    expiration = db.Column(db.String(30))
    user_name = db.Column(db.String(100), db.ForeignKey('user.user_name'))
   

# defines the Buyer table, bascially just keeps track of user's credit/debit card
#has a foreign key to the user table  
class Buyer(db.Model):
    card = db.Column(db.String(70))
    user_name = db.Column(db.String(100), db.ForeignKey('user.user_name'), primary_key=True)

#defines seller table, just keeps track of user's health license number
#has a foreign key to the user table
class Seller(db.Model):
    license = db.Column(db.String(50))
    user_name = db.Column(db.String(100), db.ForeignKey('user.user_name'), primary_key=True)

#defines user table
# id is created by flask and automatically updates, 
# apparently for UserMixin, an id column is necessary, so it's here, but it's never used
# since I consider user_name to be the true primary key
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    address = db.Column(db.String(300))
    zipcode = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    seller = db.relationship('Seller')  # seller table
    buyer = db.relationship('Buyer')  # access user's credit/debit card
    items = db.relationship('Item') #accesss user's items for sale
    cart = db.relationship('Cart') #access user's cart
    location = db.relationship('Location') # link to zipcode's state and town

#simple table to keep track of zip codes and their towns and states
class Location(db.Model):
    town =  db.Column(db.String(100))
    state =  db.Column(db.String(100))
    zipcode = db.Column(db.Integer, db.ForeignKey('user.zipcode'), primary_key=True)

#defines cart table
#has a foreign key to the user table and item table
#so the owner of the cart is stored in user_name, but the seller
#of the item must be traced through the item_id
class Cart(db.Model):
    user_name = db.Column(db.String(100), db.ForeignKey('user.user_name'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))



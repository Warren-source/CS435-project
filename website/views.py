from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Item, User, Buyer, Seller, Cart
from . import db

views = Blueprint('views', __name__)
# blueprint means it has a bunch of routes inside of it

# this just supports all the pages that aren't related to security, like 
#sign up and login

#backend for the about page
@views.route('/about', methods=['GET'])
def about():
    return render_template("about.html", user=current_user)

#backend for the market page
#this will give back custom tables to display to the user using sql commands
#it will either give back the user's items they are selling and the market
#or the market with a specific food that they search for
@views.route('/market', methods=['GET', 'POST'])
@login_required
def market():
    if request.method == 'POST':
        food_item = request.form.get('searchfood')
        searchresults = db.session.execute('SELECT I.id, I.food, I.price, I.description, I.expiration, U.user_name, U.address, U.zipcode, U.phone, L.town, L.state FROM Location AS L JOIN User AS U JOIN Item AS I WHERE U.zipcode = L.zipcode AND I.user_name = U.user_name AND I.food = :val', {'val': food_item})
        return render_template("market.html", user=current_user, searchresults=searchresults)

    result = db.session.execute('SELECT I.id, I.food, I.price, I.description, I.expiration, U.user_name, U.address, U.zipcode, U.phone, L.town, L.state FROM Location AS L JOIN User AS U JOIN Item AS I WHERE U.zipcode = L.zipcode AND I.user_name = U.user_name')
    my_stuff = Item.query.filter_by(user_name=current_user.user_name)
    return render_template("market.html", user=current_user, seller=result, my_stuff=my_stuff)

#backend for the home page, where the user can put new items on the 
#market if they have a record in the seller's table, otherwise they are blocked
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        can_sell = Seller.query.filter_by(user_name=current_user.user_name).first()
        if(can_sell != None):
            food = request.form.get('food')
            price = request.form.get('price')
            description = request.form.get('description')
            expiration = request.form.get('expiration')


            if len(food) < 1:
                flash('please insert food', category='error')
            elif len(price) < 1:
                flash('please give a price', category='error')
            elif len(description) < 1:
                flash('please give a description', category='error')
            elif len(expiration) < 1:
                flash('please give an expiration date', category='error')
            
            else:
                new_item = Item(food=food, price=price, description=description,
                                    expiration=expiration, user_name=can_sell.user_name)
                db.session.add(new_item)
                db.session.commit()
                flash('Item added to market', category='success')
                return redirect(url_for('views.home'))
        else:
            flash('you don\'t have selling priveledges', category='error')

    # we always pass the current_user to the front end 
    # so we can check if authenticated when displaying link and stuff
    return render_template("home.html", user=current_user)

#backend for the buy page, or shopping cart page
#this just shows you your cart items in a similar way it's shown in the market
@views.route('/buy')
@login_required
def buy():
    my_cart = db.session.execute('SELECT I.id, I.food, I.price, U.user_name, U.phone, U.address, L.town, L.state FROM Cart AS C JOIN Item AS I JOIN User as U JOIN User as M JOIN Location As L WHERE C.user_name = M.user_name AND C.item_id = I.id AND I.user_name = U.user_name AND U.zipcode = L.zipcode AND M.user_name= :val', {'val': current_user.user_name})

    return render_template("buy.html", user=current_user, my_cart=my_cart)


#backend for purchase button
#this checks if you have a record in the buyer's table to see if you are allowed
#to buy, then it checks if they are buying their own item, then it lets
#them add it to their cart and redirects them to the buy page
@views.route('/purchase/<int:id>')
def purchase(id):

    can_buy = Buyer.query.filter_by(user_name=current_user.user_name).first()
    if(can_buy != None):
        #check if they are selling this. 
        #i have the item's id, so I can query and have the record
        
        my_item = Item.query.filter_by(id=id).first()
        if(my_item.user_name == current_user.user_name):
            flash('You can\'t buy your own item', category='error')
            return redirect(url_for('views.home'))

        new_cart = Cart(user_name=current_user.user_name, item_id=id)
        db.session.add(new_cart)
        db.session.commit()
        flash('Item added to cart', category='success')
        my_cart = db.session.execute('SELECT I.id, I.food, I.price, U.user_name, U.phone, U.address, L.town, L.state FROM Cart AS C JOIN Item AS I JOIN User as U JOIN User as M JOIN Location As L WHERE C.user_name = M.user_name AND C.item_id = I.id AND I.user_name = U.user_name AND U.zipcode = L.zipcode AND M.user_name= :val', {'val': current_user.user_name})

        return render_template("buy.html", user=current_user, my_cart=my_cart)
    else:
        flash('you don\'t have buying priveledges', category='error')
 
    result = db.session.execute('SELECT I.id, I.food, I.price, I.description, I.expiration, U.user_name, U.address, U.zipcode, U.phone, L.town, L.state FROM Location AS L JOIN User AS U JOIN Item AS I WHERE U.zipcode = L.zipcode AND I.user_name = U.user_name')
    my_stuff = Item.query.filter_by(user_name=current_user.user_name)
    return render_template("market.html", user=current_user, seller=result, my_stuff=my_stuff)

#backend for the checkout button
#this just deletes the item from the cart table and the item table
@views.route('/checkout/<int:id>')
def checkout(id):

    try:
        Item.query.filter_by(id=id).delete()
        db.session.commit()
        Cart.query.filter_by(item_id=id).delete()
        db.session.commit()
        flash('Checked out. Enjoy your product', category='success')
    except:
        flash('Item has already been checked out or deleted', category='error')
    return redirect(url_for('views.buy'))





#backend for the delete button
#this deletes the seller's item, and teh button is only displayed to the
#seller in the market page
@views.route('/delete/<int:id>')
def delete(id):

    try:
        Item.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Item deleted', category='success')
    except:
        flash('Item has already been checked out or deleted', category='error')
    try:
        Cart.query.filter_by(item_id=id).delete()
        db.session.commit()
        flash('Carts emptied of item', category='success')
    except:
        flash('No carts had this item', category='success')
    return redirect(url_for('views.home'))
    

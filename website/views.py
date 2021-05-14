from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Seller, User
from . import db
# views.py is basically for the links which the user can see
views = Blueprint('views', __name__)
# blueprint means it has a bunch of routes inside of it

# this just displays the market


@views.route('/about', methods=['GET'])
def about():
    return render_template("about.html", user=current_user)


@views.route('/market', methods=['GET', 'POST'])
@login_required
def market():
    if request.method == 'POST':
        food_item = request.form.get('searchfood')
        # don't do error checks, some boxes can be empty
        searchresults = db.session.execute(
            'SELECT S.id, S.food, S.price, S.description, S.expiration, U.user_name, U.address, U.zipcode, U.phone FROM Seller AS S JOIN User AS U WHERE U.id = S.user_id AND S.food = :val', {'val': food_item})
        # searchresults = Seller.query.filter_by(food=food_item) #okay so search results need to give full table
        return render_template("market.html", user=current_user, searchresults=searchresults)

    result = db.session.execute(
        'SELECT S.id, S.food, S.price, S.description, S.expiration, U.user_name, U.address, U.zipcode, U.phone FROM Seller AS S JOIN User AS U WHERE S.user_id = U.id')
    my_stuff = Seller.query.filter_by(user_id=current_user.id)
    return render_template("market.html", user=current_user, seller=result, my_stuff=my_stuff)

# views is Blueprint, route to home page


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
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
            new_seller = Seller(food=food, price=price, description=description,
                                expiration=expiration, user_id=current_user.id)
            db.session.add(new_seller)
            db.session.commit()
            flash('Item added', category='success')
            return redirect(url_for('views.home'))

    # so we can check if authenticated
    return render_template("home.html", user=current_user)


@views.route('/purchase/<int:id>')
def purchase(id):
    # here i could grab all the seller and buyer info
    seller_item = db.session.execute(
        'SELECT S.id, U.id, S.food, S.price, S.description, S.expiration, U.user_name, U.address, U.zipcode, U.phone FROM Seller AS S JOIN User AS U WHERE S.id = :val', {'val': id})
    # okay, this is so I can add the item to the transaction table
    # and removing it from the market table
    # I could manage that in the market backend b/c ill match seller id with
    # item's seller id and choose to not display it, along with user's own item
    # okay, so I take from this table the specific places and make them variables,
    # then add those variables into a database called transactions
    # i should at least have buyer's id, seller's id, item's id

    return render_template("buy.html", user=current_user, seller_item=seller_item)


@views.route('/delete/<int:id>')
def delete(id):
    seller_to_delete = Seller.query.get_or_404(id)

    if seller_to_delete.user_id == current_user.id:
        try:
            db.session.delete(seller_to_delete)
            db.session.commit()
            flash('Item deleted', category='success')
            return redirect(url_for('views.market'))
        except:
            flash('Technical problem with deleting item', category='error')
            return redirect(url_for('views.home'))
    else:
        flash('You can only delete your posted items', category='error')
        return redirect(url_for('views.market'))


@views.route('/items', methods=['GET', 'POST'])
@login_required
def items():
    if request.method == 'POST':
        food_item = request.form.get('searchfood')
        # don't do error checks, some boxes can be empty
        searchresults = db.session.execute(
            'SELECT S.id, S.food, S.price, S.description, S.expiration, U.user_name, U.address, U.zipcode, U.phone FROM Seller AS S JOIN User AS U WHERE U.id = S.user_id AND S.food = :val', {'val': food_item})
        # searchresults = Seller.query.filter_by(food=food_item) #okay so search results need to give full table
        return render_template("items.html", user=current_user, searchresults=searchresults)

    result = db.session.execute(
        'SELECT S.id, S.food, S.price, S.description, S.expiration, U.user_name, U.address, U.zipcode, U.phone FROM Seller AS S JOIN User AS U WHERE S.user_id = U.id')
    my_stuff = Seller.query.filter_by(user_id=current_user.id)
    return render_template("items.html", user=current_user, seller=result, my_stuff=my_stuff)

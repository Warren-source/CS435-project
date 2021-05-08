from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Seller
from . import db
# views.py is basically for the links which the user can see
views = Blueprint('views', __name__)
# blueprint means it has a bunch of routes inside of it

# this just displays the market


@views.route('/market', methods=['GET', 'POST'])
@login_required
def market():
    if request.method == 'POST':
        food_item = request.form.get('searchfood')
        # don't do error checks, some boxes can be empty
        searchresults = Seller.query.filter_by(food=food_item)
        return render_template("market.html", user=current_user, searchresults=searchresults)

    return render_template("market.html", user=current_user, seller=Seller.query.all())

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

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Seller
from . import db
#views.py is basically for the links which the user can see
views = Blueprint('views', __name__)
#blueprint means it has a bunch of routes inside of it

#views is Blueprint, route to home page
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        item = request.form.get('item')
        description = request.form.get('description')
        expiration = request.form.get('expiration')
        
        if len(item) < 1:
            flash('please insert item', category='error')
        elif len(description) < 1:
            flash('please give a description', category='error')
        elif len(expiration) < 1:
            flash('please give an expiration date', category='error')
        else:
            new_seller = Seller(item=item, description=description, expired=expiration, user_id=current_user.id)
            db.session.add(new_seller)
            db.session.commit()
            flash('Item added', category='success')
            return redirect(url_for('views.home'))
            
    return render_template("home.html", user=current_user)#so we can check if authenticated

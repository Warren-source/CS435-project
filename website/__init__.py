from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# this is the database, db
db = SQLAlchemy()
DB_NAME = "database.db"
# this file initializes all the other files. each file is started from here


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'slkdjfdkjfh'
    # this stores the database in the wbsite folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # now we initilize the database by giving it this app
    db.init_app(app)
    # from these files import the Blueprint
    from .views import views
    from .auth import auth

    # register these blueprints with flask
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Seller

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # look for user based on id

    return app

# find if database already exists, if not, create one


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

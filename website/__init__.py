from flask import Flask
from flask_session import Session
from flask_login import LoginManager
from dotenv import load_dotenv
import os
import redis


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')

    Session(app)

    from website.auth import auth
    from website.views import views

    app.register_blueprint(auth)
    app.register_blueprint(views)

    from website.models import db, User, TrackedFlights, PriceHistory

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Load user for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

   
    db.init_app(app)


    with app.app_context():
        db.create_all()

    return app 

from website.models import db
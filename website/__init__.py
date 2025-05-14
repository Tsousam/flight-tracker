from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

    #print("SECRET_KEY:", app.config['SECRET_KEY'])
    #print("DATABASE_URL:", app.config['SQLALCHEMY_DATABASE_URI'])
    
    from website.auth import auth
    from website.views import views

    app.register_blueprint(auth)
    app.register_blueprint(views)

    from website.models import db, User, TrackedFlight, PriceHistory
   
    db.init_app(app)


    with app.app_context():
        db.create_all()

    return app 
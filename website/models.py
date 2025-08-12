from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func, asc


db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tracked_flights = db.relationship("TrackedFlights", backref="user", lazy=True)


class TrackedFlights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    url = db.Column(db.String, nullable=True)
    airline = db.Column(db.String, nullable=False)
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    departure_arrival_time = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(25), nullable=False)
    price = db.Column(db.String, nullable=True)
    bookable_seats = db.Column(db.Integer, nullable=True)
    last_checked = db.Column(db.DateTime(timezone=True), server_default=func.now())
    #is_date_range = db.Column(db.Boolean, default=False)
    #initial_date_range = db.Column(db.Date, nullable=True)
    #end_date_range = db.Column(db.Date, nullable=True)
    #only_direct_flights = db.Column(db.Boolean, default=False)

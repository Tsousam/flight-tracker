from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func



db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tracked_flights = db.relationship("TrackedFlights", backref="user", lazy=True)


class TrackedFlights(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_date = db.Column(db.Date, nullable=True)
    is_date_range = db.Column(db.Boolean, default=False)
    initial_date_range = db.Column(db.Date, nullable=True)
    end_date_range = db.Column(db.Date, nullable=True)
    only_direct_flights = db.Column(db.Boolean, default=False)
    current_price = db.Column(db.Float)
    last_checked = db.Column(db.DateTime(timezone=True), server_default=func.now())
    booking_link = db.Column(db.String, nullable=True)


class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracked_flight_id = db.Column(db.Integer, db.ForeignKey("tracked_flights.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    checked_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

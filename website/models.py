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
    departure_date = db.Column(db.Date, nullable=False)
    flex_days = db.Column(db.Integer, default=0)
    is_weekday = db.Column(db.Boolean, default=False)
    is_weekend = db.Column(db.Boolean, default=False)
    current_price = db.Column(db.Float)
    last_checked = db.Column(db.DateTime(timezone=True), server_default=func.now())
    booking_link = db.Column(db.String, nullable=True)


class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracked_flight_id = db.Column(db.Integer, db.ForeignKey("tracked_flights.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    checked_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

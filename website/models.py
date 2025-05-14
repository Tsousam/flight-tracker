from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    tracked_flights = db.relationship('TrackedFlight', backref='user', lazy=True)


class TrackedFlight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    current_price = db.Column(db.Float)
    last_checked = db.Column(db.DateTime(timezone=True), server_default=func.now())
    external_booking_link = db.Column(db.String, nullable=True)


class PriceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracked_flight_id = db.Column(db.Integer, db.ForeignKey('tracked_flight.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    checked_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

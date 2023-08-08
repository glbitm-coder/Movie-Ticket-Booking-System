from datetime import datetime
from application import db


class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    created_date_time = db.Column(db.DateTime, default=datetime.now)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), unique=True)
    booking = db.relationship('Booking', back_populates='rating', uselist=False)
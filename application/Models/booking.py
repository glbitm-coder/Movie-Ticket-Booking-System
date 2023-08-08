from datetime import datetime
from application import db


class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    number_of_tickets = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    created_date_time = db.Column(db.DateTime, default=datetime.now)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.relationship('Rating', back_populates='booking', uselist=False)
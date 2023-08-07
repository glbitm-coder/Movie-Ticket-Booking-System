from datetime import datetime
from application import db


class Theatre(db.Model):
    __tablename__ = 'theatre'
    id = db.Column(db.Integer, primary_key=True)
    storedName = db.Column(db.String, nullable=False)
    storedPlace = db.Column(db.String, unique=False, nullable=False)
    storedCapacity = db.Column(db.Integer, nullable=False)
    storedImage = db.Column(db.String, default="", unique=True, nullable=False)
    created_date_time = db.Column(db.DateTime, default=datetime.now)
    updated_date_time = db.Column(db.DateTime, default=datetime.now)
    createdby_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shows = db.relationship('Show', secondary='show_theatre_association', back_populates='theatres')
    bookings = db.relationship('Booking', backref='theatre', cascade="all,delete")
    ratings = db.relationship('Rating', backref='theatre', cascade="all,delete")

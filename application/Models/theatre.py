from application import db
from flask_login import UserMixin


class Theatre(db.Model, UserMixin):
    __tablename__ = 'theatre'
    id = db.Column(db.Integer, primary_key=True)
    storedName = db.Column(db.String, nullable=False)
    storedPlace = db.Column(db.String, unique=False, nullable=False)
    storedCapacity = db.Column(db.Integer, nullable=False)
    storedImage = db.Column(db.String, default="", unique=True, nullable=False)
    createdby_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shows = db.relationship('Show', secondary='show_theatre_association', back_populates='theatres')
    bookings = db.relationship('Booking', backref='theatre', cascade="all,delete")
    ratings = db.relationship('Rating', backref='theatre', cascade="all,delete")

from application import db
from flask_login import UserMixin


class Show(db.Model, UserMixin):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    storedName = db.Column(db.String, nullable=False)
    storedRating = db.Column(db.Integer, default=0)
    storedPrice = db.Column(db.Integer, nullable=False)
    storedTags = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    startTime = db.Column(db.Time, nullable=False)
    endTime = db.Column(db.Time, nullable=False)

    theatres = db.relationship('Theatre', secondary='show_theatre_association', back_populates='shows')
    createdby_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
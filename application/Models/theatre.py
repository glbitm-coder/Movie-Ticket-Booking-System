from application import db
from flask_login import UserMixin


class Theatre(db.Model, UserMixin):
    __tablename__ = 'theatre'
    id = db.Column(db.Integer, primary_key=True)
    storedPlace = db.Column(db.String, unique=True, nullable=False)
    storedName = db.Column(db.String, nullable=False)
    storedCapacity = db.Column(db.Integer, nullable=False)
    storedImage = db.Column(db.Integer, unique=True, nullable=False)
from application import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    stored_email = db.Column(db.String(64), unique=True, nullable=False)
    stored_username = db.Column(db.String(64), unique=True, nullable=False)
    stored_password = db.Column(db.String(64), unique=True, nullable=False)
    stored_timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    theatres_created = db.relationship('Theatre', backref='creator', lazy='dynamic', cascade="all,delete")
    shows_created = db.relationship('Show', backref='creator', lazy='dynamic', cascade="all,delete")
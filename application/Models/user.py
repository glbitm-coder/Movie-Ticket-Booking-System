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
    # stored_blogs = db.relationship('Blog', backref='user', lazy='dynamic',cscade="all,delete")
    # stored_comments = db.relationship('Comment', backref='user',cascade="all,delete" )
    # stored_likes = db.relationship('Like', backref='user', cascade="all,delete")
    # stored_followers = db.relationship('Follow',foreign_keys=[Follow.stored_following_id], backref='user',lazy='dynamic', cascade="all,delete")
    # stored_following = db.relationship('Follow',foreign_keys=[Follow.stored_follower_id], backref='user2',lazy='dynamic', cascade="all,delete")

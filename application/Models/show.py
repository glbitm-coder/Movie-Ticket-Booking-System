from application import db


class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    storedName = db.Column(db.String, nullable=False)
    storedPrice = db.Column(db.Integer, nullable=False)
    storedTags = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    startTime = db.Column(db.Time, nullable=False)
    endTime = db.Column(db.Time, nullable=False)
    theatres = db.relationship('Theatre', secondary='show_theatre_association', back_populates='shows')
    createdby_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bookings = db.relationship('Booking', backref='show', cascade="all,delete")
    ratings = db.relationship('Rating', backref='show', cascade="all,delete")
    
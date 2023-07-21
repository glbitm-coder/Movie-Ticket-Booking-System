from application import db


class ShowTheatreAssociation(db.Model):
    __tablename__ = 'show_theatre_association'
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), primary_key=True)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'), primary_key=True)

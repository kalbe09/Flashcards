from .. import db


class Phasen(db.Model):
    __tablename__ = 'phasen'
    id = db.Column(db.Integer, primary_key=True)
    waiting_days = db.Column(db.Integer)
    flashcards = db.relationship('Flashcard', backref='collection', lazy='dynamic')


    def __repr__(self):
        return '<Category: %r>' % self.name
from datetime import datetime
from .. import db
from .hascategory import has_category


class FlashcardCollection(db.Model):
    __tablename__ = 'flashcardcollection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    finaldate = db.Column(db.Text)
    prio = db.Column(db.Integer, default=0)
    activ = db.Column(db.Boolean, default=True)
    flashcards = db.relationship('Flashcard', backref='collection', lazy='dynamic')
    categories = db.relationship('Category',
                                 secondary=has_category,
                                 backref=db.backref('collections', lazy='dynamic'),
                                 lazy='dynamic')

    def __repr__(self):
        return '<Flashcard Collection: %r>' % self.name

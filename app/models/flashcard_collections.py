from datetime import datetime
from .. import db
from .hascategory import has_category


class Collection(db.Model):
    __tablename__ = 'flashcardcollection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    
    
    duedate = db.Column(db.Text)
    prio = db.Column(db.Integer, default=0)
    activ = db.Column(db.Boolean, default=True)
    

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    flashcards = db.relationship('Flashcard', backref='collection', lazy='dynamic')
    categories = db.relationship('Category',
                                 secondary=has_category,
                                 backref=db.backref('collections', lazy='dynamic'),
                                 lazy='dynamic')

    def __repr__(self):
        return '<Flashcard Collection: %r>' % self.name

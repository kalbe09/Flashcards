from .. import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    
    duedate = db.Column(db.Date) # Datefield
# datetime.strptime('09.19.2018', '%m.%d.%Y').date())

    prio = db.Column(db.Integer, default=0)
    activ = db.Column(db.Boolean, default=True)
    #flashcards = db.relationship('Flashcard', backref='collection', lazy='dynamic')

    def __repr__(self):
        return '<Category: %r>' % self.name
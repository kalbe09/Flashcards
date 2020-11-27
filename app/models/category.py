from .. import db


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    finaldate = db.Column(db.Text)
    prio = db.Column(db.Integer, default=0)
    activ = db.Column(db.Boolean, default=True)
    #flashcards = db.relationship('Flashcard', backref='collection', lazy='dynamic')

    def __repr__(self):
        return '<Category: %r>' % self.name
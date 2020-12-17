from .. import db


class Learning(db.Model):
    __tablename__ = 'learning'
    id = db.Column(db.Integer, primary_key=True)
    starttime = db.Column(db.Integer)
    mode = db.Column(db.Text)
    flashcards = db.Column(db.Text)

    def __repr__(self):
        return '<Learning: %r>' % self.mode

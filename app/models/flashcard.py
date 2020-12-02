from .. import db
from markdown import markdown
import bleach
import datetime



class Flashcard(db.Model):
    __tablename__ = 'flashcard'
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('flashcardcollection.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
#    phase = db.Column(db.Integer, db.ForeignKey('phasen.id'))    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    question = db.Column(db.Text)
    question_html = db.Column(db.Text)
    answer = db.Column(db.Text)
    answer_html = db.Column(db.Text)

    right_answered = db.Column(db.Boolean, default=False)
    wrong_answered = db.Column(db.Boolean, default=False)
    sum_right_answered = db.Column(db.Integer, default=0)
    sum_wrong_answered = db.Column(db.Integer, default=0)
    sum_answered = db.Column(db.Integer, default=0)
    quote = db.Column(db.Float, default=0)

    vote_bad = db.Column(db.Integer, default=0)
    vote_good = db.Column(db.Integer, default=0)

#    phase = db.Column(db.Integer, default=0)
    nextdate = db.Column(db.Text, default=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d.%m.%Y"))
    lastdate = db.Column(db.Text, default=datetime.datetime.now().strftime("%d.%m.%Y"))


    # Whitelist for allowed tags
    @staticmethod
    def on_changed_question(target, value, oldvalue, initiator):
        allowed_tags = ['abbr', 'acronym', 'b', 'blockquote', 'code', 'i',
                        'li', 'ol', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.question_html = bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True)

    # Whitelist for allowed tags
    @staticmethod
    def on_changed_answer(target, value, oldvalue, initiator):
        allowed_tags = ['abbr', 'acronym', 'b', 'blockquote', 'code', 'i',
                        'li', 'ol', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.answer_html = bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True)

    def __repr__(self):
        return '<Flashcard: %r>' % self.id

db.event.listen(Flashcard.answer, 'set', Flashcard.on_changed_answer)
db.event.listen(Flashcard.question, 'set', Flashcard.on_changed_question)

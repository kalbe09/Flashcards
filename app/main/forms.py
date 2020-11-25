from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class FlashcardCollectionForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = StringField('Lektion', validators=[DataRequired()])
    submit = SubmitField('Hinzufügen')


class FlashcardForm(FlaskForm):
    question = PageDownField('Frage', validators=[DataRequired()])
    answer = PageDownField('Antwort', validators=[DataRequired()])
    next = BooleanField('Nächste Karte?')
    submit = SubmitField('Hinzufügen')


class EditFlashcardForm(FlaskForm):
    question = PageDownField('Frage', validators=[DataRequired()])
    answer = PageDownField('Antwort', validators=[DataRequired()])
    submit = SubmitField('Hinzufügen')

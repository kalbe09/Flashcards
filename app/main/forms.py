from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, BooleanField, DateField, IntegerField
from wtforms.validators import DataRequired, Optional


class CollectionForm(FlaskForm):
    name = StringField('Name*', validators=[DataRequired()])
    category = StringField('Lektion*', validators=[DataRequired()])
    duedate = DateField('Fälligkeit', format='%d.%m.%Y', validators=[Optional()])
    prio = IntegerField('Priorität', validators=[Optional()])
    submit = SubmitField('Hinzufügen')

class FlashcardCategoryForm(FlaskForm):
    name = StringField('Lektion*', validators=[DataRequired()])
    duedate = DateField('Fälligkeit', format='%d.%m.%Y', validators=[Optional()])
    prio = IntegerField('Priorität', validators=[Optional()])
    submit = SubmitField('Hinzufügen')


class FlashcardForm(FlaskForm):
    question = PageDownField('Frage', validators=[DataRequired()])
    answer = PageDownField('Antwort', validators=[DataRequired()])
    #next = BooleanField('Nächste Karte?')
    submit = SubmitField('Hinzufügen')


class EditFlashcardForm(FlaskForm):
    question = PageDownField('Frage', validators=[DataRequired()])
    answer = PageDownField('Antwort', validators=[DataRequired()])
    submit = SubmitField('Hinzufügen')

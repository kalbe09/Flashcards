from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, BooleanField, DateField, IntegerField, FileField
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
    photo = FileField('Bild', validators=[Optional()])
    submit = SubmitField('Hinzufügen')




class EditCourseForm(FlaskForm):
    name = StringField('Name*', validators=[DataRequired()])
    duedate = DateField('Fälligkeit', format='%d.%m.%Y', validators=[Optional()])
    prio = IntegerField('Priorität', validators=[Optional()])
    submit = SubmitField('Ändern')

class EditCategoryForm(FlaskForm):
    name = StringField('Name*', validators=[DataRequired()])
    duedate = DateField('Fälligkeit', format='%d.%m.%Y', validators=[Optional()])
    prio = IntegerField('Priorität', validators=[Optional()])
    submit = SubmitField('Ändern')

class EditFlashcardForm(FlaskForm):
    question = PageDownField('Frage', validators=[DataRequired()])
    answer = PageDownField('Antwort', validators=[DataRequired()])
    submit = SubmitField('Ändern')

class ImportForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Submit')
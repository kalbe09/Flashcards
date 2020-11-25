from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from ..models.users import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('Eingeloggt bleiben')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Benutzername', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Benutzername darf nur Buchstaben, '
                                              'Zahlen, Punkte or Unterstriche enthalten.')])
    password = PasswordField('Passwort', validators=[
        DataRequired(), EqualTo('password2', message='Passwort muss übereinstimmen.')])
    password2 = PasswordField('Passwort bestätigen', validators=[DataRequired()])
    submit = SubmitField('Registrieren')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email ist schon registriert.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Benutzername schon vorhanden.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Altes Passwort', validators=[DataRequired()])
    password = PasswordField('Neues Passwort', validators=[
        DataRequired(), EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Bestätige dein Passwort', validators=[DataRequired()])
    submit = SubmitField('Passwort ändern')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Passwort zurücksetzen')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Neues Passwort', validators=[
        DataRequired(), EqualTo('password2', message='Paswörter müssen übereinstimmen')])
    password2 = PasswordField('Passwort bestätigen', validators=[DataRequired()])
    submit = SubmitField('Passwort zurücksetzen')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unbekannte Email-Adresse.')


class ChangeEmailForm(FlaskForm):
    email = StringField('Neue Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Email-Addresse ändern')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email schon vorhanden.')

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..email import send_email
from ..models.users import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, \
    PasswordResetForm, ChangeEmailForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Ungültiger Benutzername oder Password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Du hast dich ausgeloggt.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Bestätige dein Account', 'auth/email/confirm', user=user, token=token)
        flash('Eine Bestätigunsmail wurde an deine Email-Adresse gesendet.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('Deine Email-Adresse wurde bestätigt. Danke!')
    else:
        flash('Der Bestätigungslink ist nicht gültig oder abgelaufen!')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Bestätige dein Account', 'auth/email/confirm', user=current_user, token=token)
    
    # ******************Muss wieder geändert werden************************************+
    # flash('Eine neue Bestätigunsmail wurde an deine Email-Adresse gesendet.')
    current_user.confirm(token)
    # ******************Muss wieder geändert werden************************************+
    
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Dein Passwort wurde geändert')
            return redirect(url_for('main.index'))
        else:
            flash('Ungültiges Passwort.')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Passwort zurücksetzen',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('Du hast eine neue Email mit Anweisungen erhalten.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Dein Passwort wurde geändert.')
            return redirect(url_for('auth.login'))
        else:
            flash('Dein Passwort konnte nicht geändert werden')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Bestätige deine Email-Adresse',
                       'auth/email/change_email', user=current_user, token=token)
            flash('Du hast eine neue Email mit Anweisungen erhalten.')
            return redirect(url_for('main.index'))
        else:
            flash('Ungültiges Passwort oder Benutzername')
    return render_template('auth/change_email.html', form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Die Email-Adresse wurde geändert')
    else:
        flash('Konnte nicht geändert werden.')
    return redirect(url_for('main.index'))

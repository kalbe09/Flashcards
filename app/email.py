from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail
from . import config
import smtplib



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASHCARD_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASHCARD_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    print("1")

    
    gmail_user = app.config['MAIL_USERNAME']
    gmail_password = app.config['MAIL_PASSWORD']
    print(gmail_user)
    print(gmail_password)
    sent_from = gmail_user
    subject = 'OMG Super Important Message'
    body = 'Hey, whats up?\n\n- You'

    email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

    try:
        print("2")
        server = smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.ehlo()
        print("server")
        server.login(gmail_user, gmail_password)
        print("login")
        server.sendmail(sent_from, to, email_text)
        server.close()
        print("Geschafft")
    except:
        print('Something went wrong...')
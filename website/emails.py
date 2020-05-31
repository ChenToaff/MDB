from itsdangerous import URLSafeTimedSerializer
from .app import app,mail
from flask_mail import Message
from flask import url_for,render_template



def create_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt =app.config['SECURITY_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

def send_confirmation(email):
    token = create_token(email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('mail_activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(email, subject, html)

def send_password_change(email):
    token = create_token(email)
    confirm_url = url_for('password_token', token=token, _external=True)
    html = render_template('mail_change_password.html', confirm_url=confirm_url)
    subject = "Change Password"
    send_email(email, subject, html)
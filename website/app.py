from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail
import os
from .secrets import maiiPassword,mailUsername


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(16)
app.config['SECURITY_SALT'] = os.urandom(16).hex()
# DB settings
app.config["MONGO_URI"] = "mongodb://localhost:27017/Tweety"
# mail settings
app.config["MAIL_SERVER"] = 'smtp.googlemail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
# gmail authentication
app.config["MAIL_USERNAME"] = mailUsername
app.config["MAIL_PASSWORD"] = maiiPassword
# mail accounts
app.config["MAIL_DEFAULT_SENDER"] = 'from@example.com'
mail = Mail(app)
mongo = PyMongo(app)
from .routes import *


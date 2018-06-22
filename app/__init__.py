from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import  Migrate
from flask_login import LoginManager
from logging.handlers import SMTPHandler, RotatingFileHandler
import logging
import os

new_app = Flask(__name__)
new_app.config.from_object(Config)
db = SQLAlchemy(new_app)
migrate = Migrate(new_app,db)
login = LoginManager(new_app)
login.login_view = 'login'

if not new_app.debug:
    if new_app.config['MAIL_SERVER']:
        auth = None
        if new_app.config['MAIL_USERNAME'] or new_app.config['MAIL_PASSWORD']:
            auth = (new_app.config['MAIL_USERNAME'], new_app.config['MAIL_PASSWORD'])
        secure = None
        if new_app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(new_app.config['MAIL_SERVER'], new_app.config['MAIL_PORT']),
            fromaddr='no-reply@' + new_app.config['MAIL_SERVER'],
            toaddrs=new_app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        new_app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    new_app.logger.addHandler(file_handler)

    new_app.logger.setLevel(logging.INFO)
    new_app.logger.info('Microblog startup')

from app import routes, models, errors


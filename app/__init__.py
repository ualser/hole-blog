from flask import Flask, Response, session
from flask.ext.login import LoginManager, UserMixin, login_required
from flask.ext.session import Session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
sess = Session()
login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_object('config')
db = SQLAlchemy(app)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)

from app import views, models

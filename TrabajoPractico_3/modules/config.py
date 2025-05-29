#dependencias
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_session import Session
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
# from flask_bootstrap import Bootstrap
import datetime


app = Flask("server")
app.config['SECRET_KEY'] = "d87h3dxodj09j30"
URL_BD = 'sqlite:///data/base_datos.db'

def crear_engine():
    engine = create_engine(URL_BD)
    Session = sessionmaker(bind=engine)
    return Session

app.config.from_object(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./flask_session_cache"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=5)
Session(app)

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
# Bootstrap
# Bootstrap(app)
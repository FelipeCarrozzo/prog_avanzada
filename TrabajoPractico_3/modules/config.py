from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask("server")
SECRET_KEY = "d87h3dxodj09j30"
app.config['SECRET_KEY'] = SECRET_KEY
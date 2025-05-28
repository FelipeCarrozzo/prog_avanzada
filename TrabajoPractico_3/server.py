from flask_wtf import FlaskForm
from flask import Flask, request, render_template, flash, redirect, url_for, session
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from modules.config import SECRET_KEY
# from modules.gestorDeUsuarios import GestorUsuarios
from modules.formularios import RegistroForm

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
# app.config.from_object('config') 

# Página de inicio
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#         form = LoginForm()
#         if form.validate_on_submit():
#             # Procesamiento del login
#             username = form.username.data
#             password = form.password.data
#             print(f'Usuario: {username}, Contraseña: {password}')
#             return redirect(url_for('dashboard'))

#     return render_template('login.html', form=form)

#pagina de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Aquí podrías guardar el usuario en una base de datos
        print(f"Nuevo usuario: {username}, Email: {email}, Contraseña: {password}")
        flash('Usuario registrado exitosamente', 'success')
        # return redirect(url_for('login'))  # Redirigís a la página de login u otra

    return render_template('registro.html', form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
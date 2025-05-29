from flask_wtf import FlaskForm
from flask import Flask, request, render_template, flash, redirect, url_for, session
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from modules.config import app
from modules.gestorUsuarios import GestorUsuarios
from modules.formularios import RegistroForm

# app = Flask(__name__)
# app.config['SECRET_KEY'] = SECRET_KEY
# app.config.from_object('config') 

# admin_list = [1]
# repoReclamo, repoUsuario = crear_repositorio()
# gestor_libros = GestorDeLibros(repo_libro)
# gestor_usuarios = GestorDeUsuarios(repo_usuario)
gestorUsuarios = GestorUsuarios()
# gestor_login = GestorDeLogin(gestor_usuarios, login_manager, admin_list)

@app.route("/register", methods= ["GET", "POST"])
def register():
    form_registro = RegistroForm()
    if form_registro.validate_on_submit():
        try:
            gestorUsuarios.registrarUsuario(form_registro.nombre.data, 
                                                    form_registro.email.data, 
                                                    form_registro.password.data)
        except ValueError as e:
            flash(str(e))    
        else:
            flash("Usuario registrado con éxito")
            return redirect(url_for("login"))               
    return render_template('register.html', form=form_registro)




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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
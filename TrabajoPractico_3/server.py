# from flask_wtf import FlaskForm
from flask import render_template, flash, redirect, url_for, session
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Length
from modules.config import app, login_manager
from modules.gestorUsuarios import GestorUsuarios
from modules.gestorLogin import GestorDeLogin
from modules.formularios import RegistroForm, LoginForm
from modules.factoriaRepositorios import crearRepositorio

# app = Flask(__name__)
# app.config['SECRET_KEY'] = SECRET_KEY
# app.config.from_object('config') 

adminList = [1]
# repoReclamo, repoUsuario = crear_repositorio()
# gestor_libros = GestorDeLibros(repo_libro)
# gestor_usuarios = GestorDeUsuarios(repo_usuario)
repoUsuario = crearRepositorio()
gestorUsuarios = GestorUsuarios(repoUsuario)
gestor_login = GestorDeLogin(gestorUsuarios, login_manager, adminList)


@app.route('/')
def inicio():
    return render_template('inicio.html')


@app.route("/register", methods= ["GET", "POST"])
def register():
    form_registro = RegistroForm()
    if form_registro.validate_on_submit():
        try:
            gestorUsuarios.registrarUsuario(form_registro.nombre.data, 
                                                    form_registro.apellido.data, 
                                                    form_registro.email.data,
                                                    form_registro.nombreUsuario.data,
                                                    form_registro.claustro.data,
                                                    form_registro.password.data)
        except ValueError as e:
            flash(str(e))
        else:
            flash("Usuario registrado con éxito")
            return redirect(url_for("register"))
    return render_template('registro.html', form=form_registro)


# Página de login: principal
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     """"
#     inicio de sesión de usuarios (finales y administradores).
#     Se crea instancia de LoginForm y se valida.
#     Se autentica al usuario con el gestor de usuarios.
#     Si la autenticación es exitosa, se inicia sesión con el gestor de login
#     y se redirige a la página de inicio, pasando el nombre de usuario a la sesión.
#     """
#     print("Entrando a la página de login")
#     formLogin = LoginForm()
#     if formLogin.validate_on_submit():
#         print("Formulario de login válido")
#         try:
#             usuario = gestorUsuarios.autenticarUsuario(formLogin.username.data, formLogin.password.data) 
#             print(f"Usuario autenticado: {usuario}")
#             if not usuario:
#                 raise ValueError("El usuario no está registrado o la contraseña es incorrecta.")
#             else:
#                 gestor_login.loginUsuario(usuario)
#                 session['username'] = gestor_login.nombreUsuarioActual
#                 return redirect(url_for('inicio'))
#         except ValueError as e:
#                 flash(str("Error: el usuario no está registrado o la contraseña es incorrecta."))
#     return render_template('login.html', form=formLogin)

@app.route("/login", methods= ["GET", "POST"])
def login():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        try:
            usuario = gestorUsuarios.autenticarUsuario(form_login.username.data, 
                                                         form_login.password.data)
        except ValueError as e:
            flash(str(e))
        else:
            gestor_login.loginUsuario(usuario)
            session['username'] = gestor_login.nombreUsuarioActual
            return redirect(url_for('inicio')) 

    return render_template('login.html', form=form_login)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
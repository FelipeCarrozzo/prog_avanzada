# from flask_wtf import FlaskForm
from flask import render_template, flash, redirect, url_for, session
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Length
from modules.config import app, login_manager
from modules.gestorUsuarios import GestorUsuarios
from modules.gestorReclamos import GestorReclamos
from modules.gestorLogin import GestorDeLogin
from modules.formularios import RegistroForm, LoginForm, ReclamosForm
from modules.factoriaRepositorios import crearRepositorio

adminList = [1]
repoUsuario, repoReclamo = crearRepositorio()
gestorUsuarios = GestorUsuarios(repoUsuario)
gestorReclamos = GestorReclamos(repoReclamo)
gestor_login = GestorDeLogin(gestorUsuarios, login_manager, adminList)


@app.route('/')
def inicio():
    """
    Ruta principal que renderiza la página de inicio.
    Carga los datos de los usuarios administrativos desde un archivo y los registra en el sistema.
    """
    # Registro de usuarios administrativos
    archivoDatos = "./data/datosAdmins.txt"
    
    with open(archivoDatos, 'r') as file:
        for line in file:
            nombre, apellido, email, nombreUsuario, rol, password = line.strip().split(',')
            try:
                gestorUsuarios.registrarUsuario(nombre, apellido, email, nombreUsuario, rol, password)
            except ValueError as e:
                print(f"Error al registrar admin {nombreUsuario}: {e}")  
    
    return render_template('inicio.html')

@app.route("/bienvenido")
def bienvenido():
    """
    Ruta que renderiza la página de bienvenida.
    Muestra el nombre de usuario actual si está autenticado.
    """
    if 'username' in session:
        username = session['username']
        return render_template('bienvenido.html', username=username)
    else:
        flash("Debes iniciar sesión primero.")
        return redirect(url_for('login'))
    

        
    #     <!-- <a href = "{{ url_for('misReclamos') }}">Ver mis reclamos</a> -->

    #     <!-- <a href = "{{ url_for('listarReclamos') }}">Ver reclamos existentes</a> -->

    #     <!-- <a href = "{{ url_for('logout') }}">Cerrar sesión</a> -->
    # </div>

@app.route("/register", methods= ["GET", "POST"])
def register():
    form_registro = RegistroForm()
    if form_registro.validate_on_submit():
        try:
            gestorUsuarios.registrarUsuario(form_registro.nombre.data, 
                                                    form_registro.apellido.data, 
                                                    form_registro.email.data,
                                                    form_registro.nombreUsuario.data,
                                                    form_registro.rol,  # Asignamos el rol directamente
                                                    form_registro.password.data)
        except ValueError as e:
            flash(str(e))
        else:
            flash("Usuario registrado con éxito")
            return redirect(url_for("register"))
    return render_template('registro.html', form=form_registro)


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
            return redirect(url_for('bienvenido'))

    return render_template('login.html', form=form_login)


@app.route("/reclamos", methods=["GET", "POST"])
def crearReclamos():
    """
    Ruta que renderiza la página de reclamos.
    Muestra los reclamos del usuario actual si está autenticado.
    """
    form = ReclamosForm()
    idUsuario = gestor_login.idUsuarioActual
    descripReclamo = session.get('descripcion_reclamo')
    if 'username' in session:
        username = session['username']
        if form.validate_on_submit():
            descripcion = form.descripcion.data
            imagen = form.imagen.data
            try:
                gestorReclamos.crearReclamo(idUsuario, descripcion, imagen)
                flash("Reclamo creado con éxito")
                return redirect(url_for('crearReclamos'))
            except ValueError as e:
                flash(str(e))
        return render_template('nuevoReclamo.html', form=form, username=username, descripcion=descripReclamo)
    else:
        flash("Debes iniciar sesión primero.")
        return redirect(url_for('login'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
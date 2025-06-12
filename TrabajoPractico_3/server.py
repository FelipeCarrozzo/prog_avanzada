# from flask_wtf import FlaskForm
from flask import render_template, flash, redirect, url_for, session
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Length
import re
from modules.config import app, login_manager
from modules.gestorUsuarios import GestorUsuarios
from modules.gestorReclamos import GestorReclamos
from modules.gestorLogin import GestorDeLogin
from modules.formularios import RegistroForm, LoginForm, ReclamosForm
from modules.factoriaRepositorios import crearRepositorio
from flask import send_file, request
from modules.gestorReportes import GestorReportes

adminList = [1]
repoUsuario, repoReclamo = crearRepositorio()
gestorUsuarios = GestorUsuarios(repoUsuario)
gestorReclamos = GestorReclamos(repoReclamo)
gestor_login = GestorDeLogin(gestorUsuarios, login_manager, adminList)

gestorReportes = GestorReportes(repoReclamo)

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
            return redirect(url_for("login"))
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
            rol = gestor_login.obtenerRolUsuario()

            #definir lista de departamentos posibles? para que cuando se agrega un departamento nuevo,
            #solo se modifique al principio y no a lo largo del server
            if rol == 'secretarioTecnico' or rol == "jefeMaestranza" or rol == "jefeSoporteInformático":
                return redirect(url_for('panelAdmin'))
            
            elif rol == 'UsuarioFinal':
                return redirect(url_for('bienvenido'))

            else:
                return redirect(url_for('inicio'))

    return render_template('login.html', form=form_login)

@app.route("/adherir_a_reclamo/<int:idReclamo>", methods=["GET", "POST"])
def adherir_a_reclamo(idReclamo):
    usuario = gestor_login.idUsuarioActual  

    if gestorReclamos.adherirAReclamo(idReclamo, usuario):
        flash("Te has adherido exitosamente al reclamo.")
    else:
        flash("No fue posible adherirse al reclamo (ya estás adherido o reclamo no existe).")

    return redirect(url_for("pagina_principal"))

@app.route("/reclamos", methods=["GET", "POST"])
def crearReclamos():
    """
    Ruta que renderiza la página de reclamos.
    Muestra los reclamos del usuario actual si está autenticado.
    """
    form = ReclamosForm()
    idUsuario = gestor_login.idUsuarioActual
    # descripReclamo = session.get('descripcion_reclamo')
    if 'username' in session:
        username = session['username']
        if form.validate_on_submit():
            descripcion = form.descripcion.data
            imagen = form.imagen.data
            try:
                reclamoSimilar = gestorReclamos.verificarReclamoExistente(idUsuario, {"descripcion": descripcion})
                if reclamoSimilar:
                    return render_template('adherirAReclamo.html', reclamos=reclamoSimilar)
            except ValueError as e:
                flash(str(e))
                return redirect(url_for('crearReclamos'))
            try:
                gestorReclamos.crearReclamo(idUsuario, descripcion, imagen)
                flash("Reclamo creado con éxito")
                return redirect(url_for('crearReclamos')) #AGREGAR
            except ValueError as e:
                flash(str(e))
    return render_template("login.html", form=form)

@app.route("/panelAdmin", methods=["GET", "POST"])
def panelAdmin():
    if 'username' not in session:
        flash("Debes iniciar sesión primero.")
        return redirect(url_for('login'))

    username = session['username']
    rol = gestor_login.rolUsuarioActual
    departamento = None
    es_secretario = False

    # --- POST: procesar cambios en reclamos ---
    if request.method == "POST":
        # Recorremos los reclamos existentes
        reclamos = repoReclamo.obtenerRegistrosTotales()  # O filtrados por departamento
        for reclamo in reclamos:
            rid = reclamo.id
            estado_key = f"estado_{rid}"
            tiempo_key = f"tiempo_{rid}"
            depto_key = f"departamento_{rid}"

            # Si se enviaron datos para este reclamo:
            if estado_key in request.form:
                nuevo_estado = request.form[estado_key]
                repoReclamo.actualizarAtributo(rid, "estado", nuevo_estado)

            if tiempo_key in request.form and request.form[tiempo_key].strip() != "":
                nuevo_tiempo = int(request.form[tiempo_key])
                repoReclamo.actualizarAtributo(rid, "tiempoResolucion", nuevo_tiempo)

            if rol == "secretarioTecnico" and depto_key in request.form:
                nuevo_depto = request.form[depto_key]
                repoReclamo.actualizarAtributo(rid, "departamento", nuevo_depto)

        flash("Cambios guardados correctamente.")
        return redirect(url_for('panelAdmin'))

    # --- GET: mostrar página con los reclamos ---
    if rol.startswith("jefe"):
        departamento = re.sub(r'(?<!^)(?=[A-Z])', ' ', rol[4:]).lower()
        reclamos = repoReclamo.obtenerRegistrosFiltro("departamento", departamento)
    elif rol == "secretarioTecnico":
        es_secretario = True
        departamento = "todos"
        reclamos = repoReclamo.obtenerRegistrosTotales()
    else:
        flash("No tenés permisos para acceder al panel de administración.")
        return redirect(url_for("bienvenido"))

    return render_template("panelAdmin.html", 
                           username=username, 
                           rol=rol,
                           departamento=departamento, 
                           reclamos=reclamos, 
                           es_secretario=es_secretario)


@app.route("/analitica")
def analitica():
    if 'username' not in session:
        flash("Debes iniciar sesión primero.")
        return redirect(url_for('login'))

    rol = gestor_login.rolUsuarioActual
    departamento = None
    if rol.startswith("jefe"):
        departamento = rol[4:]
        departamento = re.sub(r'(?<!^)(?=[A-Z])', ' ', departamento).lower()

    datosReporte = gestorReportes.generarReporte(departamento)
    if departamento == None:
        departamento = "Soporte Técnico"
    else:
        departamento = departamento.title()

    return render_template("analitica.html", datos=datosReporte, departamento=departamento)


@app.route("/descargar/<formato>")
def descargarReporte(formato):
    if formato not in ['pdf', 'html']:
        flash("Formato no soportado")
        return redirect(url_for('bienvenido'))

    #obtener departamento si se trata de un jefe
    ruta = gestorReportes.exportarReporte(formato)

    nombre_archivo = ruta.split("/")[-1]  # solo el nombre del archivo
    return send_file(
        ruta,
        as_attachment=True,
        download_name=nombre_archivo,
        mimetype="application/pdf" if formato == "pdf" else "text/html"
    )

@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
#dependencias
from flask import render_template, flash, redirect, url_for, session
import re
from modules.config import app, login_manager
from modules.gestorUsuarios import GestorUsuarios
from modules.gestorReclamos import GestorReclamos
from modules.gestorLogin import GestorDeLogin
from modules.formularios import RegistroForm, LoginForm, ReclamosForm
from modules.factoriaRepositorios import crearRepositorio
from flask import send_file, request, send_from_directory
from modules.gestorReportes import GestorReportes, NoDataError
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

adminList = [1] 
repoUsuario, repoReclamo = crearRepositorio()
gestorUsuarios = GestorUsuarios(repoUsuario)
gestorReclamos = GestorReclamos(repoReclamo)
gestorLogin = GestorDeLogin(gestorUsuarios, login_manager, adminList)
gestorReportes = GestorReportes(repoReclamo)

rolesAdmin = ['secretarioTecnico', 'jefeMaestranza', 'jefeSoporteInformático']

@app.route('/')
def inicio():
    """
    Ruta principal que renderiza la página de inicio.
    Carga los datos de los usuarios administrativos desde un archivo y los registra en el sistema.
    """
    # Registro de usuarios administrativos
    archivoDatos = "./data/datosAdmins.txt"

    with open(archivoDatos, 'r', encoding='utf-8') as file:
        for line in file:
            nombre, apellido, email, nombreUsuario, rol, password = line.strip().split(',')
            try:
                gestorUsuarios.registrarUsuario(nombre, apellido, email, nombreUsuario, rol, password)
            except ValueError as e:
                print(f"Error al registrar admin {nombreUsuario}: {e}")  
    return render_template('inicio.html')

@app.route("/bienvenido")
@login_required
def bienvenido():
    """
    Ruta que renderiza la página de bienvenida.
    Muestra el nombre de usuario actual si está autenticado.
    """

    return render_template('bienvenido.html', username=current_user.nombre)

@app.route("/register", methods= ["GET", "POST"])
def register():
    """
    Ruta para registrar un nuevo usuario.
    Se utiliza un formulario para capturar los datos del usuario.
    Si el formulario es válido, se registra el usuario y se redirige a la página de inicio de sesión.
    """
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
    """
    Ruta para iniciar sesión. Se utiliza un formulario de inicio de sesión.
    Si el formulario es válido, se autentica al usuario y se redirige según su rol.
    """
    form_login = LoginForm()
    if form_login.validate_on_submit():
        try:
            usuario = gestorUsuarios.autenticarUsuario(form_login.username.data, 
                                                         form_login.password.data)
        except ValueError as e:
            flash(str(e))
        else:
            gestorLogin.loginUsuario(usuario)

            session.permanent = True #Mantener sesión activa
            rol = gestorLogin.obtenerRolUsuario()

            if rol in rolesAdmin:
                return redirect(url_for('panelAdmin'))
            elif rol == 'UsuarioFinal':
                return redirect(url_for('bienvenido'))
            else:
                flash("No tenés permisos para acceder", "error")
                return redirect(url_for('inicio'))

    return render_template('login.html', form=form_login)

@app.route("/listarReclamos", methods=["GET", "POST"])
@login_required
def listarReclamos():
    """
    Ruta que lista los reclamos del usuario actual.
    Si el filtro es 'mios', muestra todos los reclamos propios y adheridos (sin importar el estado).
    Si el filtro es 'todos', muestra todos los reclamos pendientes.
    Ambos casos pueden filtrarse por departamento.
    """
    username = current_user.nombre
    idUsuario = current_user.id

    filtroUsuario = request.form.get("filtroUsuario", "mios")
    filtroDepartamento = request.form.get("filtroDepartamento", "todos")

    if filtroUsuario == "todos":
        # Solo reclamos pendientes
        reclamosFiltrados = repoReclamo.obtenerRegistrosFiltro("estado", "pendiente")

    elif filtroUsuario == "mios":
        # Reclamos creados por el usuario (todos los estados)
        reclamosMios = repoReclamo.obtenerRegistrosFiltro("idUsuario", idUsuario)

        # Reclamos a los que se adhirió el usuario (todos los estados)
        todosReclamos = repoReclamo.obtenerRegistrosTotales()
        reclamosAdheridos = [r for r in todosReclamos if idUsuario in r.usuariosAdheridos]

        # Unir sin duplicados
        reclamosFiltrados = list({r.id: r for r in reclamosMios + reclamosAdheridos}.values())

    # Filtrar por departamento si corresponde
    if filtroDepartamento != "todos":
        reclamosFiltrados = [
            r for r in reclamosFiltrados if r.departamento == filtroDepartamento
        ]

    return render_template(
        "listarReclamos.html",
        reclamos=reclamosFiltrados,
        username=username,
        idUsuario=idUsuario,
        filtro_usuario=filtroUsuario
    )

@app.route("/adherir_a_reclamo/<int:idReclamo>", methods=["POST"])
@login_required
def adherir_a_reclamo(idReclamo):
    """
    Ruta para adherirse a un reclamo existente.
    Si el ID del reclamo es 0, se crea un nuevo reclamo.
    """
    idUsuario = current_user.id
    usuario = repoUsuario.obtenerRegistroFiltro("id", idUsuario)

    # Manejo especial para cancelar y volver
    if idReclamo == 99999999 and request.method == "POST":
        rutaImagen = request.form.get("rutaImagen")
        if rutaImagen and os.path.exists(rutaImagen):
            try:
                os.remove(rutaImagen)
            except Exception as e:
                print(f"Error al borrar imagen temporal: {e}")
        flash("Acción cancelada. No se creó ningún reclamo.", "success")
        return redirect(url_for("bienvenido"))
 
    #Si el ID es 0, significa "crear nuevo reclamo"
    if idReclamo == 0 and request.method == "POST":
        descripcion = request.form.get("descripcion")
        rutaImagen = request.form.get("rutaImagen")  # Recupera la ruta de la imagen
        if not descripcion:
            flash("La descripción del reclamo es obligatoria.", "error")
            return redirect(url_for("crearReclamos"))

        try:
            gestorReclamos.crearReclamo(idUsuario, descripcion, rutaImagen)
            flash("Reclamo creado con éxito", "success")
            return redirect(url_for('listarReclamos'))
        except ValueError as e:
            flash(str(e), "error")
    
    # Adherirse a un reclamo existente
    if idReclamo != 0:
        rutaImagen = request.form.get("rutaImagen")
        if rutaImagen and os.path.exists(rutaImagen):
            try:
                os.remove(rutaImagen)
            except Exception as e:
                # Opcional: loguear el error, pero no interrumpir el flujo
                print(f"Error al borrar imagen temporal: {e}")

        if gestorReclamos.adherirAReclamo(idReclamo, usuario):
            flash("Te has adherido exitosamente al reclamo.", "success")
        else:
            flash("No fue posible adherirse al reclamo (ya estás adherido o reclamo no existe).", "error")

    return redirect(url_for("listarReclamos"))


@app.route("/reclamos", methods=["GET", "POST"])
@login_required
def crearReclamos():
    """
    Ruta que renderiza la página de reclamos.
    Muestra los reclamos del usuario actual si está autenticado.
    """
    form = ReclamosForm()
    idUsuario = current_user.id
    username = current_user.nombre

    if form.validate_on_submit():
        descripcion = form.descripcion.data
        imagenFile = form.imagen.data  # esto es un FileStorage
        rutaImagen = None

        if imagenFile:
            carpeta_destino = os.path.join('data', 'imagenesReportes')
            os.makedirs(carpeta_destino, exist_ok=True)

            nombre_seguro = secure_filename(imagenFile.filename)
            rutaImagen = os.path.join(carpeta_destino, nombre_seguro)
            imagenFile.save(rutaImagen)

        try:
            reclamoSimilar = gestorReclamos.verificarReclamoExistente(idUsuario, descripcion)
            if reclamoSimilar:
                return render_template(
                    'adherirAReclamo.html',
                    reclamos=reclamoSimilar,
                    descripcionOriginal=descripcion,
                    rutaImagen=rutaImagen,
                    idUsuario=idUsuario
                )
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('crearReclamos'))

        try:
            gestorReclamos.crearReclamo(idUsuario, descripcion, rutaImagen)
            flash("Reclamo creado con éxito", "success")
            return redirect(url_for('listarReclamos'))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("nuevoReclamo.html", form=form, username=username)

@app.route("/panelAdmin", methods=["GET", "POST"])
@login_required
def panelAdmin():
    """
    Ruta para el panel de administración.
    Permite a los usuarios con rol de administrador gestionar reclamos.
    Se utiliza expresiones regulares para formatear el rol del usuario y obtener el departamento.
    """
    idUsuario = current_user.id
    username = current_user.nombre
    rol = current_user.rol
    departamento = None
    es_secretario = False

    #POST: procesar cambios en reclamos
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
        
        flash("Cambios guardados correctamente.", "success")      
        return redirect(url_for('panelAdmin'))

    #GET: mostrar página con los reclamos
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


@app.route('/data/<path:filename>')
def data_static(filename):
    """
    Ruta para servir archivos estáticos desde el directorio 'data'.
    """
    return send_from_directory('data', filename)

@app.route("/analitica")
@login_required
def analitica():
    """"
    Ruta para mostrar la analítica de reclamos.
    Muestra un gráfico con el porcentaje de reclamos por estado.
    Utiliza expresiones regulares para formatear el rol del usuario y obtener el departamento.
    """
    idUsuario = current_user.id
    rol = current_user.rol
    departamento = None
    if rol.startswith("jefe"):
        departamento = rol[4:]
        departamento = re.sub(r'(?<!^)(?=[A-Z])', ' ', departamento).lower()

    try:
        datosReporte = gestorReportes.generarReporte(departamento)
    except NoDataError as e:
        flash(str(e), "error")
        datosReporte = {}  #no hay datos para graficar

    if departamento == None:
        departamento = "Soporte Técnico"
    else:
        departamento = departamento.title()

    return render_template("analitica.html", datos=datosReporte, departamento=departamento)


@app.route("/descargar/<formato>")
@login_required
def descargarReporte(formato):
    """
    Ruta para descargar el reporte en el formato especificado.
    El formato puede ser 'pdf' o 'html'.
    Si el formato no es soportado, redirige a la página de inicio con un mensaje de error.
    """
    idUsuario = current_user.id
    if formato not in ['pdf', 'html']:
        flash("Formato no soportado")
        return redirect(url_for('inicio'))

    departamento = None
    rol = current_user.rol
    #obtener departamento si se trata de un jefe
    if rol.startswith("jefe"):
        departamento = rol[4:]
        departamento = re.sub(r'(?<!^)(?=[A-Z])', ' ', departamento).lower()
    #gestorExportacion=gestorExportacion
    ruta = gestorReportes.exportarReporte(formato, departamento)

    import os
    nombre_archivo = os.path.basename(ruta)
    return send_file(
        ruta,
        as_attachment=True,
        download_name=nombre_archivo,
        mimetype="application/pdf" if formato == "pdf" else "text/html"
    )

@app.route("/ayuda")
def ayuda():
    """
    Ruta para mostrar la página de ayuda.
    """
    return render_template("ayuda.html")

@app.route("/logout")
@login_required
def logout():
    """
    Ruta para cerrar sesión del usuario current_user.
    Limpia la sesión y redirige a la página de inicio.
    """
    idUsuario = current_user.id
    gestorLogin.logoutUsuario()
    flash("Has cerrado sesión exitosamente.", "success") 
    return redirect(url_for('inicio'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
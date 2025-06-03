#dependencias
from modules.usuario import Usuario
from modules.repositorioAbstractoBD import RepositorioAbstractoBD
from werkzeug.security import generate_password_hash, check_password_hash

class GestorUsuarios:
    """Clase para gestionar usuarios en el sistema.
    Permite registrar, loguear y cargar usuarios."""

    def __init__(self, repo: RepositorioAbstractoBD):
        self.__repo = repo

    def registrarUsuario(self, nombre, apellido, email, nombreUsuario, claustro, password):
        """ Registra un nuevo usuario en el sistema.
            args: nombre, apellido, email, nombreUsuario, claustro, password
        """
        #verifico si no está registrado
        if self.__repo.obtenerRegistroFiltro("email", email):
            raise ValueError("El usuario ya está registrado, por favor inicie sesión")

        #genero la contraseña hasheada
        passEncriptada = generate_password_hash(password= password,
                                                 method= 'pbkdf2:sha256',
                                                 salt_length=8
                                                )
        #genero la intancia de usuario CON ROL Y DEPARTAMENTO = None
        usuario = Usuario(None, nombre, apellido, email, nombreUsuario, claustro,
                          passEncriptada, rol=None, departamento=None)
        self.__repo.guardarRegistro(usuario)

    """POSIBLE SOLUCIÓN PARA REGISTRAR ADMINS"""
    # sólo accesible para admins
    # def crearAdmin(self, nombre, apellido, email, usuario, claustro, password, rol, departamento):
    #     admin = Usuario(
    #         nombre=nombre,
    #         apellido=apellido,
    #         email=email,
    #         username=usuario,
    #         claustro=claustro,
    #         password=hash(password),
    #         rol=rol,
    #         departamento=departamento
    #     )
    #     self.repo.guardar(admin)

    def autenticarUsuario(self, nombreUsuario, password) -> dict:
        """ Autentica un usuario con email y contraseña.
            args: email, password
        """
        usuario = self.__repo.obtenerRegistroFiltro("nombreUsuario", nombreUsuario)

        if not usuario:
            raise ValueError("El usuario no está registrado.")
        elif not check_password_hash(usuario.password, password):
            raise ValueError("Contraseña incorrecta.")
        return usuario.to_dict()
    
    def cargarUsuario(self, id_usuario):
        """ Carga un usuario por su ID.
            args: id_usuario
        """
        return self.__repo.obtenerRegistroFiltro("id", id_usuario).to_dict()
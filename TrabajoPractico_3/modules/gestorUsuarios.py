#dependencias
from modules.usuario import Usuario
from modules.repositorioAbstractoBD import RepositorioAbstractoBD
from werkzeug.security import generate_password_hash, check_password_hash

class GestorUsuarios:
    """
    Clase para gestionar usuarios en el sistema.
    Permite registrar, loguear y cargar usuarios.
    """

    def __init__(self, repo: RepositorioAbstractoBD): 
        self.__repo = repo

    def registrarUsuario(self, nombre, apellido, email, nombreUsuario, rol, password):
        """ Registra un nuevo usuario en el sistema.
            args: nombre, apellido, email, nombreUsuario, rol, password
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
        usuario = Usuario(id = None, nombre = nombre, apellido = apellido, email = email, nombreUsuario = nombreUsuario,
                          rol = rol, password = passEncriptada)
        self.__repo.guardarRegistro(usuario)

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
    
    def cargarUsuario(self, idUsuario):
        """ Carga un usuario por su ID.
            args: id_usuario
        """
        registro = self.__repo.obtenerRegistroFiltro("id", idUsuario) #devuelve un objeto Usuario o None
        return registro.to_dict() if registro else None
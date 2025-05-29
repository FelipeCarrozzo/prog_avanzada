#dependencias
from modules.usuario import Usuario
from modules.repositorioAbstractoBD import RepositorioAbstractoBD
from werkzeug.security import generate_password_hash, check_password_hash

class GestorUsuarios:
    def __init__(self, repo: RepositorioAbstractoBD):
        self.__repo = repo 
    def registrarUsuario(self, nombre, apellido, nombreUsuario, email, password, rol, claustro, departamento: None):
        """
        Registra un nuevo usuario en el sistema.
        args: nombre, email, password
        """
        #verifico si no está registrado
        if self.__repo.obtenerRegistroFiltro("email", email):
            raise ValueError("El usuario ya está registrado, por favor inicie sesión")
        #genero la contraseña hasheada
        passEncriptada = generate_password_hash(password= password,
                                                 method= 'pbkdf2:sha256',
                                                 salt_length=8
                                                )
        #genero la intancia de usuario
        usuario = Usuario(None, nombre, apellido, nombreUsuario, email, passEncriptada, rol, claustro, departamento)
        self.__repo.guardarRegistro(usuario)

    def loguearUsuario(self, email, password):
        #busco el mail ingresado por el usuario
        usuario = self.__repo.obtenerRegistroFiltro("email", email)

        if not usuario:
            raise ValueError("El usuario no está registrado.")
        elif not check_password_hash(usuario.password, password):
            raise ValueError("Contraseña incorrecta.")
        return usuario.to_dict()
    
    def cargarUsuario(self, id_usuario):
        return self.__repo.obtenerRegistroFiltro("id", id_usuario).to_dict()
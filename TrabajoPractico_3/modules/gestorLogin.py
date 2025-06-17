#dependencias
from flask_login import UserMixin
from flask_login import login_user, logout_user, current_user


class FlaskLoginUser(UserMixin):
    """
    Clase que representa un usuario para Flask-Login.
    Hereda de UserMixin para integrarse con Flask-Login.
    Atributos:
        id: ID del usuario.
        nombre: Nombre del usuario.
        email: Email del usuario.
        rol: Rol del usuario.
        password: Contraseña del usuario (encriptada).
    """

    def __init__(self, diccUsuario):
        self.id = diccUsuario["id"]
        self.nombre = diccUsuario["nombre"]
        self.email = diccUsuario["email"]
        self.rol = diccUsuario["rol"]
        self.password = diccUsuario["password"]

class GestorDeLogin:
    """Clase para gestionar el login de usuarios en la aplicación."""
    def __init__(self, gestorUsuarios, loginManager, adminList):
        self.__gestorUsuarios = gestorUsuarios
        loginManager.user_loader(self.__cargarUsuarioActual)
        self.__adminList = adminList

    @property
    def idUsuarioActual(self):
        return current_user.id

    @property
    def nombreUsuarioActual(self):
        return current_user.nombre

    @property
    def rolUsuarioActual(self):
        return current_user.rol

    @property
    def usuarioAutenticado(self):
        return current_user.is_authenticated

    def __cargarUsuarioActual(self, idUsuario):
        """Carga el usuario actual desde la base de datos."""
        usuario = self.__gestorUsuarios.cargarUsuario(idUsuario)
        if usuario:
            return FlaskLoginUser(usuario)
        return None

    def loginUsuario(self, diccUsuario):
        """Inicia sesión para el usuario con los datos proporcionados."""
        user = FlaskLoginUser(diccUsuario)
        login_user(user)
        print(f"Usuario {current_user.nombre} ha iniciado sesión")

    def obtenerRolUsuario(self):
        """Obtiene el rol del usuario actual."""
        if current_user.is_authenticated:
            return current_user.rol
        return None

    def logoutUsuario(self):
        """Cierra sesión del usuario actual."""
        logout_user()
        print("Usuario ha cerrado sesión")
        print(f"Usuario actual {current_user}")
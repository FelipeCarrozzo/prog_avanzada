#dependencias
from flask_login import UserMixin
from flask_login import login_user, logout_user, login_required, current_user
from flask import abort
from functools import wraps

class FlaskLoginUser(UserMixin):
    """Clase que representa un usuario para Flask-Login.
    Hereda de UserMixin para integrarse con Flask-Login.
    Atributos:
        id: ID del usuario.
        nombre: Nombre del usuario.
        email: Email del usuario.
        password: Contraseña del usuario (encriptada).
    """
    def __init__(self, diccUsuario):
        self.id = diccUsuario["id"]
        self.nombre = diccUsuario["nombre"]
        self.email = diccUsuario["email"]
        self.password = diccUsuario["password"]

class GestorDeLogin:
    """Clase para gestionar el login de usuarios en la aplicación."""
    def __init__(self, gestorUsuarios, loginManager, adminList):
        self.__gestorUsuarios = gestorUsuarios
        loginManager.user_loader(self.__cargarUsuarioActual)
        self.__adminList = adminList

    @property
    def nombre_usuarioActual(self):
        return current_user.nombre

    @property
    def id_usuarioActual(self):
        return current_user.id
    
    @property
    def usuarioAutenticado(self):
        return current_user.is_authenticated

    def __cargarUsuarioActual(self, idUsuario):
        """Carga el usuario actual desde la base de datos."""
        diccUsuario = self.__gestorUsuarios.cargarUsuario(idUsuario)
        return FlaskLoginUser(diccUsuario)

    def login_usuario(self, diccUsuario):
        """Inicia sesión para el usuario con los datos proporcionados."""
        user = FlaskLoginUser(diccUsuario)
        login_user(user)
        print(f"Usuario {current_user.nombre} ha iniciado sesión")

    def logout_usuario(self):
        """Cierra sesión del usuario actual."""
        logout_user()
        print("Usuario ha cerrado sesión")
        print(f"Usuario actual {current_user}")

    # def admin_only(self, f):
    #     @wraps(f)
    #     def decorated_function(*args, **kwargs):
    #         if current_user.is_authenticated and current_user.id not in self.__adminList:
    #             return abort(403)
    #         return f(*args, **kwargs)
    #     return decorated_function
    
    # def se_requiere_login(self, func):
    #     return login_required(func)
    
    # def es_admin(self):
    #     if current_user.is_authenticated and current_user.id in self.__admin_list:
    #         return True
    #     else:
    #         return False
"""ELIMINAR: Este módulo está obsoleto y no se utiliza en el proyecto actual."""
#dependencias
# from usuario import Usuario
# from repositorioAbstractoBD import RepositorioAbstractoBD
# from werkzeug.security import generate_password_hash, check_password_hash

# class GestorUsuarios:
#     """Clase para gestionar usuarios en el sistema.
#     Permite registrar, loguear y listar usuarios."""

#     def __init__(self, repo: RepositorioAbstractoBD): #repo = instancia de RepositorioUsuariosBD
#         self.__repo = repo 

#     def registrarUsuario(self, nombre, email, password):
#         """
#         Registra un nuevo usuario en el sistema.
#         args: nombre, email, password
#         """
#         #verifico si no está registrado
#         if self.__repo.obtenerRegistroFiltro("email", email):
#             raise ValueError("El usuario ya está registrado, por favor inicie sesión")
#         #genero la contraseña hasheada
#         passEncriptada = generate_password_hash(password= password,
#                                                  method= 'pbkdf2:sha256',
#                                                  salt_length=8
#                                                 )
#         #genero la intancia de usuario
#         usuario = Usuario(None, nombre, email, passEncriptada)
#         self.__repo.guardarRegistro(usuario)

#     def loguearUsuario(self, email, password):
#         #busco el mail ingresado por el usuario
#         usuario = self.__repo.obtenerRegistroFiltro("email", email)
#         if not usuario:
#             raise ValueError("El usuario no está registrado.")
#         elif not check_password_hash(usuario.password, password):
#             raise ValueError("Contraseña incorrecta.")
#         return usuario.to_dict()

#     def listarUsuarios(self) -> list:
#         return self.usuarios
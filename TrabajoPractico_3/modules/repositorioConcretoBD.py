#dependencias
from modules.repositorioAbstractoBD import RepositorioAbstractoBD
from modules.modelosDTO import ModeloUsuario
from modules.usuario import Usuario

class RepositorioUsuariosBD(RepositorioAbstractoBD):
    def __init__(self, session):
        self.__tabla_usuario = ModeloUsuario()
        self._session = session
        self.__tabla_usuario.metadata.create_all(self._session.bind)
    
    def guardar_registro(self, usuario):
        """
        Guarda un registro de un usuario en la base de datos.

        Args:
            usuario(Usuario): usuario a guardar en el registro. 
        """
        if not isinstance(usuario, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        modelo_usuario = self.__map_usuario_a_modelo(usuario)
        self._session.add(modelo_usuario)
        self._session.commit()

    def __map_usuario_a_modelo(self, usuario: Usuario):
        return ModeloUsuario(
            # Cuándo se genera el id automáticamente?
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            email=usuario.email,
            claustro=usuario.claustro,
            nombreUsuario=usuario.nombreUsuario,
            password=usuario.password,
            rol=usuario.rol,
            departamento=usuario.departamento
        )
        
    def __map_modelo_a_usuario(self, modelo_usuario: ModeloUsuario):
        return Usuario(
            id=modelo_usuario.id,
            nombre=modelo_usuario.nombre,
            apellido=modelo_usuario.apellido,
            email=modelo_usuario.email,
            nombreUsuario=modelo_usuario.nombre_de_usuario,
            claustro=modelo_usuario.claustro,
            password=modelo_usuario.password,  
            rol=modelo_usuario.rol,
            departamento=modelo_usuario.departamento
        )


class RepositorioReclamosBD(RepositorioAbstractoBD):
    pass

class RepositorioDepartamentosBD(RepositorioAbstractoBD):
    pass


#dependencias
from modules.repositorioAbstractoBD import RepositorioAbstractoBD
from modules.modelosDTO import ModeloUsuario
from modules.usuario import Usuario

class RepositorioUsuariosBD(RepositorioAbstractoBD):
    """Repositorio de usuarios en la base de datos.
    Hereda de RepositorioAbstractoBD para implementar operaciones CRUD.
    """

    def __init__(self, session):
        self.__tabla_usuario = ModeloUsuario()
        self.__session = session
        self.__tabla_usuario.metadata.create_all(self.__session.bind)
    
    def guardarRegistro(self, usuario):
        """
        Guarda un registro de un usuario en la base de datos.

        Args:
            usuario(Usuario): usuario a guardar en el registro. 
        """
        if not isinstance(usuario, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        
        modelo_usuario = self.__map_usuario_a_modelo(usuario)
        self.__session.add(modelo_usuario)
        #tabla intermedia - para cuando IMPLEMENTEMOS EL RECLAMO
        # usuario = self.__session.query(ModeloUsuario).filter_by(id=reclamo.idUsuario).first()
        # usuario.reclamosSeguidos.apend(modeloReclamo)
        self.__session.commit()

    def actualizarAtributo(self, id, atributo, valor):
        """
        Método abstracto para actualizar un atributo de un registro en la base de datos.

        param id: Identificador del registro a actualizar.
        param atributo: Nombre del atributo a actualizar.
        param valor: Nuevo valor del atributo.
        """
        pass

    def obtenerRegistroFiltro(self, filtro, valor):
        """
        Método abstracto para obtener un registro de la base de datos basado en un filtro.

        args:
        filtro: Filtro para buscar el registro.
        valor: valor que se desea encontrar.
        return: Registro que coincide con el filtro.
        """
        modeloUsuario = self.__session.query(ModeloUsuario).filter_by(**{filtro:valor}).first()
        return self.__map_modelo_a_usuario(modeloUsuario) if modeloUsuario else None


    def obtenerRegistrosFiltro(self, filtro):
        """
        Método abstracto para obtener múltiples registros de la base de datos basados en un filtro.

        param filtro: Filtro para buscar los registros.
        return: Lista de registros que coinciden con el filtro.
        """
        pass

    def obtenerRegistrosTotales(self):
        """
        Método abstracto para obtener todos los registros de la base de datos.

        return: Lista de todos los registros.
        """
        pass

#---------------------------------------------------------------------------

    def __map_usuario_a_modelo(self, usuario: Usuario):
        return ModeloUsuario(
            # Cuándo se genera el id automáticamente?
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            email=usuario.email,
            nombreUsuario=usuario.nombreUsuario,
            claustro=usuario.claustro,
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
            nombreUsuario=modelo_usuario.nombreUsuario,
            claustro=modelo_usuario.claustro,
            password=modelo_usuario.password,  
            rol=modelo_usuario.rol,
            departamento=modelo_usuario.departamento
        )


# class RepositorioReclamosBD(RepositorioAbstractoBD):
#     pass

# class RepositorioDepartamentosBD(RepositorioAbstractoBD):
#     pass


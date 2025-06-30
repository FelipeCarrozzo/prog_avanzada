#dependencias
from abc import ABC, abstractmethod

class RepositorioAbstractoBD(ABC):
    """Clase abstracta que define la interfaz para un repositorio de base de datos."""

    def __init__(self, session):
        """
        Inicializa el repositorio con una conexión a la base de datos.
        Param:
            session: Sesión de conexión a la base de datos.        
        """
        self.__session = session

    @abstractmethod
    def guardarRegistro(self, registro):
        """
        Método abstracto para guardar un registro en la base de datos.
        
        param registro: El registro a guardar.
        """
        pass
    
    @abstractmethod
    def actualizarAtributo(self, id, atributo, valor):
        """
        Método abstracto para actualizar un atributo de un registro en la base de datos.

        param id: Identificador del registro a actualizar.
        param atributo: Nombre del atributo a actualizar.
        param valor: Nuevo valor del atributo.
        """
        pass

    @abstractmethod
    def obtenerRegistroFiltro(self, filtro, valor):
        """
        Método abstracto para obtener un registro de la base de datos basado en un filtro.

        param filtro: Filtro para buscar el registro.
        param valor: Valor a buscar.
        return: Registro que coincide con el filtro.
        """
        pass

    @abstractmethod
    def obtenerRegistrosFiltro(self, filtro, valor):
        """
        Método abstracto para obtener múltiples registros de la base de datos basados en un filtro.

        param filtro: Filtro para buscar los registros.
        param valor: Valor a buscar.
        return: Lista de registros que coinciden con el filtro.
        """
        pass

    @abstractmethod
    def obtenerRegistrosTotales(self):
        """
        Método abstracto para obtener todos los registros de la base de datos.

        return: Lista de todos los registros.
        """
        pass
    
    @abstractmethod
    def eliminarRegistro(self, id):
        """
        Elimina un registro de la base de datos por su id.
        """
        pass

    @abstractmethod
    def eliminarTabla(self, nombreTabla):
        """
        Elimina una tabla de la base de datos por su nombre.
        """
        pass
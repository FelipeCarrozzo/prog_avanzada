#dependencias
from modules.repositorioAbstractoBD import RepositorioAbstractoBD
from modules.modelosDTO import ModeloUsuario, ModeloReclamo
from modules.usuario import Usuario
from modules.reclamo import Reclamo

class RepositorioUsuariosBD(RepositorioAbstractoBD):
    """Repositorio de usuarios en la base de datos.
    Hereda de RepositorioAbstractoBD para implementar operaciones CRUD.
    """

    def __init__(self, session):
        self.__tablaUsuario = ModeloUsuario
        self.__session = session
        self.__tablaUsuario.metadata.create_all(self.__session.bind)
    
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
        self.__session.commit()

    def actualizarAtributo(self, id, atributo, valor):
        """
        Método para actualizar un atributo de un registro en 
        la tabla Usuarios.
        args:
        id: Identificador del registro a actualizar.
        atributo: Nombre del atributo a actualizar.
        valor: Nuevo valor del atributo.
        """
        instancia = self.__session.get(self.__tablaUsuario, id)

        if not instancia:
            raise ValueError(f"Error: Instancia con id {id} no existe.")
        
        setattr(instancia, atributo, valor)
        self.__session.commit()

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

    def obtenerModeloPorId(self, id):
        """
        Método para obtener un modelo de usuario por su id.
        """
        return self.__session.get(ModeloUsuario, id)

    def obtenerRegistrosFiltro(self, filtro, valor):
        """
        Método para obtener conjunto de registros de la 
        base de datos basados en un filtro.

        args:
        filtro: Filtro para buscar los registros.
        return: Lista de registros que coinciden con el filtro.
        """
        if isinstance(valor, list) and len(valor) > 0:
            valor = valor[0] 
        modeloUsuario = self.__session.query(ModeloUsuario).filter_by(**{filtro: valor}).all()

        if modeloUsuario:
            return [self.__map_modelo_a_usuario(usuario) for usuario in modeloUsuario]
        #si no hay resultados: devuelve lista vacia
        return [] 

    def obtenerRegistrosTotales(self):
        """
        Método abstracto para obtener todos los registros de la base de datos.

        return: Lista de todos los registros.
        """
        modeloUsuario = self.__session.query(ModeloUsuario).all()
        return [self.__map_modelo_a_usuario(usuario) for usuario in modeloUsuario]

    def eliminarRegistro(self, idUsuario):
        """
        Elimina un usuario de la base de datos por su id.
        Args:
            idUsuario: id del usuario a eliminar.
        """
        usuario = self.__session.query(ModeloUsuario).filter_by(id=idUsuario).first()
        if usuario:
            self.__session.delete(usuario)
            self.__session.commit()
            return True
        return False
    
    def borrarTabla(self, nombre_tabla: str):
        """
        Elimina una tabla de la base de datos por su nombre.
        Args:
            nombre_tabla (str): Nombre de la tabla a eliminar.
        """
        from sqlalchemy import text
        try:
            self.__session.execute(text(f"DROP TABLE IF EXISTS {nombre_tabla}"))
            self.__session.commit()
            print(f"Tabla '{nombre_tabla}' eliminada correctamente.")
        except Exception as e:
            print(f"Error al eliminar la tabla '{nombre_tabla}': {e}")
    

#---------------------------------------------------------------------------

    def __map_usuario_a_modelo(self, usuario: Usuario):
        return ModeloUsuario(
            # Cuándo se genera el id automáticamente?
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            email=usuario.email,
            nombreUsuario=usuario.nombreUsuario,
            rol=usuario.rol,
            password=usuario.password
        )
        
    def __map_modelo_a_usuario(self, modeloUsuario: ModeloUsuario):
        return Usuario(
            id=modeloUsuario.id,  # Asumiendo que el modelo tiene un campo id
            nombre=modeloUsuario.nombre,
            apellido=modeloUsuario.apellido,
            email=modeloUsuario.email,
            nombreUsuario=modeloUsuario.nombreUsuario,
            rol=modeloUsuario.rol,
            password=modeloUsuario.password
        )


class RepositorioReclamosBD(RepositorioAbstractoBD):
    """Repositorio de reclamos en la base de datos."""
    def __init__(self, session):
        self.__tablaReclamo = ModeloReclamo
        self.__session = session
        self.__tablaReclamo.metadata.create_all(self.__session.bind)
    
    def guardarRegistro(self, reclamo):
        """Guarda un registro de un reclamo en la base de datos.
        Args:
        reclamo(Reclamo): reclamo a guardar en el registro. """
        
        # Verifica que el reclamo sea una instancia de la clase Reclamo
        if not isinstance(reclamo, Reclamo):
            raise ValueError("El parámetro no es una instancia de la clase Reclamo")
        
        modeloReclamo = self.__map_reclamo_a_modelo(reclamo)
        self.__session.add(modeloReclamo)
        self.__session.commit()
        #tabla intermedia - para cuando IMPLEMENTEMOS EL RECLAMO
        # usuario = self.__session.query(ModeloUsuario).filter_by(id=reclamo.idUsuario).first()
        # usuario.reclamosSeguidos.apend(modeloReclamo)

    def actualizarAtributo(self, id, atributo, valor):
        """
        Método abstracto para actualizar un atributo de un registro en la base de datos.

        param id: Identificador del registro a actualizar.
        param atributo: Nombre del atributo a actualizar.
        param valor: Nuevo valor del atributo.
        """
        instancia = self.__session.get(ModeloReclamo, id)


        if not instancia:
            raise ValueError(f"Error: Instancia con id {id} no existe.")
        
        setattr(instancia, atributo, valor)
        self.__session.commit()

    def agregarUsuarioAReclamo(self, idReclamo, usuarioDominio):
        usuarioModelo = self.__session.query(ModeloUsuario).get(usuarioDominio.id)
        reclamo = self.__session.get(ModeloReclamo, idReclamo)

        if not reclamo:
            raise ValueError(f"No se encontró reclamo con ID {idReclamo}")
        if not usuarioModelo:
            raise ValueError(f"No se encontró usuario con ID {usuarioDominio.id}")

        if usuarioModelo not in reclamo.usuariosAdheridos:
            reclamo.usuariosAdheridos.append(usuarioModelo)
            reclamo.numeroAdheridos = len(reclamo.usuariosAdheridos)
            self.__session.commit()
            return True
        return False

    def obtenerRegistroFiltro(self, filtro, valor):
        """
        Método abstracto para obtener un registro de la base de datos basado en un filtro.

        param filtro: Filtro para buscar el registro.
        return: Registro que coincide con el filtro.
        """
        modeloReclamo = self.__session.query(ModeloReclamo).filter_by(**{filtro:valor}).first()
        return self.__map_modelo_a_reclamo(modeloReclamo) if modeloReclamo else None

    def obtenerRegistrosFiltro(self, filtro, valor):
        """
        Método abstracto para obtener múltiples registros de la base de datos basados en un filtro.

        param filtro: Filtro para buscar los registros.
        return: Lista de registros que coinciden con el filtro.
        """
        if isinstance(valor, list) and len(valor) > 0:
            valor = valor[0] 
        modeloReclamo = self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).all()

        if modeloReclamo:
            return [self.__map_modelo_a_reclamo(reclamo) for reclamo in modeloReclamo]
        #si no hay resultados: devuelve lista vacia
        return [] 

    def obtenerRegistrosTotales(self):
        """
        Método abstracto para obtener todos los registros de la base de datos.

        return: Lista de todos los registros.
        """
        modeloReclamo = self.__session.query(ModeloReclamo).all()
        return [self.__map_modelo_a_reclamo(reclamo) for reclamo in modeloReclamo]

    def eliminarRegistro(self, id):
        """
        Elimina un reclamo de la base de datos por su id.
        Args:
            id: id del reclamo a eliminar.
        """
        reclamo = self.__session.query(ModeloReclamo).filter_by(id=id).first()
        if reclamo:
            self.__session.delete(reclamo)
            self.__session.commit()
            return True
        return False
 
    def borrarTabla(self, nombre_tabla: str):
        """
        Elimina una tabla de la base de datos por su nombre.
        Args:
            nombre_tabla (str): Nombre de la tabla a eliminar.
        """
        from sqlalchemy import text
        try:
            self.__session.execute(text(f"DROP TABLE IF EXISTS {nombre_tabla}"))
            self.__session.commit()
            print(f"Tabla '{nombre_tabla}' eliminada correctamente.")
        except Exception as e:
            print(f"Error al eliminar la tabla '{nombre_tabla}': {e}")
    #--------------------------------------------------------------------------

    def __map_reclamo_a_modelo(self, reclamo: Reclamo):
        modelo = ModeloReclamo(
            idUsuario=reclamo.idUsuario,  # id del usuario creador
            fechaYHora=reclamo.fechaYHora,
            estado=reclamo.estado,
            tiempoResolucion=reclamo.tiempoResolucion,
            departamento=reclamo.departamento,
            numeroAdheridos=reclamo.numeroAdheridos,
            descripcion=reclamo.descripcion,
            imagen=reclamo.imagen
        )
        modelo.usuariosAdheridos = reclamo.usuariosAdheridos
        return modelo
    
    def __map_modelo_a_reclamo(self, modeloReclamo: ModeloReclamo):
        return Reclamo(
            id = modeloReclamo.id, 
            idUsuario=modeloReclamo.idUsuario,
            fechaYHora=modeloReclamo.fechaYHora,
            estado=modeloReclamo.estado,
            tiempoResolucion=modeloReclamo.tiempoResolucion,
            departamento=modeloReclamo.departamento,
            numeroAdheridos=modeloReclamo.numeroAdheridos,
            descripcion=modeloReclamo.descripcion,
            imagen=modeloReclamo.imagen,
            usuariosAdheridos=[u.id for u in modeloReclamo.usuariosAdheridos]
        )
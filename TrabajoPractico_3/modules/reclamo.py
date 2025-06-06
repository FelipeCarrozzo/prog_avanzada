#capa de dominio

class Reclamo:
    def __init__(self, idReclamo, pFechaYHora, pEstado, pTiempoResolucion, pDepartamento, 
                 pUsuarioCreador, pNumeroAdheridos, pUsuariosAdheridos, pDescripcion, pImagen):
        self.__idReclamo = idReclamo
        self.__fechaYHora = pFechaYHora
        self.__estado = pEstado
        self.__tiempoDeResolucion = pTiempoResolucion
        self.__departamento = pDepartamento
        self.__idUsuarioCreador = pUsuarioCreador #id del usuario en lugar del objeto Usuario?
        self.__usuariosAdheridos = pUsuariosAdheridos #list[Usuario]
        self.__numeroAdheridos = pNumeroAdheridos
        self.__descripcion = pDescripcion
        self.__imagen = pImagen

    @property
    def idReclamo(self):
        return self.__idReclamo

    #@idReclamo.setter
    
    @property
    def idUsuarioCreador(self):
        return self.__idUsuarioCreador

    @property
    def descripcion(self):
        return self.__descripcion
    
    @property
    def estado(self):
        return self.__estado
    
    @property
    def fechaYHora(self):
        return self.__fechaYHora

    @property
    def departamento(self):
        return self.__departamento
    
    @departamento.setter
    def departamento(self, value):
        self.__departamento = value

    @property
    def tiempoDeResolucion(self):
        return self.__tiempoDeResolucion

    @tiempoDeResolucion.setter
    def tiempoDeResolucion(self, value):
        if value is not None and value < 0:
            raise ValueError("El tiempo de resolución debe ser positivo.")
        self.__tiempoDeResolucion = value

    @property
    def usuariosAdheridos(self):
        return self.__usuariosAdheridos
    
    @property
    def numeroAdheridos(self):
        return self.__numeroAdheridos
    
    # @numeroAdheridos.setter

    @property
    def imagen(self):
        return self.__imagen

    @estado.setter
    def estado(self, value):
        estadosValidos = ['pendiente', 'en proceso', 'resuelto', 'invalido']
        if value not in estadosValidos:
            raise ValueError(f"Estado inválido: '{value}'. Los estados permitidos son: {', '.join(estadosValidos)}.")
        self.__estado = value

    def to_dict(self):
        #actualizar cuando se definan bien los atributos
        return {
            "idReclamo": self.idReclamo,
            "idUsuarioCreador": self.idUsuarioCreador,
            "descripcion": self.descripcion,
            "departamento": self.departamento,
            "fechaHora": self.fechaYHora,
            "estado": self.estado,
            "tiempoDeResolucion": self.tiempoDeResolucion,
            "numeroAdheridos": self.numeroAdheridos,
            "usuariosAdheridos": [usuario.to_dict() for usuario in self.usuariosAdheridos],
            "imagen": self.imagen
        }
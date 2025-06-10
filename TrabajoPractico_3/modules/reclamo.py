#capa de dominio

class Reclamo:
    def __init__(self, id, idUsuario, fechaYHora, estado, tiempoResolucion, departamento, 
                 numeroAdheridos, usuariosAdheridos, descripcion, imagen):

        self.__id = id
        self.__idUsuario = idUsuario
        self.__fechaYHora = fechaYHora
        self.__estado = estado
        self.tiempoResolucion = tiempoResolucion
        self.__departamento = departamento
        self.__idAdheridos = []  # Lista de IDs de usuarios adheridos
        self.__numeroAdheridos = numeroAdheridos
        self.__descripcion = descripcion
        self.__imagen = imagen

    @property
    def id(self):
        return self.__id
    
    @property
    def idUsuario(self):
        return self.__idUsuario 

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
    def tiempoResolucion(self):
        return self.__tiempoResolucion

    @tiempoResolucion.setter
    def tiempoResolucion(self, value):
        if value is not None and value < 0:
            raise ValueError("El tiempo de resolución debe ser positivo.")
        self.__tiempoResolucion = value

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
        return {
            "id": self.__id,
            "idUsuario": self.__idUsuario,
            "fechaYHora": self.__fechaYHora,
            "estado": self.__estado,
            "tiempoResolucion": self.__tiempoResolucion,
            "departamento": self.__departamento,
            "idAdheridos": self.__idAdheridos,
            "numeroAdheridos": self.__numeroAdheridos,
            "descripcion": self.__descripcion,
            "imagen": self.__imagen
        }
    

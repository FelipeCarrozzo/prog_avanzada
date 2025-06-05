#capa de dominio
class Usuario:
    def __init__(self, nombre, apellido, email, nombreUsuario, rol=None, password=None):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__nombreUsuario = nombreUsuario
        self.__rol = rol #usuarioFinal, jefeDepartamento, secretarioTecnico
        self.__password = password


    # @property
    # def id(self):
    #     return self.__id
    
    #setter id?
    
    @property
    def nombre(self):
        return self.__nombre
        
    @property
    def apellido(self):
        return self.__apellido

    @property
    def email(self):
        return self.__email
    
    @property
    def nombreUsuario(self):
        return self.__nombreUsuario
    
    @property
    def rol(self):
        return self.__rol
    
    def to_dict(self):
        """
        Serializa el usuario en un diccionario.
        Returns:
            dict: Representación del usuario como un diccionario.
        """
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "nombreUsuario": self.nombreUsuario,
            "rol": self.rol,
            "password": self.password
        }
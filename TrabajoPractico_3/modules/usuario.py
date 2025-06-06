#capa de dominio
class Usuario:
    def __init__(self, id, nombre, apellido, email, nombreUsuario, rol=None, password=None):
        self.__id = id
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__nombreUsuario = nombreUsuario
        self.__rol = rol #usuarioFinal, jefeDepartamento, secretarioTecnico
        self.__password = password


    @property
    def id(self):
        return self.__id

    def get_id(self):
        """
        Obtiene el ID del usuario.
        Returns:
            int: ID del usuario.
        """
        return str(self.__id) # Flask-Login requiere que el ID sea un string

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
    
    @property
    def password(self):
        return self.__password
    
    def to_dict(self):
        """
        Serializa el usuario en un diccionario.
        Returns:
            dict: Representación del usuario como un diccionario.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "nombreUsuario": self.nombreUsuario,
            "rol": self.rol,
            "password": self.password
        }
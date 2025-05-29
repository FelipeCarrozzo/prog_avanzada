#capa de dominio
class Usuario:
    def __init__(self, id, nombre, apellido, email, pNombreUsuario, claustro, password, rol):
        
        self.__id = None #revisar
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__nombreUsuario = pNombreUsuario
        self.__claustro = claustro #estudiante, docente, PAyS
        self.__password = password
        self.__rol = rol #usuarioFinal, jefeDepartamento, secretarioTecnico
        self.__departamento = None #es None si se trata de un usuarioFinal


    @property
    def id(self):
        return self.__id
    
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
    def claustro(self):
        return self.__claustro
    
    @property
    def password(self):
        return self.__password
    
    @property
    def rol(self):
        return self.__rol
    
    @property
    def departamento(self):
        return self.__departamento
    
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
            "claustro": self.claustro,
            "password": self.password,
            "rol": self.rol,
            "departamento": self.__departamento,
            
        }
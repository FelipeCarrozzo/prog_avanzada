class Persona:
    def __init__(self, nombre, apellido, dni):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if nuevo_nombre.strip() == "":
            raise ValueError("El nombre no puede ser una cadena vacía")
        self.__nombre = nuevo_nombre

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, nuevo_apellido):
        if nuevo_apellido.strip() == "":
            raise ValueError("El apellido no puede ser una cadena vacía")
        self.__apellido = nuevo_apellido

    @property
    def dni(self):
        return self.__dni

    def __str__(self):
        return f"{self.__nombre} {self.__apellido}, DNI: {self.__dni}"
class Estudiante:
    def __init__(self, nombre, apellido, dni):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni
        self.__facultades = []
        self.__cursos = []

    def inscribir_facultad(self, facultad):
        if facultad not in self.facultades:
            self.facultades.append(facultad)

    def __str__(self):
        return f"{self.__nombre} {self.__apellido}, DNI: {self.__dni}"
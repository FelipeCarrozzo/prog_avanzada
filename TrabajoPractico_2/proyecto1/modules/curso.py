class Curso:
    def __init__(self, nombre, codigo, titular):
        self.__nombre = nombre
        self.__codigo = codigo
        self.__titular = titular  # Profesor
        self.__estudiantes = []

    def inscribir_estudiante(self, estudiante):
        if estudiante not in self.estudiantes:
            self.estudiantes.append(estudiante)

    def __str__(self):
        return f"Curso: {self.__nombre}, Código: {self.__codigo}, Titular: {self.__titular}"
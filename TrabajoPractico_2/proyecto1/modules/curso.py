class Curso:
    def __init__(self, nombre, codigo, titular):
        self.__nombre = nombre
        self.__codigo = codigo
        self.__titular = titular  # Profesor
        self.__estudiantes = []

    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def codigo(self):
        return self.__codigo
    
    @property
    def titular(self):
        return self.__titular
    
    @property
    def estudiantes(self):
        return self.__estudiantes

    def inscribir_estudiante(self, p_estudiante):
        if p_estudiante not in self.__estudiantes:
            self.__estudiantes.append(p_estudiante)
        else:
            raise ValueError("El estudiante ya está inscrito en el curso.")

    def __str__(self):
        return f"Curso: {self.__nombre}, Código: {self.__codigo}, Titular: {self.__titular}"
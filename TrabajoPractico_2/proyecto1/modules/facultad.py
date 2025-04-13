class Facultad:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__departamentos = []
        self.__estudiantes = []
        self.__profesores = []

    def agregar_estudiante(self, estudiante):
        if estudiante not in self.__estudiantes:
            self.__estudiantes.append(estudiante)

    def listar_estudiantes(self):
        return [str(estudiante) for estudiante in self.__estudiantes]

    def __str__(self):
        return self.__nombre

    def contratar_profesor(self, profesor):
        if profesor not in self.__profesores:
            self.__profesores.append(profesor)

    def listar_profesores(self):
        return [str(profesor) for profesor in self.__profesores]
    
    def agregar_departamento(self, departamento):
        if departamento not in self.__departamentos:
            self.__departamentos.append(departamento)
    
    def listar_departamentos(self):
        return [str(departamento) for departamento in self.__departamentos]
    
    def get_nombre(self):
        return self.__nombre
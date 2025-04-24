class Facultad:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__departamentos = []
        self.__estudiantes = []
        self.__profesores = []

    @property
    def nombre(self):
        return self.__nombre

    @property
    def estudiantes(self):
        return self.__estudiantes

    @property
    def departamentos(self):
        return self.__departamentos

    @property
    def profesores(self):
        return self.__profesores
    
    def agregar_estudiante(self, p_estudiante):
        if p_estudiante not in self.__estudiantes:
            self.__estudiantes.append(p_estudiante)

    def listar_estudiantes(self):
        return [str(estudiante) for estudiante in self.__estudiantes]

    def contratar_profesor(self, p_profesor):
        if p_profesor not in self.__profesores:
            self.__profesores.append(p_profesor)

    def listar_profesores(self):
        return [str(profesor) for profesor in self.__profesores]
    
    def agregar_departamento(self, p_departamento):
        if p_departamento not in self.__departamentos:
            self.__departamentos.append(p_departamento)
    
    def listar_departamentos(self):
        return [str(departamento) for departamento in self.__departamentos]
    
    def obtener_cursos_con_departamento(self):
        cursos = []
        for depto in self.__departamentos:
            for curso in depto.cursos:
                cursos.append((curso, depto))
        return cursos
    
    def __str__(self):
        return self.__nombre
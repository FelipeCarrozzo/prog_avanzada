class Departamento:
    def __init__(self, nombre, director):
        self.__nombre = nombre
        self.__director = director  #Profesor
        self.__profesores = [director]  # al menos contiene al director
        self.__cursos = []

    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def director(self):
        return self.__director
    
    @property
    def profesores(self):
        return self.__profesores
    
    @property
    def cursos(self):
        return self.__cursos

    def agregar_profesor(self, profesor):
        if profesor not in self.__profesores:
            self.__profesores.append(profesor)

    def listar_profesores(self):
        return [str(profesor) for profesor in self.__profesores]
    
    def agregar_curso(self, curso):
        self.__cursos.append(curso)

    def listar_cursos(self):
        return [str(curso) for curso in self.__cursos]
    
    def __str__(self):
        return f"Departamento: {self.__nombre}, Director: {self.__director}"
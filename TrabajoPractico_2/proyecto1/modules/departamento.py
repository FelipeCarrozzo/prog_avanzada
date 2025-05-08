from modules.persona import Profesor

class Departamento:
    def __init__(self, nombre, director: Profesor):
        self.__nombre = nombre
        self.__director = director  
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

    def agregar_profesor(self, p_profesor):
        if p_profesor not in self.__profesores:
            self.__profesores.append(p_profesor)

    def listar_profesores(self):
        return [str(profesor) for profesor in self.__profesores]
    
    def agregar_curso(self, p_curso):
        if p_curso not in self.__cursos:
            self.__cursos.append(p_curso) 

    def listar_cursos(self):
        return [str(curso) for curso in self.__cursos]
    
    def __str__(self):
        return f"{self.__nombre}, Director: {self.__director}"
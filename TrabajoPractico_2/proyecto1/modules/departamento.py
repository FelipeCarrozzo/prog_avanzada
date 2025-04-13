class Departamento:
    def __init__(self, nombre, director):
        self.__nombre = nombre
        self.__director = director  #Profesor
        self.__profesores = [director]  # al menos contiene al director
        self.__cursos = []

    def agregar_profesor(self, profesor):
        if profesor not in self.profesores:
            self.profesores.append(profesor)

    def listar_profesores(self):
        return [str(profesor) for profesor in self.profesores]

    def __str__(self):
        return f"Departamento: {self.__nombre}, Director: {self.__director}"
    
    def agregar_curso(self, curso):
        self.cursos.append(curso)

    def listar_cursos(self):
        return [str(curso) for curso in self.cursos]
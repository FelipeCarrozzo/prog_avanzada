from modules.persona import Persona

class Estudiante(Persona):
    def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni)
        self.__facultades = []
        self.__cursos = []

    def inscribir_facultad(self, facultad):
        if facultad not in self.__facultades:
            self.__facultades.append(facultad)

    def inscribir_curso(self, curso):
        if curso not in self.__cursos:
            self.__cursos.append(curso)

    def listar_cursos(self):
        for curso in self.__cursos:
            print(curso)

    def __str__(self):
        return super().__str__()
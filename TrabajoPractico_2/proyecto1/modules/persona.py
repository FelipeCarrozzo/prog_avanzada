#CLASE BASE PERSONA
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
    
#CLASE ESTUDIANTE
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
    
#CLASE PROFESOR
class Profesor(Persona):
    def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni)
        self.__departamentos = []

    def asociar_departamento(self, depto):
        if depto not in self.__departamentos:
            self.__departamentos.append(depto)

    def __str__(self):
        return super().__str__()

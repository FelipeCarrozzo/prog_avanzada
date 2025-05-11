from abc import ABC


# CLASE BASE ABSTRACTA
class Persona(ABC):
    """
    Clase base abstracta que representa una persona con nombre, apellido y DNI.
    """

    def __init__(self, p_nombre: str, p_apellido: str, p_dni: str):
        """
        Inicializa una nueva persona.

        Args:
            nombre (str): Nombre de la persona.
            apellido (str): Apellido de la persona.
            dni (str): Documento Nacional de Identidad.
        """
        self.__nombre = p_nombre
        self.__apellido = p_apellido
        self.__dni = p_dni

    @property
    def nombre(self):
        """Devuelve el nombre de la persona."""
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        """Asigna un nuevo nombre, si no está vacío."""
        if nuevo_nombre.strip() == "":
            raise ValueError("El nombre no puede ser una cadena vacía")
        self.__nombre = nuevo_nombre

    @property
    def apellido(self):
        """Devuelve el apellido de la persona."""
        return self.__apellido

    @apellido.setter
    def apellido(self, nuevo_apellido: str):
        """Asigna un nuevo apellido, si no está vacío."""
        if nuevo_apellido.strip() == "":
            raise ValueError("El apellido no puede ser una cadena vacía")
        self.__apellido = nuevo_apellido

    @property
    def dni(self):
        """Devuelve el DNI de la persona."""
        return self.__dni

    def __str__(self):
        return f"{self.__nombre} {self.__apellido}, DNI: {self.__dni}"

class Estudiante(Persona):
    """
    Representa a un estudiante, que puede estar inscrito en múltiples facultades y cursos.
    """

    def __init__(self, nombre: str, apellido: str, dni: str):
        super().__init__(nombre, apellido, dni)
        self.__facultades = []  
        self.__cursos = []     

    @property
    def cursos(self):
        """Devuelve la lista de cursos en los que está inscrito el estudiante."""
        return self.__cursos

    @property
    def facultades(self):
        """Devuelve la lista de facultades a las que pertenece el estudiante."""
        return self.__facultades

    def inscribir_facultad(self, p_facultad):
        """Agrega una facultad a la lista, si no está ya inscrito."""
        from modules.facultad import Facultad
        if not isinstance(p_facultad, Facultad):
            raise TypeError("La facultad debe ser una instancia de la clase Facultad.")
        if p_facultad not in self.__facultades:
            self.__facultades.append(p_facultad)

    def inscribir_curso(self, p_curso):
        """Agrega un curso a la lista, si no está ya inscrito."""
        from modules.curso import Curso
        if not isinstance(p_curso, Curso):
            raise TypeError("El curso debe ser una instancia de la clase Curso.")
        if p_curso not in self.__cursos:
            self.__cursos.append(p_curso)

    def listar_cursos(self):
        """Devuelve la lista de cursos como cadenas."""
        return [str(curso) for curso in self.__cursos]

    def __str__(self):
        return super().__str__()

# CLASE PROFESOR
class Profesor(Persona):
    """
    Representa a un profesor que puede estar asociado a uno o más departamentos.
    """

    def __init__(self, nombre: str, apellido: str, dni: str):
        super().__init__(nombre, apellido, dni)
        self.__departamentos_asignados = [] 
        self.__departamento_director = None
        self.__cursos = []

    @property
    def departamentos(self):
        """Devuelve la lista de departamentos en los que el profesor es director."""
        return self.__departamentos
    
    @property
    def cursos(self):
        """Devuelve la lista de cursos en los que el profesor es titular."""
        return self.__cursos

    def asociar_departamento(self, p_depto):
        """Asocia un nuevo departamento al profesor, si aún no lo está."""
        from modules.departamento import Departamento
        if not isinstance(p_depto, Departamento):
            raise TypeError("El departamento debe ser una instancia de la clase Departamento.")
        if p_depto not in self.__departamentos:
            self.__departamentos.append(p_depto)
    
    def asociar_curso(self, p_curso):
        """Asocia un nuevo curso al profesor, si aún no lo está."""
        from modules.curso import Curso
        if not isinstance(p_curso, Curso):
            raise TypeError("El curso debe ser una instancia de la clase Curso.")
        if p_curso not in self.__cursos:
            self.__cursos.append(p_curso)

    def __str__(self):
        return super().__str__()

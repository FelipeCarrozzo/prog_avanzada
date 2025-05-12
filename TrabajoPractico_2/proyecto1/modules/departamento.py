from modules.persona import Profesor
from modules.curso import Curso

class Departamento:
    """
    Representa un departamento académico dentro de una facultad.
    Cada departamento tiene un nombre, un director (profesor),
    una lista de profesores asociados y una lista de cursos.
    """

    def __init__(self, p_nombre: str, director: Profesor):
        """
        Inicializa un departamento con su nombre y director.

        Args:
            nombre (str): Nombre del departamento.
            director (Profesor): Profesor asignado como director.
        """
        if not isinstance(director, Profesor):
            raise TypeError("El director debe ser una instancia de la clase Profesor.")
        self.__nombre = p_nombre
        self.__director = director
        self.__profesores = [director]  # El director es automáticamente parte del departamento
        self.__cursos = []

        director.asignar_como_director(self)

    @property
    def nombre(self):
        """Devuelve el nombre del departamento."""
        return self.__nombre

    @property
    def director(self):
        """Devuelve el profesor que dirige el departamento."""
        return self.__director

    @property
    def profesores(self):
        """Devuelve la lista de profesores asociados al departamento."""
        return self.__profesores

    @property
    def cursos(self):
        """Devuelve la lista de cursos ofrecidos por el departamento."""
        return self.__cursos

    def agregar_profesor(self, p_profesor: Profesor):
        """
        Agrega un profesor al departamento si aún no está asociado.

        Args:
            p_profesor (Profesor): Profesor a agregar.
        """
        if not isinstance(p_profesor, Profesor):
            raise TypeError("El profesor debe ser una instancia de la clase Profesor.")
        if p_profesor not in self.__profesores:
            self.__profesores.append(p_profesor)
            p_profesor.asignar_departamento(self)

    def listar_profesores(self):
        """Devuelve una lista de los profesores como cadenas de texto."""
        return [str(profesor) for profesor in self.__profesores]

    def agregar_curso(self, p_curso: Curso):
        """
        Agrega un curso al departamento si aún no está registrado.

        Args:
            p_curso (Curso): Curso a agregar.
        """
        if not isinstance(p_curso, Curso):
            raise TypeError("El curso debe ser una instancia de la clase Curso.")
        if p_curso not in self.__cursos:
            self.__cursos.append(p_curso)
        else:
            raise ValueError("El curso ya está registrado en el departamento.")

    def listar_cursos(self):
        """Devuelve una lista de los cursos como cadenas de texto."""
        return [str(curso) for curso in self.__cursos]

    def __str__(self):
        """Devuelve una representación en texto del departamento."""
        return f"Departamento: {self.__nombre}, Director: {self.__director}"

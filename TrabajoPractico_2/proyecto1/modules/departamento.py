from modules.persona import Profesor
from modules.curso import Curso

class Departamento:
    """
    Representa un departamento académico dentro de una facultad.

    Un departamento tiene un nombre, un director (que es un profesor),
    una lista de profesores asignados y una lista de cursos que dicta.
    """

    def __init__(self, p_nombre: str, director: Profesor):
        """
        Inicializa un nuevo departamento con nombre y director.

        El director se asigna automáticamente como parte del departamento 
        y se registra también como director de este.

        Args:
            p_nombre (str): Nombre del departamento.
            director (Profesor): Profesor asignado como director del departamento.

        Raises:
            TypeError: Si el director no es una instancia de Profesor.
        """
        if not isinstance(director, Profesor):
            raise TypeError("El director debe ser una instancia de la clase Profesor.")
        self.__nombre = p_nombre
        self.__director = director
        self.__profesores = [director]  # El director es también un profesor del departamento
        self.__cursos = []

        director.asignar_como_director(self)

    @property
    def nombre(self):
        """str: Devuelve el nombre del departamento."""
        return self.__nombre

    @property
    def director(self):
        """Profesor: Devuelve el profesor director del departamento."""
        return self.__director

    @property
    def profesores(self):
        """list[Profesor]: Lista de profesores asociados al departamento."""
        return self.__profesores

    @property
    def cursos(self):
        """list[Curso]: Lista de cursos que dicta el departamento."""
        return self.__cursos

    def agregar_profesor(self, p_profesor: Profesor):
        """
        Asocia un nuevo profesor al departamento si aún no lo está.

        Args:
            p_profesor (Profesor): Profesor a asociar.

        Raises:
            TypeError: Si el argumento no es una instancia de Profesor.
        """
        if not isinstance(p_profesor, Profesor):
            raise TypeError("El profesor debe ser una instancia de la clase Profesor.")
        if p_profesor not in self.__profesores:
            self.__profesores.append(p_profesor)
            p_profesor.asignar_departamento(self)

    def listar_profesores(self):
        """
        Retorna una lista con las representaciones en texto de los profesores del departamento.

        Returns:
            list[str]: Lista de strings con los profesores.
        """
        return [str(profesor) for profesor in self.__profesores]

    def agregar_curso(self, p_curso: Curso):
        """
        Agrega un curso al departamento si no está registrado previamente.

        Args:
            p_curso (Curso): Curso a agregar.

        Raises:
            TypeError: Si el argumento no es una instancia de Curso.
            ValueError: Si el curso ya está registrado en el departamento.
        """
        if not isinstance(p_curso, Curso):
            raise TypeError("El curso debe ser una instancia de la clase Curso.")
        if p_curso not in self.__cursos:
            self.__cursos.append(p_curso)
        else:
            raise ValueError("El curso ya está registrado en el departamento.")

    def listar_cursos(self):
        """
        Retorna una lista con las representaciones en texto de los cursos del departamento.

        Returns:
            list[str]: Lista de strings con los cursos ofrecidos.
        """
        return [str(curso) for curso in self.__cursos]

    def __str__(self):
        """
        Retorna una representación legible del departamento.

        Returns:
            str: Nombre del departamento y su director.
        """
        return f"Departamento: {self.__nombre}, Director/a: {self.__director}"

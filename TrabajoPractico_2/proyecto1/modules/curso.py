
class Curso:
    """
    Representa un curso universitario.

    Un curso está definido por su nombre, un profesor titular, una lista de estudiantes que lo cursan,
    y una lista de profesores asignados. La clase permite inscribir estudiantes y consultar
    los detalles del curso.
    """

    def __init__(self, p_nombre: str, titular):
        """
        Inicializa una nueva instancia de la clase Curso.

        Args:
            nombre (str): Nombre del curso.
            titular (Profesor): Profesor titular del curso.

        Raises:
            TypeError: Si el titular no es una instancia de la clase Profesor.
        """
        from modules.persona import Profesor
        if not isinstance(titular, Profesor):
            raise TypeError("El titular debe ser una instancia de la clase Profesor.")
        self.__nombre = p_nombre
        self.__titular = titular  
        self.__estudiantes = []
        self.__profesores = []

        titular.asignar_como_titular(self) 
        self.__profesores.append(titular)

    @property
    def nombre(self):
        """
        str: Nombre del curso.
        """
        return self.__nombre
    
    @property
    def titular(self):
        """
        Profesor: Profesor titular del curso.
        """
        return self.__titular

    @property
    def estudiantes(self):
        """
        list[Estudiante]: Lista de estudiantes inscritos en el curso.
        """
        return self.__estudiantes
    
    @property
    def profesores(self):
        """
        list[Profesor]: Lista de profesores que dictan el curso.
        """
        return self.__profesores

    def inscribir_estudiante(self, p_estudiante):
        """
        Inscribe un estudiante en el curso.

        Args:
            p_estudiante (Estudiante): El estudiante a inscribir.

        Raises:
            TypeError: Si p_estudiante no es una instancia de Estudiante.
            ValueError: Si el estudiante ya está inscrito en el curso.
        """
        from modules.persona import Estudiante
        if not isinstance(p_estudiante, Estudiante):
            raise TypeError("El estudiante debe ser una instancia de la clase Estudiante.")
        if p_estudiante not in self.__estudiantes:
            self.__estudiantes.append(p_estudiante)
            p_estudiante.inscribir_curso(self)
        else:
            raise ValueError("El estudiante ya está inscrito en el curso.")

    def __str__(self):
        """
        Retorna una representación en string del curso.

        Returns:
            str: Información del curso incluyendo nombre, código y titular.
        """
        return f"Curso: {self.__nombre}, Titular: {self.__titular}"

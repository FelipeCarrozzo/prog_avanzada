from abc import ABC

# CLASE BASE ABSTRACTA
class Persona(ABC):
    """
    Clase abstracta que representa una persona con nombre, apellido y DNI.
    """

    def __init__(self, p_nombre: str, p_apellido: str, p_dni: str):
        """
        Inicializa una nueva persona.

        Args:
            p_nombre (str): Nombre de la persona.
            p_apellido (str): Apellido de la persona.
            p_dni (str): Documento Nacional de Identidad.
        """
        self.__nombre = p_nombre
        self.__apellido = p_apellido
        self.__dni = p_dni

    @property
    def nombre(self):
        """str: Devuelve el nombre de la persona."""
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        """Asigna un nuevo nombre, si no está vacío."""
        if nuevo_nombre.strip() == "":
            raise ValueError("El nombre no puede ser una cadena vacía")
        self.__nombre = nuevo_nombre

    @property
    def apellido(self):
        """str: Devuelve el apellido de la persona."""
        return self.__apellido

    @apellido.setter
    def apellido(self, nuevo_apellido: str):
        """Asigna un nuevo apellido, si no está vacío."""
        if nuevo_apellido.strip() == "":
            raise ValueError("El apellido no puede ser una cadena vacía")
        self.__apellido = nuevo_apellido

    @property
    def dni(self):
        """str: Devuelve el DNI de la persona."""
        return self.__dni

    def __str__(self):
        """str: Representación legible de la persona."""
        return f"{self.__nombre} {self.__apellido}, DNI: {self.__dni}"


class Estudiante(Persona):
    """
    Representa a un estudiante que puede estar inscrito en múltiples facultades y cursos.
    """

    def __init__(self, nombre: str, apellido: str, dni: str):
        super().__init__(nombre, apellido, dni)
        self.__facultades = []
        self.__cursos = []

    @property
    def cursos(self):
        """list: Devuelve la lista de cursos en los que está inscrito el estudiante."""
        return self.__cursos

    @property
    def facultades(self):
        """list: Devuelve la lista de facultades a las que pertenece el estudiante."""
        return self.__facultades

    def inscribir_facultad(self, p_facultad):
        """
        Agrega una facultad a la lista, si aún no está inscrito.

        Args:
            p_facultad (Facultad): Facultad a la que se inscribe el estudiante.

        Raises:
            TypeError: Si el argumento no es una instancia de Facultad.
        """
        from modules.facultad import Facultad
        if not isinstance(p_facultad, Facultad):
            raise TypeError("La facultad debe ser una instancia de la clase Facultad.")
        if p_facultad not in self.__facultades:
            self.__facultades.append(p_facultad)

    def inscribir_curso(self, p_curso):
        """
        Agrega un curso a la lista, si aún no está inscrito.

        Args:
            p_curso (Curso): Curso a inscribir.

        Raises:
            TypeError: Si el argumento no es una instancia de Curso.
        """
        from modules.curso import Curso
        if not isinstance(p_curso, Curso):
            raise TypeError("El curso debe ser una instancia de la clase Curso.")
        if p_curso not in self.__cursos:
            self.__cursos.append(p_curso)

    def listar_cursos(self):
        """
        Devuelve una lista con representaciones en texto de los cursos del estudiante.

        Returns:
            list[str]: Cursos en formato string.
        """
        return [str(curso) for curso in self.__cursos]

    def __str__(self):
        """str: Representación legible del estudiante."""
        return super().__str__()


class Profesor(Persona):
    """
    Representa a un profesor que puede dictar cursos, ser director de un departamento y ser titular de un curso.
    """

    def __init__(self, nombre: str, apellido: str, dni: str):
        super().__init__(nombre, apellido, dni)
        self.__departamentos_asignados = []
        self.__departamento_director = None
        self.__cursos_dictados = []
        self.__curso_titular = None

    @property
    def departamentos_asignados(self):
        """list: Devuelve los departamentos en los que el profesor trabaja."""
        return self.__departamentos_asignados

    @property
    def departamento_director(self):
        """Departamento or None: Devuelve el departamento que dirige (si lo hay)."""
        return self.__departamento_director

    @property
    def cursos_dictados(self):
        """list: Devuelve la lista de cursos en los que el profesor enseña."""
        return self.__cursos_dictados
    
    @property
    def cursos_dictados(self):
        """list: Devuelve la lista de cursos en los que el profesor enseña."""
        return self.__cursos_dictados

    @property
    def curso_titular(self):
        """Curso or None: Devuelve el curso que el profesor dicta como titular."""
        return self.__curso_titular

    def asignar_departamento(self, p_depto):
        """
        Asigna un departamento al profesor, si aún no lo está.

        Args:
            p_depto (Departamento): Departamento a asignar.

        Raises:
            TypeError: Si el argumento no es una instancia de Departamento.
        """
        from modules.departamento import Departamento
        if not isinstance(p_depto, Departamento):
            raise TypeError("Debe ser una instancia de Departamento.")
        if p_depto not in self.__departamentos_asignados:
            self.__departamentos_asignados.append(p_depto)

    def asignar_como_director(self, p_depto):
        """
        Asigna al profesor como director del departamento, si no dirige otro.

        Args:
            p_depto (Departamento): Departamento a dirigir.

        Raises:
            TypeError: Si el argumento no es una instancia de Departamento.
            ValueError: Si ya dirige otro departamento.
        """
        from modules.departamento import Departamento
        if not isinstance(p_depto, Departamento):
            raise TypeError("Debe ser una instancia de Departamento.")
        if self.__departamento_director is not None:
            raise ValueError("El profesor ya es director de otro departamento.")
        self.__departamento_director = p_depto
        self.asignar_departamento(p_depto)

    def asociar_curso(self, p_curso):
        """
        Asocia un curso al profesor, si aún no está registrado como titular.

        Args:
            p_curso (Curso): Curso a asociar.

        Raises:
            TypeError: Si el argumento no es una instancia de Curso.
        """
        from modules.curso import Curso
        if not isinstance(p_curso, Curso):
            raise TypeError("El curso debe ser una instancia de la clase Curso.")
        if p_curso not in self.__cursos_dictados:
            self.__cursos_dictados.append(p_curso)

    def asignar_como_titular(self, p_curso):
        """
        Asigna al profesor como titular de un curso, si no es titular de otro, y se asegura de que el curso esté asociado.

        Args:
            p_curso (Curso): Curso a dictar.

        Raises:
            TypeError: Si el argumento no es una instancia de Curso.
            ValueError: Si ya es titular de otro curso.
        """
        from modules.curso import Curso
        if not isinstance(p_curso, Curso):
            raise TypeError("El curso debe ser una instancia de la clase Curso.")
        if self.__curso_titular is not None:
            raise ValueError("El profesor ya es titular de otro curso.")
        self.__curso_titular = p_curso
        self.asociar_curso(p_curso)

    def __str__(self):
        """str: Representación legible del profesor."""
        return super().__str__()


from modules.departamento import Departamento

class Facultad:
    """
    Representa una facultad dentro de una universidad, con estudiantes, profesores y departamentos asociados.
    """

    def __init__(self, p_nombre: str, p_nombre_departamento: str, p_director):
        """
        Inicializa una nueva instancia de la clase Facultad.

        Args:
            p_nombre (str): El nombre de la facultad.
            p_nombre_departamento (str): El nombre del departamento.
            p_director: El director del departamento.
        """
        self.__nombre = p_nombre
        self.__departamentos = []
        self.__estudiantes = []
        self.__profesores = []

        self.contratar_profesor(p_director)
        self.crear_departamento(p_nombre_departamento, p_director)

    @property
    def nombre(self):
        """
        str: Nombre de la facultad.
        """
        return self.__nombre

    @property
    def estudiantes(self):
        """
        list: Lista de estudiantes (objetos Estudiante) inscritos en la facultad.
        """
        return self.__estudiantes

    @property
    def departamentos(self):
        """
        list: Lista de departamentos (objetos Departamento) pertenecientes a la facultad.
        """
        return self.__departamentos

    @property
    def profesores(self):
        """
        list: Lista de profesores (objetos Profesor) contratados en la facultad.
        """
        return self.__profesores

    def agregar_estudiante(self, p_estudiante):
        """
        Agrega un estudiante a la facultad, si aún no está inscrito.

        Args:
            p_estudiante (Estudiante): El estudiante a agregar.

        Raises:
            TypeError: Si el argumento no es una instancia de Estudiante.
            ValueError: Si el estudiante ya está inscrito en la facultad.
        """
        from modules.persona import Estudiante
        if not isinstance(p_estudiante, Estudiante):
            raise TypeError("El estudiante debe ser una instancia de la clase Estudiante.")
        if p_estudiante not in self.__estudiantes:
            self.__estudiantes.append(p_estudiante)
        else:
            raise ValueError("El estudiante ya está inscrito en la facultad.")

    def listar_estudiantes(self):
        """
        Retorna una lista con representaciones en string de todos los estudiantes.

        Returns:
            list[str]: Lista de strings representando a cada estudiante.
        """
        return [str(estudiante) for estudiante in self.__estudiantes]

    def contratar_profesor(self, p_profesor):
        """
        Contrata un profesor para la facultad, si aún no está registrado.

        Args:
            p_profesor (Profesor): El profesor a contratar.

        Raises:
            TypeError: Si el argumento no es una instancia de Profesor.
            ValueError: Si el profesor ya está contratado en la facultad.
        """
        from modules.persona import Profesor
        if not isinstance(p_profesor, Profesor):
            raise TypeError("El profesor debe ser una instancia de la clase Profesor.")
        if p_profesor not in self.__profesores:
            self.__profesores.append(p_profesor)
        else:
            raise ValueError("El profesor ya está contratado en la facultad.")

    def listar_profesores(self):
        """
        Retorna una lista con representaciones en string de todos los profesores.

        Returns:
            list[str]: Lista de strings representando a cada profesor.
        """
        return [str(profesor) for profesor in self.__profesores]
    
    def crear_departamento(self, p_nombre: str, p_director):
        """
        Crea un nuevo departamento en la facultad.

        Args:
            p_nombre (str): Nombre del departamento.
            p_director (Profesor): Profesor que será el director del departamento.

        Raises:
            TypeError: Si el director no es una instancia de Profesor.
        """
        from modules.persona import Profesor
        if not isinstance(p_director, Profesor):
            raise TypeError("El director debe ser una instancia de la clase Profesor.")
        
        if p_nombre in [depto.nombre for depto in self.__departamentos]:
            raise ValueError("El departamento ya está registrado en la facultad.")
        
        nuevo_departamento = Departamento(p_nombre, p_director) #contención
        
        self.__departamentos.append(nuevo_departamento)
        return nuevo_departamento

    def listar_departamentos(self):
        """
        Retorna una lista con representaciones en string de todos los departamentos.

        Returns:
            list[str]: Lista de strings representando a cada departamento.
        """
        return [str(departamento) for departamento in self.__departamentos]

    def obtener_cursos_con_departamento(self):
        """
        Retorna una lista de tuplas con cada curso y su departamento correspondiente.

        Returns:
            list[tuple]: Tuplas de la forma (curso, departamento).
        """
        cursos = []
        for depto in self.__departamentos:
            for curso in depto.cursos:
                cursos.append((curso, depto))
        return cursos

    def __str__(self):
        """
        Retorna una representación en string de la facultad.

        Returns:
            str: Nombre de la facultad.
        """
        return self.__nombre

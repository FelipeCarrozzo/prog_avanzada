class Facultad:
    def __init__(self, nombre, ubicacion, departamentos, decano, contacto):
        self.__nombre = nombre
        self.__ubicacion = ubicacion
        self.__departamentos = departamentos
        self.__decano = decano
        self.__contacto = contacto

class Departamento:
    def __init__(self, nombre, id, facultad, jefe_depto, cursos, profesores):
        self.__nombre = nombre
        self.__id = id
        self.__facultad = facultad
        self.__jefe_depto = jefe_depto
        self.__cursos = cursos
        self.__profesores = profesores

class Estudiante:
    def __init__(self, nombre_completo, dni, mail, carrera, cursos):
        self.__nombre_completo = nombre_completo
        self.__dni = dni
        self.__mail = mail
        self.__carrera = carrera
        self.__cursos = cursos

class Profesor:
    def __init__(self, nombre_completo, dni, especialidad, cursos_asignados, departamentos):
        self.__nombre_completo = nombre_completo
        self.__dni = dni
        self.__especialidad = especialidad
        self.__cursos_asignados = cursos_asignados
        self.__departamentos = departamentos

class Curso:
    def __init__(self, nombre, id, profesores, departamento, creditos, horario, estudiantes):
        self.__nombre = nombre
        self.__id = id
        self.__profesores = profesores
        self.__departamento = departamento
        self.__creditos = creditos
        self.__horario = horario
        self.__estudiantes = estudiantes
        

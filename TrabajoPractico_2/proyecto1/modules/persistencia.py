# persistencia.py
# Este módulo se encarga de la persistencia de datos, es decir, guardar y cargar la información del sistema en archivos.
# modules/persistencia_txt.py
import os
from modules.facultad import Facultad
from modules.persona import Estudiante, Profesor
from modules.facultad import Facultad
from modules.departamento import Departamento
from modules.curso import Curso

base_dir = os.path.dirname(__file__)
path_personas = os.path.join(base_dir,'..', 'data', 'personas.txt')
path_sistema = os.path.join(base_dir,'..', 'data', 'sistema.txt')

def cargar_facultad_desde_personas_txt(nombre_facultad):
    
    """
    Crea una instancia de Facultad a partir de un archivo de texto con datos de personas.

    El archivo `personas.txt` debe contener líneas con el siguiente formato:
    - ESTUDIANTE,Nombre,Apellido,DNI
    - PROFESOR,Nombre,Apellido,DNI

    Se agregan hasta 4 estudiantes y 4 profesores a la facultad creada.

    Parámetros:
    ----------
    nombre_facultad : str
        Nombre de la facultad a crear.

    Retorna:
    -------
    Facultad
        Instancia de la facultad con los estudiantes y profesores cargados.
    """
        
    facultad = Facultad(nombre_facultad)
    estudiantes_agregados = 0
    profesores_agregados = 0

    with open(path_personas, 'r', encoding='utf-8') as f:
        for linea in f:
            datos = linea.strip().split(',')
            if datos[0] == 'ESTUDIANTE' and estudiantes_agregados < 4:
                nombre, apellido, dni = datos[1], datos[2], datos[3]
                estudiante = Estudiante(nombre, apellido, dni)
                facultad.agregar_estudiante(estudiante)
                estudiantes_agregados += 1
            elif datos[0] == 'PROFESOR' and profesores_agregados < 4:
                nombre, apellido, dni = datos[1], datos[2], datos[3]
                profesor = Profesor(nombre, apellido, dni)
                facultad.contratar_profesor(profesor)
                profesores_agregados += 1
            if estudiantes_agregados == 4 and profesores_agregados == 4:
                break

    return facultad

def guardar_sistema_txt(facultades):
    """
    Guarda en un archivo de texto plano (`sistema.txt`) toda la información del sistema:
    facultades, profesores, estudiantes, departamentos, cursos e inscripciones.

    Cada entidad se guarda con una línea prefijada indicando su tipo:
    - FACULTAD
    - PROFESOR
    - ESTUDIANTE
    - DEPARTAMENTO
    - CURSO
    - INSCRIPCION

    Parámetros:
    ----------
    facultades : list[Facultad]
        Lista de facultades a guardar.
    """
        
    with open(path_sistema, "w", encoding="utf-8") as f:
        for facultad in facultades:
            f.write(f"FACULTAD,{facultad.nombre}\n")
            for profesor in facultad.profesores:
                f.write(f"PROFESOR,{profesor.nombre},{profesor.apellido},{profesor.dni}\n")
            for estudiante in facultad.estudiantes:
                f.write(f"ESTUDIANTE,{estudiante.nombre},{estudiante.apellido},{estudiante.dni}\n")
            for depto in facultad.departamentos:
                director = depto.director
                f.write(f"DEPARTAMENTO,{depto.nombre},{director.nombre},{director.apellido},{director.dni}\n")
                for curso in depto.cursos:
                    prof = curso.titular
                    f.write(f"CURSO,{curso.codigo},{curso.nombre},{prof.nombre},{prof.apellido},{prof.dni},{depto.nombre}\n")
                    for estudiante in curso.estudiantes:
                        f.write(f"INSCRIPCION,{estudiante.nombre},{estudiante.apellido},{estudiante.dni},{curso.codigo}\n")

def cargar_sistema_txt():
    """
    Carga la estructura completa de universidades desde un archivo `sistema.txt`,
    reconstruyendo todas las relaciones entre facultades, departamentos, cursos,
    profesores y estudiantes.

    El archivo debe haber sido generado previamente por la función `guardar_sistema_txt()`.

    Retorna:
    -------
    list[Facultad]
        Lista de facultades reconstruidas desde el archivo.
    """

    facultades = []
    profesores_global = {}
    estudiantes_global = {}
    cursos_global = {}
    facultad_actual = None
    departamentos = {}

    with open(path_sistema, 'r', encoding='utf-8') as f:
        for linea in f:
            partes = linea.strip().split(",")
            tipo = partes[0]

            if tipo == "FACULTAD":
                facultad_actual = Facultad(partes[1])
                facultades.append(facultad_actual)

            elif tipo == "PROFESOR":
                nombre, apellido, dni = partes[1], partes[2], partes[3]
                prof = Profesor(nombre, apellido, dni)
                profesores_global[dni] = prof
                facultad_actual.contratar_profesor(prof)

            elif tipo == "ESTUDIANTE":
                nombre, apellido, dni = partes[1], partes[2], partes[3]
                est = Estudiante(nombre, apellido, dni)
                estudiantes_global[dni] = est
                facultad_actual.agregar_estudiante(est)

            elif tipo == "DEPARTAMENTO":
                nombre_depto, nombre, apellido, dni = partes[1], partes[2], partes[3], partes[4]
                director = profesores_global[dni]
                depto = Departamento(nombre_depto, director)
                facultad_actual.agregar_departamento(depto)
                director.asociar_departamento(depto)
                departamentos[nombre_depto] = depto

            elif tipo == "CURSO":
                codigo, nombre_curso = partes[1], partes[2]
                nombre_prof, apellido_prof, dni_prof = partes[3], partes[4], partes[5]
                nombre_depto = partes[6]
                profesor = profesores_global[dni_prof]
                curso = Curso(nombre_curso, codigo, profesor)

                departamento = next((d for d in facultad_actual.departamentos if d.nombre == nombre_depto), None)
                if departamento:
                    departamento.agregar_curso(curso)
                    cursos_global[codigo] = curso
                    profesor.asociar_curso(curso)

            elif tipo == "INSCRIPCION":
                nombre, apellido, dni, codigo = partes[1], partes[2], partes[3], partes[4]
                estudiante = estudiantes_global[dni]
                curso = cursos_global.get(codigo)
                if curso:
                    curso.inscribir_estudiante(estudiante)
                    estudiante.inscribir_curso(curso)

    return facultades



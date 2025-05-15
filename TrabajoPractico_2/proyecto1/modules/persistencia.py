# persistencia.py
# Este módulo se encarga de la persistencia de datos, es decir, guardar y cargar la información del sistema en archivos.

import os
from modules.facultad import Facultad
from modules.persona import Estudiante, Profesor
from modules.departamento import Departamento
from modules.curso import Curso

base_dir = os.path.dirname(__file__)
path_personas = os.path.join(base_dir,'..', 'data', 'personas.txt')
path_sistema = os.path.join(base_dir,'..', 'data', 'sistema.txt')



def cargar_estudiantes_y_profesores():
    """
    Carga los estudiantes y profesores desde el archivo `personas.txt`.
    Retorna:
    -------
    tuple
        list[Estudiante], list[Profesor]
        Lista de estudiantes y lista de profesores.
    """
    estudiantes = []
    profesores = []
    estudiantes_agregados = 0
    profesores_agregados = 0

    with open(path_personas, 'r', encoding='utf-8') as f:
        for linea in f:
            datos = linea.strip().split(',')
            if datos[0] == 'ESTUDIANTE' and estudiantes_agregados < 4:
                estudiante = Estudiante(datos[1], datos[2], datos[3])
                estudiantes.append(estudiante)
                estudiantes_agregados += 1
            elif datos[0] == 'PROFESOR' and profesores_agregados < 4:
                profesor = Profesor(datos[1], datos[2], datos[3])
                profesores.append(profesor)
                profesores_agregados += 1
            if estudiantes_agregados == 4 and profesores_agregados == 4:
                break

    return estudiantes, profesores


def guardar_sistema_txt(facultades):
    """
    Guarda en un archivo de texto plano (`sistema.txt`) toda la información del sistema:
    facultades, profesores, estudiantes, departamentos, cursos e inscripciones.

    Cada entidad se guarda con una línea prefijada indicando su tipo:
    - FACULTAD,nombre,nombre_depto,nom_director,ape_director,dni_director
    - PROFESOR,nombre,apellido,dni
    - ESTUDIANTE,nombre,apellido,dni
    - DEPARTAMENTO,nombre,nom_director,ape_director,dni_director
    - CURSO,nombre,nom_profesor,ape_profesor,dni_profesor,nombre_depto
    - INSCRIPCION,nombre_estudiante,apellido_estudiante,dni_estudiante,nombre_curso
    """
    with open(path_sistema, "w", encoding="utf-8") as f:
        for facultad in facultades:
            # Obtener el primer departamento
            if facultad.departamentos:
                primer_depto = facultad.departamentos[0]
                director = primer_depto.director
                f.write(f"FACULTAD,{facultad.nombre},{primer_depto.nombre},{director.nombre},{director.apellido},{director.dni}\n")
            else:
                raise ValueError(f"La facultad {facultad.nombre} no tiene departamentos asignados.")

            for profesor in facultad.profesores:
                f.write(f"PROFESOR,{profesor.nombre},{profesor.apellido},{profesor.dni}\n")

            for estudiante in facultad.estudiantes:
                f.write(f"ESTUDIANTE,{estudiante.nombre},{estudiante.apellido},{estudiante.dni}\n")

            for depto in facultad.departamentos:
                director = depto.director
                f.write(f"DEPARTAMENTO,{depto.nombre},{director.nombre},{director.apellido},{director.dni}\n")

                for curso in depto.cursos:
                    prof = curso.titular
                    f.write(f"CURSO,{curso.nombre},{prof.nombre},{prof.apellido},{prof.dni},{depto.nombre}\n")

                    for estudiante in curso.estudiantes:
                        f.write(f"INSCRIPCION,{estudiante.nombre},{estudiante.apellido},{estudiante.dni},{curso.nombre}\n")


def cargar_sistema_txt():
    """
    Carga la estructura completa de universidades desde un archivo `sistema.txt`,
    reconstruyendo todas las relaciones entre facultades, departamentos, cursos,
    profesores y estudiantes.

    Retorna:
    -------
    list[Facultad]
        Lista de facultades reconstruidas desde el archivo.
    """

    facultades = []
    profesores_global = {}
    estudiantes_global = {}
    cursos_global = {}
    departamentos = {}
    facultad_actual = None

    with open(path_sistema, 'r', encoding='utf-8') as f:
        for linea in f:
            partes = linea.strip().split(",")
            tipo = partes[0]

            if tipo == "FACULTAD":
                nombre_facultad = partes[1]
                nombre_depto = partes[2]
                nombre_dir, apellido_dir, dni_dir = partes[3], partes[4], partes[5]

                director = Profesor(nombre_dir, apellido_dir, dni_dir)
                profesores_global[dni_dir] = director

                facultad_actual = Facultad(nombre_facultad, nombre_depto, director)
                facultades.append(facultad_actual)

            elif tipo == "PROFESOR":
                nombre, apellido, dni = partes[1], partes[2], partes[3]
                if dni not in profesores_global:
                    prof = Profesor(nombre, apellido, dni)
                    profesores_global[dni] = prof
                    facultad_actual.contratar_profesor(prof)

            elif tipo == "ESTUDIANTE":
                nombre, apellido, dni = partes[1], partes[2], partes[3]
                est = Estudiante(nombre, apellido, dni)
                estudiantes_global[dni] = est
                facultad_actual.agregar_estudiante(est)

            elif tipo == "DEPARTAMENTO":
                nombre_depto, nombre_dir, apellido_dir, dni_dir = partes[1], partes[2], partes[3], partes[4]
                if not any(depto.nombre == nombre_depto for depto in facultad_actual.departamentos):
                    director = profesores_global[dni_dir]
                    depto = facultad_actual.crear_departamento(nombre_depto, director)
                    departamentos[nombre_depto] = depto

            elif tipo == "CURSO":
                nombre_curso = partes[1]
                nombre_prof, apellido_prof, dni_prof = partes[2], partes[3], partes[4]
                nombre_depto = partes[5]

                profesor = profesores_global[dni_prof]
                curso = Curso(nombre_curso, profesor)

                departamento = departamentos.get(nombre_depto)
                if departamento:
                    departamento.agregar_curso(curso)
                    cursos_global[nombre_curso] = curso
                    profesor.asociar_curso(curso)

            elif tipo == "INSCRIPCION":
                nombre, apellido, dni, nombre_curso = partes[1], partes[2], partes[3], partes[4]
                estudiante = estudiantes_global.get(dni)
                curso = cursos_global.get(nombre_curso)
                if curso and estudiante:
                    curso.inscribir_estudiante(estudiante)
                    estudiante.inscribir_curso(curso)

    return facultades



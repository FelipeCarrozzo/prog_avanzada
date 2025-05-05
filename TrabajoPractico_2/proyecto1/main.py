# -*- coding: utf-8 -*-
from modules.facultad import Facultad
from modules.departamento import Departamento
from modules.persona import Persona, Estudiante, Profesor
from modules.curso import Curso
import os

facultades = []

def inicializar_facultades():
    #se crean 2 facultades
    facultades = [Facultad("Ingeniería"), Facultad("Ciencias Económicas")]
    #se crean 2 profesores por facultad
    facultades[0].contratar_profesor(Profesor("Juan", "Pérez", "12345678"))
    facultades[0].contratar_profesor(Profesor("María", "Gómez", "87654321"))
    facultades[1].contratar_profesor(Profesor("Ana", "López", "11223344"))
    facultades[1].contratar_profesor(Profesor("Luis", "Martínez", "44332211"))
    #se crea 1 departamento por facultad
    Departamento1 = Departamento("Sistemas", facultades[0].profesores[0])
    Departamento2 = Departamento("Contabilidad", facultades[1].profesores[0])
    facultades[0].agregar_departamento(Departamento1)
    facultades[1].agregar_departamento(Departamento2)
    #se crean 2 estudiantes para la facultad de ingeniería
    estudiante1 = Estudiante("Pedro", "García", "12345678")
    estudiante2 = Estudiante("Laura", "Fernández", "87654321")
    facultades[0].agregar_estudiante(estudiante1)
    facultades[0].agregar_estudiante(estudiante2)
    #se crea 1 curso por departamento
    curso1 = Curso("Programación", "INF101", facultades[0].profesores[0])
    curso2 = Curso("Contabilidad I", "ECO101", facultades[1].profesores[0])
    Departamento1.agregar_curso(curso1)
    Departamento2.agregar_curso(curso2)

    return facultades

#facultades = inicializar_facultades()

# Ruta absoluta al archivo personas.txt
base_dir = os.path.dirname(__file__)
path_personas = os.path.join(base_dir, 'data', 'personas.txt')

def crear_facultad_desde_archivo(nombre_facultad):
    facultad = Facultad(nombre_facultad)
    estudiantes_agregados = 0
    profesores_agregados = 0

    #crear 1 txt por cada entidad
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

print("Bienvenido al sistema de gestión de facultades.")
nombre_facultad = input("Ingrese el nombre de la facultad: ")

#facultades = crear_facultad_desde_archivo(nombre_facultad)
facultades = [crear_facultad_desde_archivo(nombre_facultad)]


#facultades = [crear_facultad_desde_archivo("Facultad de Ingeniería")]

#cuando creamos la facultad desde el archivo, se deberían crear los departamentos y cursos automáticamente

while True:
    print("##########################################")
    print("#  Sistema de Información Universitaria  #")
    print("##########################################")
    print("Elige una opción")
    print("1 - Inscribir alumno")
    print("2 - Contratar profesor")
    print("3 - Crear departamento nuevo")
    print("4 - Crear curso nuevo")
    print("5 - Inscribir estudiante a un curso")
    print("6 - Salir")
    
    opcion = input("Opción: ")
    
    if opcion == "1":
        # lógica para inscribir alumno
            #cómo hacer con la facultad?
            print("Seleccione la facultad:")
            for i, facultad in enumerate(facultades):
                print(f"{i + 1} - {facultad.nombre}")
            facultad_index = int(input("Opción: ")) - 1
            facultad = facultades[facultad_index]

            nombre = input("Nombre del estudiante: ")
            apellido = input("Apellido del estudiante: ")
            dni = input("DNI: ")

            estudiante = Estudiante(nombre, apellido, dni)
            facultad.agregar_estudiante(estudiante)
            print(f"{estudiante} inscripto en {facultad}.\n")
            print("\n")
            print("Estudiantes inscriptos en la facultad:")
            for est in facultad.listar_estudiantes():
                print(est)
            print("\n")
        
    elif opcion == "2":
        # lógica para contratar profesor
        print("Seleccione la facultad:")
        for i, facultad in enumerate(facultades):
            print(f"{i + 1} - {facultad.nombre}")
        facultad_index = int(input("Opción: ")) - 1
        if facultad_index < 0 or facultad_index >= len(facultades):
            print("Opción no válida.")
            continue
        facultad = facultades[facultad_index]

        nombre = input("Nombre del profesor: ")
        apellido = input("Apellido del profesor: ")
        dni = input("DNI: ")

        nuevo_profesor = Profesor(nombre, apellido, dni)
        facultad.contratar_profesor(nuevo_profesor)
        print(f"\nProfesor {nuevo_profesor} contratado en {facultad}.\n")

    elif opcion == "3":
        # lógica para crear departamento nuevo
        print("Seleccione la facultad:")
        for i, facultad in enumerate(facultades):
            print(f"{i + 1} - {facultad.nombre}")
        facultad_index = int(input("Opción: ")) - 1
        if facultad_index < 0 or facultad_index >= len(facultades):
            print("Opción no válida.")
            continue
        facultad = facultades[facultad_index]

        nuevo_departamento = input("Nombre del nuevo departamento: ")

        #se verifica si el departamento ya existe
        for depto in facultad.departamentos:
            if depto.nombre == nuevo_departamento:
                print(f"El departamento {nuevo_departamento} ya existe en la facultad {facultad}.")
                break
        else:
            # Si no existe, crear el nuevo departamento y asociar un profesor a él

            print("\nSeleccione el director del departamento entre los profesores existentes:")
            if not facultad.listar_profesores():
                print("No hay profesores disponibles para asignar como director.")
                continue
            for i, prof in enumerate(facultad.listar_profesores()):
                print(f"{i + 1} - {prof}")
            profesor_index = int(input("Opción: ")) - 1
            if profesor_index < 0 or profesor_index >= len(facultad.listar_profesores()):
                print("Opción no válida.")
                continue
            profesor = facultad.listar_profesores()[profesor_index]
            nuevo_profesor = profesor
            nuevo_departamento = Departamento(nuevo_departamento, nuevo_profesor)
            facultad.agregar_departamento(nuevo_departamento)
            #nuevo_profesor.asociar_departamento(nuevo_departamento)
            #print(f"\nProfesor {nuevo_profesor} asociado al departamento {nuevo_departamento}.\n")
            
            print(f"Departamento {nuevo_departamento} creado en la facultad {facultad}.\n")

        print("Departamentos en la facultad:")
        for depto in facultad.listar_departamentos():
            print(depto)
        print("\n")
        
    elif opcion == "4":
        print("Seleccione la facultad:")
        for i, facultad in enumerate(facultades):
            print(f"{i + 1} - {facultad.nombre}")
        facultad_index = int(input("Opción: ")) - 1
        if facultad_index < 0 or facultad_index >= len(facultades):
            print("Opción no válida.")
            continue
        facultad = facultades[facultad_index]

        #1ero se valida si hay departamentos
        if not facultad.listar_departamentos():
            print("La facultad aún no tiene departamentos.")
            continue

        print("Seleccione el departamento donde se creará el curso:")
        for i, depto in enumerate(facultad.departamentos):
            print(f"{i + 1} - {depto.nombre}")
        depto_index = int(input("Opción: ")) - 1
        if depto_index < 0 or depto_index >= len(facultad.listar_departamentos()):
            print("Opción no válida.")
            continue
        departamento = facultad.departamentos[depto_index]

        #ingresar nombre y código del curso
        nombre_curso = input("Nombre del curso: ")
        codigo_curso = input("Código del curso: ")

        #se verifica que haya profesores disponibles
        if not facultad.listar_profesores():
            print("No hay profesores en esta facultad para asignar como titular.")
            continue

        print("Seleccione el profesor titular:")
        for i, prof in enumerate(facultad.listar_profesores()):
            print(f"{i + 1} - {prof}")
        prof_index = int(input("Opción: ")) - 1
        if prof_index < 0 or prof_index >= len(facultad.listar_profesores()):
            print("Opción no válida.")
            continue
        profesor = facultad.listar_profesores()[prof_index]

        #crear el curso y agregarlo al departamento
        nuevo_curso = Curso(nombre_curso, codigo_curso, profesor)
        departamento.agregar_curso(nuevo_curso)

        print(f"\nCurso '{nombre_curso}' creado correctamente en el departamento {departamento.nombre}.\n")

        print("Cursos actuales en el departamento:")
        for curso_str in departamento.listar_cursos():
            print(curso_str)
    
    elif opcion == "5":
        # lógica para inscribir estudiante a un curso
        print("Seleccione la facultad:")
        for i, facultad in enumerate(facultades):
            print(f"{i + 1} - {facultad.nombre}")
        facultad_index = int(input("Opción: ")) - 1
        if facultad_index < 0 or facultad_index >= len(facultades):
            print("Opción no válida.")
            continue
        facultad = facultades[facultad_index]

        if not facultad.estudiantes:
            print("No hay estudiantes registrados en esta facultad.")
            continue

        print("Seleccione el estudiante a inscribir:")
        for i, est in enumerate(facultad.estudiantes):
            print(f"{i + 1} - {est}")
        est_index = int(input("Opción: ")) - 1
        if est_index < 0 or est_index >= len(facultad.estudiantes):
            print("Opción no válida.")
            continue
        estudiante = facultad.estudiantes[est_index]

        cursos_y_depto = facultad.obtener_cursos_con_departamento()
        if not cursos_y_depto:
            print("No hay cursos disponibles en esta facultad.")
            continue
        
        print("Seleccione el curso:")
        for i, (curso, depto) in enumerate(cursos_y_depto):
            print(f"{i + 1} - {curso} (Departamento: {depto.nombre})")
        curso_index = int(input("Opción: ")) - 1
        if curso_index < 0 or curso_index >= len(cursos_y_depto):
            print("Opción no válida.")
            continue

        curso, departamento = cursos_y_depto[curso_index]
        if estudiante in curso.estudiantes:
            print(f"El estudiante {estudiante} ya está inscrito en el curso '{curso}'.")
            continue

        curso.inscribir_estudiante(estudiante)
        estudiante.inscribir_curso(curso)

        print(f"\nEstudiante {estudiante} inscripto en '{curso}' del departamento {departamento.nombre}.\n")

    elif opcion == "6":
        print("Saliendo del sistema...")
        break
    else:
        print("Opción no válida. Intente de nuevo.")

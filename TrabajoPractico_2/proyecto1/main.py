from modules.facultad import Facultad
from modules.departamento import Departamento
from modules.persona import Estudiante, Profesor
from modules.curso import Curso
from modules.persistencia import cargar_facultad_desde_personas_txt, cargar_sistema_txt, guardar_sistema_txt, cargar_estudiantes_y_profesores

facultades = []

print("Bienvenido al Sistema de Información Universitaria.")
opcion = input("¿Desea cargar una universidad guardada anteriormente? (s/n): ").lower()

if opcion == 's':
    facultades = cargar_sistema_txt()
    print("Universidad cargada correctamente.")

elif opcion == 'n':  
    estudiantes, profesores = cargar_estudiantes_y_profesores()
    nombre_facultad = input("Ingrese el nombre de la facultad: ")
    nombre_departamento = input("Ingrese el nombre del primer departamento: ")

    print("Elija el director del departamento (0 para profesor nuevo):")
    for i, prof in enumerate(profesores):
        print(f"{i + 1} - {prof}")

    opcion_director = int(input("Opción: ")) - 1
    if opcion_director == -1:
        nombre = input("Nombre del nuevo profesor: ")
        apellido = input("Apellido: ")
        dni = input("DNI: ")
        director = Profesor(nombre, apellido, dni)
        profesores.append(director)
    else:
        if opcion_director < 0 or opcion_director >= len(profesores):
            print("Opción no válida.")
            exit()
        director = profesores[opcion_director]

    facultad = Facultad(nombre_facultad, nombre_departamento, director)

    # agregar estudiantes y profesores a la facultad
    for est in estudiantes:
        facultad.agregar_estudiante(est)
    for prof in profesores:
        if prof != director:
            facultad.contratar_profesor(prof)

    facultades = [facultad]

    print("Facultad creada correctamente. Estudiantes y profesores cargados.")
else:
    print("Opción no válida")
    exit()

while True:
    print("\n")
    print("##########################################")
    print("#  Sistema de Información Universitaria  #")
    print("##########################################")
    print("Elige una opción")
    print("1 - Inscribir estudiante")
    print("2 - Contratar profesor")
    print("3 - Crear departamento nuevo")
    print("4 - Crear curso nuevo")
    print("5 - Inscribir estudiante a un curso")
    print("6 - Salir")
    
    opcion = input("Opción: ")
    
    if opcion == "1":
        # lógica para inscribir estudiante
        print("Ingrese los datos del estudiante:")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        dni = input("DNI: ")
        estudiante = Estudiante(nombre, apellido, dni)

        print("Seleccione la facultad donde inscribirlo/a:")
        for i, facultad in enumerate(facultades):
            print(f"{i + 1} - {facultad.nombre}")
        facultad_index = int(input("Opción: ")) - 1
        if facultad_index < 0 or facultad_index >= len(facultades):
            print("Opción no válida.")
            continue

        facultad = facultades[facultad_index]
        facultad.agregar_estudiante(estudiante)

        print(f"{estudiante} inscripto/a en {facultad}.\n")
        
        print("Estudiantes en la facultad en orden alfabético:")
        for est in sorted(facultad.listar_estudiantes()):
            print(est)
        
    elif opcion == "2":
        # lógica para contratar profesor
        print("Ingrese los datos del profesor:")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        dni = input("DNI: ")
        profesor = Profesor(nombre, apellido, dni)

        print("Seleccione la facultad:")
        for i, facultad in enumerate(facultades):
            print(f"{i + 1} - {facultad.nombre}")
        facultad_index = int(input("Opción: ")) - 1
        if facultad_index < 0 or facultad_index >= len(facultades):
            print("Opción no válida.")
            continue
        facultad = facultades[facultad_index]

        facultad.contratar_profesor(profesor)
        print(f"\nProfesor/a {profesor} contratado/a en {facultad}.\n")

        print("Profesores en la facultad en ordes alfabético:")
        for prof in sorted(facultad.listar_profesores()):
            print(prof)

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

        nombre_nuevo_departamento = input("Nombre del nuevo departamento: ")

        #se verifica si el departamento ya existe
        for depto in facultad.departamentos:
            if depto.nombre == nombre_nuevo_departamento:
                print(f"El departamento {nombre_nuevo_departamento} ya existe en la facultad {facultad}.")
                break
        else:
            # Si no existe, se crea el nuevo departamento y se asocia un profesor a él

            print("\nSeleccione el/la director/a del departamento entre los profesores existentes:")
            if not facultad.listar_profesores():
                print("No hay profesores disponibles para asignar como director/a. Por favor, contrate uno primero.")
                continue

            for i, prof in enumerate(facultad.listar_profesores()):
                print(f"{i + 1} - {prof}")
            profesor_index = int(input("Opción: ")) - 1
            if profesor_index < 0 or profesor_index >= len(facultad.profesores):
                print("Opción no válida.")
                continue
            
            profesor = facultad.profesores[profesor_index]
            if profesor.departamento_director:
                print(f"El/la profesor/a {profesor} ya es director/a del departamento {profesor.departamento_director.nombre}.")
                continue

            facultad.crear_departamento(nombre_nuevo_departamento, profesor)
            
            print(f"Departamento {nombre_nuevo_departamento} creado en la facultad {facultad}.\n")
            print(f"\nProfesor/a {profesor} asociado/a como director/a al departamento {nombre_nuevo_departamento}.\n")

        print("Departamentos en la facultad:")
        for depto in facultad.listar_departamentos():
            print(depto)
        
    elif opcion == "4":
        # lógica para crear curso nuevo
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
            print("La facultad aún no tiene departamentos. Por favor cree uno primero.")
            continue

        print("Seleccione el departamento donde se creará el curso:")
        for i, depto in enumerate(facultad.departamentos):
            print(f"{i + 1} - {depto.nombre}")
        depto_index = int(input("Opción: ")) - 1
        if depto_index < 0 or depto_index >= len(facultad.departamentos):
            print("Opción no válida.")
            continue
        departamento = facultad.departamentos[depto_index]

        #ingresar nombre del curso
        nombre_curso = input("Nombre del curso: ")

        #se verifica que haya profesores disponibles
        if not facultad.listar_profesores():
            print("No hay profesores en esta facultad para asignar como titular. Por favor, contrate uno/a primero.")
            continue

        print("Seleccione el/la profesor/a titular:")
        for i, prof in enumerate(facultad.listar_profesores()):
            print(f"{i + 1} - {prof}")
        prof_index = int(input("Opción: ")) - 1
        if prof_index < 0 or prof_index >= len(facultad.profesores):
            print("Opción no válida.")
            continue
        profesor = facultad.profesores[prof_index]

        #crear el curso y agregarlo al departamento
        nuevo_curso = Curso(nombre_curso, profesor)
        departamento.agregar_curso(nuevo_curso)

        print(f"\nCurso '{nombre_curso}' creado correctamente en el departamento {departamento.nombre}, con {profesor} como profesor/a titular.\n")

        print(f"Cursos actuales en el departamento: {departamento.nombre}")
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
            print("No hay estudiantes registrados en esta facultad. Por favor, inscriba uno/a primero.")
            continue

        print("Seleccione el/la estudiante a inscribir:")
        for i, est in enumerate(facultad.estudiantes):
            print(f"{i + 1} - {est}")
        est_index = int(input("Opción: ")) - 1
        if est_index < 0 or est_index >= len(facultad.estudiantes):
            print("Opción no válida.")
            continue
        estudiante = facultad.estudiantes[est_index]

        cursos_y_depto = facultad.obtener_cursos_con_departamento()
        if not cursos_y_depto:
            print("No hay cursos disponibles en esta facultad. Por favor, cree uno primero.")
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
            print(f"El/la estudiante {estudiante} ya está inscrito/a en el curso '{curso}'.")
            continue

        curso.inscribir_estudiante(estudiante)

        print(f"\nEstudiante {estudiante} inscripto/a en '{curso}' del departamento {departamento.nombre}.\n")

    elif opcion == "6":
        guardar = input("¿Desea guardar los cambios antes de salir? (s/n): ").lower()
        if guardar == 's':
            guardar_sistema_txt(facultades)
            print("Sistema guardado correctamente.")
        print("Saliendo del sistema...")
        break

    else:
        print("Opción no válida. Intente de nuevo.")

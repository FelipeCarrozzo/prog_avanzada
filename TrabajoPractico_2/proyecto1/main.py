from modules.facultad import Facultad
from modules.departamento import Departamento
from modules.persona import Estudiante, Profesor
from modules.curso import Curso
from modules.persistencia import cargar_facultad_desde_personas_txt, cargar_sistema_txt, guardar_sistema_txt

facultades = []

print("Bienvenido al Sistema de Información Universitaria.")
opcion = input("¿Desea cargar una universidad guardada anteriormente? (s/n): ").lower()

if opcion == 's':
    try:
        facultades = cargar_sistema_txt()
        print("Universidad cargada correctamente.")
    except FileNotFoundError:
        print("No se encontró un sistema guardado. Se creará uno nuevo.")
        nombre_facultad = input("Ingrese el nombre de la facultad: ")
        facultades = [cargar_facultad_desde_personas_txt(nombre_facultad)]
elif opcion == 'n':    
    nombre_facultad = input("Ingrese el nombre de la facultad: ")
    facultades = [cargar_facultad_desde_personas_txt(nombre_facultad)]
else:
    print("Opción no válida")
    exit()

while True:
    print("\n")
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
            print("Seleccione la facultad:")
            for i, facultad in enumerate(facultades):
                print(f"{i + 1} - {facultad.nombre}")
            facultad_index = int(input("Opción: ")) - 1
            if facultad_index < 0 or facultad_index >= len(facultades):
                print("Opción no válida.")
                continue
            facultad = facultades[facultad_index]

            nombre = input("Nombre del estudiante: ")
            apellido = input("Apellido del estudiante: ")
            dni = input("DNI: ")

            estudiante = Estudiante(nombre, apellido, dni)
            facultad.agregar_estudiante(estudiante)
            print(f"{estudiante} inscripto en {facultad}.\n")
            print("Estudiantes inscriptos en la facultad:")
            for est in facultad.listar_estudiantes():
                print(est)
        
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
                print("No hay profesores disponibles para asignar como director. Por favor, contrate uno primero.")
                continue
            for i, prof in enumerate(facultad.listar_profesores()):
                print(f"{i + 1} - {prof}")
            profesor_index = int(input("Opción: ")) - 1
            if profesor_index < 0 or profesor_index >= len(facultad.listar_profesores()):
                print("Opción no válida.")
                continue
            profesor = facultad.profesores[profesor_index]
            nuevo_profesor = profesor
            nuevo_departamento = Departamento(nuevo_departamento, nuevo_profesor)
            facultad.agregar_departamento(nuevo_departamento)
            nuevo_profesor.asociar_departamento(nuevo_departamento)
            
            print(f"Departamento {nuevo_departamento} creado en la facultad {facultad}.\n")
            print(f"\nProfesor {nuevo_profesor} asociado como director al departamento {nuevo_departamento}.\n")

        print("Departamentos en la facultad:")
        for depto in facultad.listar_departamentos():
            print(depto)
        
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
            print("La facultad aún no tiene departamentos. Por favor cree uno primero.")
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
            print("No hay profesores en esta facultad para asignar como titular. Por favor, contrate uno primero.")
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
            print("No hay estudiantes registrados en esta facultad. Por favor, inscriba uno primero.")
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
            print(f"El estudiante {estudiante} ya está inscrito en el curso '{curso}'.")
            continue

        curso.inscribir_estudiante(estudiante)
        estudiante.inscribir_curso(curso)

        print(f"\nEstudiante {estudiante} inscripto en '{curso}' del departamento {departamento.nombre}.\n")

    elif opcion == "6":
        guardar = input("¿Desea guardar los cambios antes de salir? (s/n): ").lower()
        if guardar == 's':
            guardar_sistema_txt(facultades)
            print("Sistema guardado correctamente.")
        print("Saliendo del sistema...")
        break

    else:
        print("Opción no válida. Intente de nuevo.")

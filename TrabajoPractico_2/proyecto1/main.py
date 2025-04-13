from modules.facultad import Facultad
from modules.departamento import Departamento
from modules.profesor import Profesor
from modules.estudiante import Estudiante
from modules.curso import Curso


facultades = [Facultad("Ingeniería"), Facultad("Ciencias Económicas")]


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
                print(f"{i + 1} - {facultad.get_nombre()}")
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
            print(f"{i + 1} - {facultad.get_nombre()}")
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
            print(f"{i + 1} - {facultad.get_nombre()}")
        facultad_index = int(input("Opción: ")) - 1
        if facultad_index < 0 or facultad_index >= len(facultades):
            print("Opción no válida.")
            continue
        facultad = facultades[facultad_index]

        nuevo_departamento = input("Nombre del nuevo departamento: ")

        # Verificar si el departamento ya existe
        for depto in facultad.listar_departamentos():
            if depto.get_nombre() == nuevo_departamento:
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


        
    elif opcion == "4":
        # lógica para crear curso nuevo
        pass
    elif opcion == "5":
        # lógica para inscribir estudiante a un curso
        pass
    elif opcion == "6":
        print("Saliendo del sistema...")
        break
    else:
        print("Opción no válida. Intente de nuevo.")
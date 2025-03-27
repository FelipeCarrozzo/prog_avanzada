def agregar_usuario_nfrases(lista_usuarios, n_usuario, n_frases):
    """Función que guarda la información de un libro a una lista
    de libros en forma de diccionario.
    """
    datos_usuario = {
            "usuario": n_usuario,
            "frases": n_frases
        }
    lista_usuarios.append(datos_usuario) 

def cargar_lista(nombre_archivo, lista_libros):
    """Función que lee la información de los usuarios desde un archivo
    y lo carga a una lista.
    """
    with open(nombre_archivo, "r") as archi:
        for linea in archi:
            libro = linea.rstrip().split(',')
            agregar_usuario_nfrases(lista_libros, libro[0], libro[1]) 

def guardar_usuario_en_archivo(nombre_archivo, n_usuario: str, n_frases: int): 
    """Guarda la información de un usuario y cant frases en archivo
    """   
    with open(nombre_archivo, "a") as archi:
        archi.write(f"{n_usuario},{n_frases}\n")

if __name__ == '__main__':
    lista = []
    a = agregar_usuario_nfrases(lista, "Tapalin", 3)

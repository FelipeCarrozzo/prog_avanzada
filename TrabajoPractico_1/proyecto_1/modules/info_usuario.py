def agregar_usuario_nfrases(lista_usuarios, n_usuario, n_frases):
    """Función que guarda la información de un libro a una lista
    de libros en forma de diccionario.
    """
    datos_usuario = {
            "usuario": n_usuario,
            "frases": n_frases
        }
    lista_usuarios.append(datos_usuario) 
 
def cargar_lista(nombre_archivo, lista_usuarios):
    """Función que lee la información de los usuarios desde un archivo
    y lo carga a una lista.
    """
    with open(nombre_archivo, "r") as archi:
        for linea in archi:
            libro = linea.rstrip().split(',')
            agregar_usuario_nfrases(lista_usuarios, libro[0], libro[1]) 

def guardar_usuario_en_archivo(nombre_archivo, n_usuario: str, n_frases: int, aciertos: int, fechayhora: str): 
    """Guarda la información del usuario: 
    nombre de usuario, num de frases, aciertos, fecha y hora del inicio de la trivia.
    """   
    with open(nombre_archivo, "a") as archi:
        archi.write(f"{n_usuario},{n_frases},{aciertos},{fechayhora}\n")

if __name__ == '__main__':
    guardar_usuario_en_archivo("./data/datos_usuario.txt", "usuario1", 5, 3, "2021-09-01 12:00:00")

#dependencias
import random

#funciones
def guardar_nombre_usuario(nombre_usuario: str, n_frases: int):
    '''
    Guarda el nombre del usuario en un diccionario

    Args:
        nombre_usuario (str): Nombre del usuario a guardar.
    '''
    with open("data/datos_usuario.txt", "w", encoding="utf-8") as archivo:
        archivo.write(f"{nombre_usuario},{n_frases}\n")


def listar_peliculas(nombre_archivo: str) -> list:
    '''
    Lee un diccionario (frase:película) y retorna una lista ordenada de las películas sin repetir, 
    asegurando que cada palabra en el nombre de la película tenga la inicial en mayúscula.

    Args:
        nombre_archivo (str): Ruta del archivo a leer.
    Returns:
        list: Lista de películas ordenadas sin repetir.
    '''
    datos_diccionario = cargar_datos_peliculas(nombre_archivo)
    
    # Aplicamos title() a cada película y guardo solo los valores
    conjunto_peliculas = {pelicula.title() for pelicula in datos_diccionario.values()}

    
    lista_peliculas_ordenada = sorted(conjunto_peliculas)  # Ordenamos la lista

    # Lista por comprensión con índice
    lista_peliculas_ord_index = [f"{i}. {pelicula}" for i, pelicula in enumerate(lista_peliculas_ordenada, start=1)]
    return lista_peliculas_ord_index


def cargar_datos_usuario(nombre_archivo: str) -> list:
    """
    Lee un archivo con datos de usuarios y la cantidad de frases. Retorna la ultima linea del archivo

    Args:
        nombre_archivo (str): Ruta del archivo a leer.

    Returns:
        list: Lista con los datos del último usuario registrado.
    """
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.split(",")
            usuario = partes[0].strip()
            nfrases = int(partes[1].strip())

    if usuario and nfrases:
        return usuario, nfrases
    else:
        print("No hay datos")

def cargar_datos_peliculas(nombre_archivo: str) -> dict:
    """
    Lee un archivo con frases y películas y las organiza en un diccionario 
    donde la clave es la frase y el valor es la película correspondiente.

    Args:
        nombre_archivo (str): Ruta del archivo a leer.

    Returns:
        dict: Diccionario con las frases como claves y las películas como valores.
    """
    datos = dict()
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split(";")
            if len(partes) == 2:  # si tiene dos datos por linea
                clave = partes[0].strip()
                valor = partes[1].strip().title() #en esta funcion no importa que se repitan las peliculas
                datos[clave] = valor
    return datos

def generar_frases_aleatorias(datos_peliculas: dict, n_frases: int) -> dict:
    """
    Genera un diccionario con N preguntas y respuestas de trivia a partir de un diccionario de datos de películas.

    Args:
        datos_peliculas (dict): Diccionario con frases como claves y películas como valores.
        n_frases (int): Número de frases a seleccionar para la trivia.

    Returns:
        dict: Diccionario con preguntas y respuestas.
    """
    preguntas_respuestas = dict()
    for i in range(n_frases):
        clave = random.choice(list(datos_peliculas.keys()))
        valor = datos_peliculas[clave]
        preguntas_respuestas[clave] = valor
        del datos_peliculas[clave]  # Eliminar la frase seleccionada para evitar repeticiones
    return preguntas_respuestas


def generar_intentos(preguntas_respuestas: dict, datos_peliculas: dict) -> list:
    """
    Genera una lista de preguntas con opciones aleatorias para mostrar en una página HTML.

    Args:
        preguntas_respuestas (dict): Diccionario con frases como claves y películas correctas como valores.
        datos_peliculas (dict): Diccionario original con frases y películas para obtener opciones incorrectas.

    Returns:
        list: Lista de preguntas, donde cada pregunta es un diccionario con la frase, opciones y la correcta.
    """
    preguntas_html = []

    for frase, pelicula_correcta in preguntas_respuestas.items():
        # Obtener todas las películas posibles y eliminar la correcta
        peliculas_incorrectas = list(set(datos_peliculas.values()) - {pelicula_correcta})
        
        # Seleccionar dos opciones incorrectas al azar
        opciones_incorrectas = random.sample(peliculas_incorrectas, 2)
        
        # Crear una lista con las opciones (correcta + incorrectas)
        opciones = opciones_incorrectas + [pelicula_correcta]
        
        # Mezclar el orden de las opciones
        random.shuffle(opciones)
        
        # Crear la estructura de la pregunta
        pregunta = {
            "frase": frase,
            "opciones": opciones,
            "correcta": pelicula_correcta
        }
        
        preguntas_html.append(pregunta)

    return preguntas_html


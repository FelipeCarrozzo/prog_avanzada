import random

def cargar_datos(DIRECCION: str) -> dict:
    """
    Lee un archivo con frases y películas y las organiza en un diccionario donde la clave es la frase
    y el valor es la película correspondiente.
    """
    frases_y_peliculas = {}

    with open(DIRECCION, "r", encoding="utf-8") as f:
        for linea in f:
            frase, pelicula = linea.strip().split(';')
            frases_y_peliculas[frase] = pelicula.strip().title()  # Normaliza la película

    return frases_y_peliculas

def listar_pelis(datos: dict) -> list[str]:
    """
    Retorna una lista de películas no repetidas, ordenadas alfabéticamente.
    """
    return sorted(set(p.lower().title() for p in datos.values()))

def selec_frases(datos: dict, N: int) -> list[str]:
    """
    Selecciona N frases aleatorias del diccionario, asegurando que N no supere la cantidad total de frases.
    """
    if N > len(datos):
        raise ValueError("N es mayor que el número de frases disponibles")
    return random.sample(list(datos.keys()), N)

def selec_peliculas(datos: dict, frase: str) -> list[str]:
    """
    Selecciona tres películas aleatorias para mostrar como opciones, asegurando que sean distintas.
    """
    pelicula_correcta = datos[frase]
    otras_peliculas = list(set(p.lower().title() for p in datos.values()) - {pelicula_correcta})
    opciones = [pelicula_correcta] + random.sample(otras_peliculas, 2)
    random.shuffle(opciones)  # Se mezclan las opciones para que la correcta no siempre esté en el mismo lugar
    return opciones
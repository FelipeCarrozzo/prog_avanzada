#funciones

def cargar_datos(nombre_archivo: str) -> dict:
    """
    Lee un archivo con frases y películas y las organiza en un diccionario donde la clave es la frase
    y el valor es la película correspondiente.

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
                valor = partes[1].strip().title()
                datos[clave] = valor
    return datos


def listar_peliculas(nombre_archivo:str) -> list:
    '''
    Lee un diccionario (frase:película) y retorna una lista ordenada de las películas sin repetir.

    Args:
        nombre_archivo (str): Ruta del archivo a leer.
    Returns:
        list: Lista de películas ordenadas sin repetir.
    '''
    datos_diccionario = cargar_datos("data/frases_de_peliculas.txt")
    conjunto_peliculas = set(datos_diccionario.values())  # Convertimos a set para eliminar duplicados
    lista_peliculas_ordenada = sorted(conjunto_peliculas)  # Ordenamos la lista

    # Lista por comprensión con índice
    lista_peliculas_ord_index = [f"{i}. {pelicula}" for i, pelicula in enumerate(lista_peliculas_ordenada, start=1)]
    return lista_peliculas_ord_index


if __name__ == "__main__":
    prueba = cargar_datos("data/frases_de_peliculas.txt")
    print(prueba)
    # prueba = listar_peliculas()
    # print(prueba)
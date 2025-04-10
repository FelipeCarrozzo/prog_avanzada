#dependencias
import random
import datetime


from fpdf import FPDF
from flask import send_file

#funciones

def cargar_datos_peliculas(nombre_archivo: str) -> dict:
    """
    Carga un archivo con frases y nombres de películas separadas por punto y coma (;)
    y devuelve un diccionario con las frases como claves y los nombres de películas como valores.

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

def listar_peliculas(nombre_archivo: str) -> list:
    """
    Lee un archivo con frases y películas, y retorna una lista ordenada de los nombres
    de películas sin repetir, con las palabras en formato título (mayúscula inicial).

    Args:
        nombre_archivo (str): Ruta del archivo con frases y películas separadas por punto y coma.

    Returns:
        list: Lista ordenada de nombres de películas formateados y enumerados.
    """
    datos_diccionario = cargar_datos_peliculas(nombre_archivo)
    
    # convertimos a set para evitar repeticiones
    conjunto_peliculas = set(datos_diccionario.values())
    lista_peliculas_ordenada = sorted(conjunto_peliculas)  # Ordenamos la lista

    # Lista por comprensión con índice
    lista_peliculas_ord_index = [f"{i}. {pelicula}" for i, pelicula in enumerate(lista_peliculas_ordenada, start=1)]
    return lista_peliculas_ord_index

def generar_frases_aleatorias(datos_peliculas: dict, n_frases: int) -> dict:
    """
    Genera un diccionario con N preguntas y respuestas de trivia a partir de un diccionario de datos de películas.

    Args:
        datos_peliculas (dict): Diccionario con frases como claves y películas como valores.
        n_frases (int): Número de frases a seleccionar para la trivia.

    Returns:
        dict: Diccionario con preguntas y respuestas.
    """
    frases_seleccionadas = random.sample(list(datos_peliculas.keys()), n_frases)

    #diccionario por comprensión con las frases seleccionadas y sus respectivas películas
    preguntas_respuestas = {frase: datos_peliculas[frase] for frase in frases_seleccionadas}
    return preguntas_respuestas


def generar_intentos(preguntas_respuestas: dict, datos_peliculas: dict) -> list:
    """
    Genera una lista de preguntas para la trivia, cada una con una frase,
    tres opciones (una correcta y dos incorrectas) y la respuesta correcta.

    Args:
        preguntas_respuestas (dict): Diccionario con frases como claves y películas correctas como valores.
        datos_peliculas (dict): Diccionario original con frases y películas para obtener opciones incorrectas.

    Returns:
        list: Lista de preguntas, donde cada pregunta es un diccionario con la frase, opciones y la correcta.
    """
    preguntas_html = []

    for frase, pelicula_correcta in preguntas_respuestas.items():
        peliculas_incorrectas = list(set(datos_peliculas.values()) - {pelicula_correcta}) #todas las películas posibles y eliminar la correcta
        opciones_incorrectas = random.sample(peliculas_incorrectas, 2) #seleccionar dos opciones incorrectas al azar
        opciones = opciones_incorrectas + [pelicula_correcta] #opciones correcta + incorrectas
        
        random.shuffle(opciones) #mezclo el orden de las opciones       

        pregunta = {
            "frase": frase,
            "opciones": opciones,
            "correcta": pelicula_correcta #estructura de la pregunta: dict
        }

        preguntas_html.append(pregunta) #agrego a la lista los diccionarios: lista de diccionarios

    return preguntas_html

def guardar_resultado_partida(usuario, n_frases, aciertos, fecha_hora, nombre_archivo): 
    """
    Guarda la información de una partida en un archivo .txt.

    Args:
        usuario (str): Nombre del usuario.
        n_frases (int): Número de frases seleccionadas.
        aciertos (int): Cantidad de respuestas correctas.
        fecha_hora (str): Fecha y hora de inicio de la partida (formato dd-mm-aa HH:MM).
        nombre_archivo (str): Ruta del archivo donde se guardará la información.
    """

    fecha_hora = datetime.datetime.strptime(fecha_hora, "%d-%m-%y %H:%M").strftime("%d-%m-%y %H:%M")

    with open(nombre_archivo, "a", encoding="utf-8") as archi:
        archi.write(f"{usuario},{n_frases},{aciertos},{fecha_hora}\n")

def leer_archivo_resultados_historicos(nombre_archivo):
    """Lee un archivo de texto con resultados históricos y devuelve una lista de listas con los datos de cada partida.

    Args:
        nombre_archivo (str): Ruta del archivo a leer con los resultados de las partidas.

    Returns:
        list: Lista de listas con los datos de cada partida.
    """
    lista_partidas = []
    with open(nombre_archivo, "r") as archi:
        for linea in archi:
            datos_partida = linea.strip().split(",")
            lista_partidas.append(datos_partida)
    return lista_partidas

def mostrar_resultados_formateados(lista_usuarios):
    """
    Devuelve una cadena con los datos de los usuarios formateados en forma de tabla.

    Args:
        lista_usuarios (list): Lista de listas con los datos de cada usuario.

    Returns:
        str: Tabla de resultados formateada como texto plano.
    """
    tabla = []
    tabla.append(f"{'Usuario':<20}{'Aciertos/N':<15}{'Fecha y Hora':<20}") #linea de titulos
    tabla.append("-" * 55) #linea de separacion

    for usuario, n_frases, aciertos, fecha_hora in lista_usuarios: #recorro elementos del .txt
        aciertos_n = f"{aciertos}/{n_frases}" #se juntan los aciertos/frases
        tabla.append(f"{usuario:<20}{aciertos_n:<15}{fecha_hora:<20}") #agrego linea a linea
    return "\n".join(tabla)


    """
    Genera un archivo PDF que contiene los gráficos de resultados generados por la función `generar_graficos`.

    Returns:
        str: Ruta del archivo PDF generado.
    """
    pdf_path = "data/graficos.pdf"
    
    pdf = FPDF() #creo el objeto PDF
    pdf.set_auto_page_break(auto=True, margin=15) #salto de página automático
    pdf.add_page() 
    pdf.set_font("Arial", "B", 16) # defino los estilos
    pdf.cell(190, 10, "Resultados en Graficos", ln=True, align="C") #celda de título centrada, con salto de linea

    #agrego gráficos
    pdf.image("data/grafico_lineas.png", x=10, y=30, w=180)
    pdf.ln(110) #espacio entre imágenes
    pdf.image("data/grafico_pie.png", x=10, y=150, w=180)

    #guardo el PDF y devuelvo la ruta
    pdf.output(pdf_path)
    return pdf_path
#dependencias
import random
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os
from fpdf import FPDF
from flask import send_file

#funciones

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
    
    # title() a cada película y guardo solo los valores
    conjunto_peliculas = {pelicula.title() for pelicula in datos_diccionario.values()}
    lista_peliculas_ordenada = sorted(conjunto_peliculas)  # Ordenamos la lista

    # Lista por comprensión con índice
    lista_peliculas_ord_index = [f"{i}. {pelicula}" for i, pelicula in enumerate(lista_peliculas_ordenada, start=1)]
    return lista_peliculas_ord_index

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
        del datos_peliculas[clave]  #eliminar la frase seleccionada para evitar repeticiones
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
        #obtener todas las películas posibles y eliminar la correcta
        peliculas_incorrectas = list(set(datos_peliculas.values()) - {pelicula_correcta})
        
        #seleccionar dos opciones incorrectas al azar
        opciones_incorrectas = random.sample(peliculas_incorrectas, 2)
        
        #crear una lista con las opciones (correcta + incorrectas)
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

def guardar_usuario_en_archivo(usuario, n_frases, aciertos, fecha_hora, nombre_archivo): 
        """Guarda la información del usuario en un archivo .txt a partir de una lista

        Args: 
            - lista con datos recopilados de 1 usuario
            - nombre de usuario
            - numero de frases
            - cantidad de aciertos
            - fecha y hora del inicio de la partida

        """
        try:
            # Asegurar que la fecha esté en el formato correcto antes de escribirla
            fecha_hora = datetime.datetime.strptime(fecha_hora, "%d-%m-%y %H:%M").strftime("%d-%m-%y %H:%M")
        except ValueError:
            # Si la fecha no está en el formato correcto, intentamos convertir desde otro formato
            fecha_hora = datetime.datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%y %H:%M")

        with open(nombre_archivo, "a", encoding="utf-8") as archi:
            archi.write(f"{usuario},{n_frases},{aciertos},{fecha_hora}\n")

def leer_archivo_resultados_historicos(nombre_archivo):
    """Lee un archivo de texto con resultados históricos y devuelve una lista de listas con los datos de cada usuario.

    Args:
        nombre_archivo (str): Ruta del archivo a leer.

    Returns:
        list: Lista de listas con los datos de cada usuario.
    """
    lista_usuarios = []
    with open(nombre_archivo, "r") as archi:
        for linea in archi:
            datos_usuario = linea.strip().split(",")
            lista_usuarios.append(datos_usuario)
    return lista_usuarios

def mostrar_resultados_formateados(lista_usuarios):
    """Muestra los resultados históricos en formato de tabla.

    Args:
        lista_usuarios (list): Lista de listas con los datos de cada usuario.
    """
    tabla = []
    tabla.append(f"{'Usuario':<20}{'Aciertos/N':<15}{'Fecha y Hora':<20}")
    tabla.append("-" * 55)

    for usuario, n_frases, aciertos, fecha_hora in lista_usuarios:
        aciertos_n = f"{aciertos}/{n_frases}"
        tabla.append(f"{usuario:<20}{aciertos_n:<15}{fecha_hora:<20}")
    return "\n".join(tabla)


def generar_graficos():
    """
    Genera gráficos de evolución de aciertos y desaciertos acumulados por fecha y de distribución total,
    y los guarda en la carpeta static.
    """
    ruta_data = "./data"
    
    # aseguro que exista la carpeta static
    if not os.path.exists(ruta_data):
        os.makedirs(ruta_data)

    #leo los datos desde el archivo de resultados
    ruta_archivo_resultados = "./data/resultados_partidas.txt"
    if not os.path.exists(ruta_archivo_resultados):
        return

    datos = []
    with open(ruta_archivo_resultados, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split(",")
            if len(partes) == 4:
                usuario, n_frases, aciertos, fecha_hora = partes
                fecha = fecha_hora.split(" ")[0]  # Extraer solo la fecha (dd-mm-aa)
                datos.append((fecha, int(aciertos), int(n_frases) - int(aciertos)))

    if not datos:
        return  # No hay datos para graficar

    df = pd.DataFrame(datos, columns=["Fecha", "Aciertos", "Desaciertos"])

    #agrupo por fecha y calcular el acumulado
    df_agrupado = df.groupby("Fecha").sum().reset_index()

    # Gráfico de evolución (líneas acumuladas)
    plt.figure(figsize=(8, 4))
    plt.plot(df_agrupado["Fecha"], df_agrupado["Aciertos"], marker="o", label="Aciertos", color="green")
    plt.plot(df_agrupado["Fecha"], df_agrupado["Desaciertos"], marker="x", label="Desaciertos", color="red")
    plt.xlabel("Fecha")
    plt.ylabel("Cantidad Acumulada")
    plt.title("Evolución Acumulada de Aciertos y Desaciertos")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()  # Ajusta márgenes automáticamente
    plt.subplots_adjust(bottom=0.2)  # Asegura espacio para el eje X
    plt.savefig(os.path.join(ruta_data, "grafico_lineas.png"))
    plt.close()

    # Gráfico de distribución (torta)
    total_aciertos = df["Aciertos"].sum()
    total_desaciertos = df["Desaciertos"].sum()

    plt.figure(figsize=(5, 5))
    plt.pie([total_aciertos, total_desaciertos], labels=["Aciertos", "Desaciertos"], autopct="%1.1f%%", colors=["green", "red"])
    plt.title("Distribución de Aciertos y Desaciertos")
    plt.savefig(os.path.join(ruta_data, "grafico_pie.png"))
    plt.close()


def generar_pdf():
    pdf_path = "data/graficos.pdf"
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "Resultados en Graficos", ln=True, align="C")

    # Agregar gráficos
    pdf.image("data/grafico_lineas.png", x=10, y=30, w=180)
    pdf.ln(110)
    pdf.image("data/grafico_pie.png", x=10, y=150, w=180)

    pdf.output(pdf_path)
    return pdf_path
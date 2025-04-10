import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Para evitar problemas con la interfaz gráfica
import pandas as pd
import os

def generar_graficos():
    """
    Genera gráficos de evolución de aciertos y desaciertos acumulados por fecha y de distribución total,
    y los guarda en la carpeta data.
    """
    ruta_data = "./data"
    
    # aseguro que exista la carpeta data
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

    #agrupo por fecha y calculo el acumulado
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
    plt.pie([total_aciertos, total_desaciertos], labels=["Aciertos - "+str(total_aciertos), "Desaciertos - "+str(total_desaciertos)], autopct="%1.1f%%", colors=["green", "red"])
    plt.title("Distribución de Aciertos y Desaciertos")
    plt.savefig(os.path.join(ruta_data, "grafico_pie.png"))
    plt.close()


def generar_pdf():
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
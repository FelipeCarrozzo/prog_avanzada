from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') 

class Graficador:
    def __init__(self):
        pass

    def graficarCantidadesReclamos(self, cantidades, ruta_salida=None):
        total = sum(cantidades.values())
        if total == 0:
            raise ValueError("No hay reclamos para graficar.")

        porcentajes = {estado: (count / total) * 100 for estado, count in cantidades.items()}

        plt.figure(figsize=(40, 34))
        plt.pie(
            porcentajes.values(),
            autopct='%1.1f%%',
            startangle=140
        )

        plt.rcParams.update({'font.size': 60})
        plt.title(f"Porcentaje de reclamos por estado\n(Cantidad total: {total})")
        plt.axis('equal')
        plt.tight_layout()
        plt.legend([f"{estado} ({cantidades[estado]})" for estado in porcentajes], loc='upper right', fontsize=60)

        if ruta_salida:
            plt.savefig(ruta_salida)
            plt.close()
            return ruta_salida
        else:
            plt.show()



def graficarPorcentajesReclamos(self, porcentajes, ruta_salida=None):
    """
    Grafica en un gráfico de torta los porcentajes de reclamos por estado e incluye los valores de los porcentajes.
    Args:
    porcentajes: diccionario con los porcentajes de reclamos por estado
    ruta_salida: opcional, nombre de archivo PNG de salida
    """

    plt.figure(figsize=(16, 12))

    # Graficar y capturar textos de autopct
    wedges, texts, autotexts = plt.pie(
        porcentajes.values(),
        labels=porcentajes.keys(),
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': 14}  #tamaño de las etiquetas
    )

    # También puedes cambiar el tamaño de las etiquetas si lo deseas:
    for text in texts:
        text.set_fontsize(16)  # Tamaño de etiquetas (nombres de las porciones)
    for autotext in autotexts:
        autotext.set_fontsize(16)  # Tamaño de los porcentajes

    plt.title('Porcentaje de reclamos por estado', fontsize=20)
    plt.tight_layout()
    plt.legend(porcentajes.keys(), fontsize=12)
    plt.axis('equal')

    if ruta_salida:
        plt.savefig(ruta_salida)
        plt.close()
        return ruta_salida


    def graficarPalabrasClave(self, palabras_frecuentes, ruta_salida=None):
        """
        palabras_frecuentes: lista de (palabra, frecuencia)
        ruta_salida: opcional, nombre de archivo PNG de salida
        """
        freqs = dict(palabras_frecuentes)

        wc = WordCloud(width=800, height=400, background_color="white")
        wc.generate_from_frequencies(freqs)
        wc.to_file(ruta_salida)
        return ruta_salida 
    

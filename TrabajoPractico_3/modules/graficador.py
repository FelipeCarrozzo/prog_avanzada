from wordcloud import WordCloud
import matplotlib.pyplot as plt

class Graficador:
    def __init__(self):
        pass

    def graficarPalabrasClave(self, palabras_frecuentes, ruta_salida=None):
        """
        palabras_frecuentes: lista de (palabra, frecuencia)
        ruta_salida: opcional, nombre de archivo PNG de salida
        """
        freqs = dict(palabras_frecuentes)

        wc = WordCloud(width=800, height=400, background_color="white")
        wc.generate_from_frequencies(freqs)
        wc.to_file(ruta_salida)
        return ruta_salida  # Devuelve la ruta como string
    

    # def graficarPorcentajesReclamos(self, porcentajes, ruta_salida=None):
    #     """
    #     grafica en un gráfico de torta los porcentajes de reclamos por estado.
    #     Args:
    #     porcentajes: diccionario con los porcentajes de reclamos por estado
    #     ruta_salida: opcional, nombre de archivo PNG de salida
    #     """
    #    plt.figure(figsize=(8, 8))
    #    plt.pie(porcentajes.values(), labels=porcentajes.keys(), autopct='%1.1f%%', startangle=140)
    #    plt.title('Porcentaje de Reclamos por Estado')
    #    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    #    if ruta_salida:
    #        plt.savefig(ruta_salida)
    #        plt.close()
    #        return ruta_salida

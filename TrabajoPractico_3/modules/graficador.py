from wordcloud import WordCloud
import matplotlib.pyplot as plt

class Graficador:
    def __init__(self):
        pass

    def graficarCantidadesReclamos(self, cantidades, ruta_salida=None):
        total = sum(cantidades.values())
        if total == 0:
            raise ValueError("No hay reclamos para graficar.")

        porcentajes = {estado: (count / total) * 100 for estado, count in cantidades.items()}

        plt.figure(figsize=(12, 8))
        plt.pie(
            porcentajes.values(),
            labels=[
                f"{estado} ({cantidades[estado]})" 
                for estado in porcentajes
            ],
            autopct='%1.1f%%',
            startangle=140
        )

        plt.title(f"Porcentaje de reclamos por estado\n(Cantidad total: {total})")
        plt.axis('equal')
        plt.tight_layout()

        if ruta_salida:
            plt.savefig(ruta_salida)
            plt.close()
            return ruta_salida
        else:
            plt.show()

    def graficarPorcentajesReclamos(self, porcentajes, ruta_salida=None):
        """
        grafica en un gráfico de torta los porcentajes de reclamos por estado e incluye los valores de los porcentajes.
        Args:
        porcentajes: diccionario con los porcentajes de reclamos por estado
        ruta_salida: opcional, nombre de archivo PNG de salida
        """
    
        plt.figure(figsize=(16, 12))
        plt.pie(porcentajes.values(), labels=porcentajes.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Porcentaje de reclamos por estado')
        plt.tight_layout()
        plt.legend(porcentajes.keys())
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
    

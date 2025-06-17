from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Para evitar problemas con el backend de matplotlib en entornos sin GUI

class Graficador:
    """
    Clase para generar gráficos y visualizaciones a partir de datos de reclamos.
    Permite graficar cantidades de reclamos por estado y generar nubes de palabras clave.
    """
    def __init__(self):
        pass

    def graficarCantidadesReclamos(self, cantidades, rutaSalida=None):
        """
        cantidades: dict con estados de reclamos y sus cantidades
        ruta_salida: opcional, nombre de archivo PNG de salida
        """
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

        if rutaSalida:
            plt.savefig(rutaSalida)
            plt.close()
            return rutaSalida
        else:
            plt.show()

    def graficarPalabrasClave(self, palabrasFrecuentes, rutaSalida=None):
        """
        palabras_frecuentes: lista de (palabra, frecuencia)
        ruta_salida: opcional, nombre de archivo PNG de salida
        """
        freqs = dict(palabrasFrecuentes)

        wc = WordCloud(width=800, height=400, background_color="white")
        wc.generate_from_frequencies(freqs)
        wc.to_file(rutaSalida)
        return rutaSalida
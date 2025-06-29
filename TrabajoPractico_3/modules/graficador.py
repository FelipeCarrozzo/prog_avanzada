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
        Calcula el porcentaje de reclamos por estado y genera un gráfico de torta.
        Args:
            cantidades (dict): Diccionario con la cantidad de reclamos por estado.
            rutaSalida (str): Ruta del archivo PNG de salida. Si es None, muestra el gráfico en pantalla.

        Returns:
            str: Ruta del archivo generado o None si se mostró en pantalla.
        """
        total = sum(cantidades.values())
        if total == 0:
            raise ValueError("No hay reclamos para graficar.")

        porcentajes = {estado: (count / total) * 100 for estado, count in cantidades.items()}

        plt.rcParams.update({'font.size': 20}) 
        plt.figure(figsize=(12, 8))
        plt.pie(
            porcentajes.values(),
            autopct='%1.1f%%',
            startangle=140,
            pctdistance=0.85 
        )
        plt.title(f"Porcentaje de reclamos por estado\n(Cantidad total: {total})")
        plt.axis('equal')
        plt.tight_layout()
        plt.legend([f"{estado} ({cantidades[estado]})" for estado in porcentajes], loc='upper right', fontsize=20)

        if rutaSalida:
            plt.savefig(rutaSalida, bbox_inches='tight')
            plt.close()
            return rutaSalida
        else:
            plt.show()

    def graficarPalabrasClave(self, palabrasFrecuentes, rutaSalida=None):
        """
        Genera una nube de palabras a partir de las palabras clave más frecuentes.
        Args:
            palabrasFrecuentes (list): Lista de tuplas con palabras y su frecuencia.
            rutaSalida (str): Ruta del archivo PNG de salida. Si es None, muestra la nube en pantalla.
        Returns:
            str: Ruta del archivo generado o None si se mostró en pantalla.
        """
        freqs = dict(palabrasFrecuentes)

        wc = WordCloud(width=800, height=400, background_color="white")
        wc.generate_from_frequencies(freqs)
        wc.to_file(rutaSalida)
        return rutaSalida
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from modules.monticulos import MonticuloMediana
from modules.reclamo import Reclamo

class generadorDeEstadisticas:
    def __init__(self):
        """
        Inicializa el generador de estadísticas.
        """
        pass

    def obtenerCantidadesReclamos(self, reclamos):
        """
        Calcula la cantidad de reclamos por estado (en proceso, resuelto o pendiente).

        Args:
            reclamos (list): Lista de objetos Reclamo.

        Returns:
            dict: Diccionario con las cantidades de reclamos por estado.
        """
        estados = Counter(r.estado for r in reclamos)
        return dict(estados)

    def obtenerPorcentajesReclamos(self, reclamos):
        """
        Calcula el porcentaje de reclamos por estado (en proceso, resuelto o pendiente).

        Args:
            reclamos (list): Lista de objetos Reclamo.

        Returns:
            dict: Diccionario con los porcentajes de reclamos por estado.
        """

        total = len(reclamos)
        if total == 0:
            return {}

        estados = Counter(r.estado for r in reclamos)
        porcentajes = {estado: (count / total) * 100 for estado, count in estados.items()}
        
        return porcentajes
    
    def obtenerPalabrasClave(self, reclamos, num_palabras=15):
        """
        Genera una lista de palabras clave a partir de los reclamos.
        Utiliza el tokenizador de NLTK para dividir las descripciones en palabras,
        y devuelve las `num_palabras` más frecuentes y su cuenta.

        Args:
            reclamos (list): Lista de objetos Reclamo.
            num_palabras (int): Número de palabras clave a devolver.

        Returns:
            list: Lista de tuplas con las palabras clave y su frecuencia.
        """
        todas = []
        stop_words = set(stopwords.words("spanish"))
        for r in reclamos:
            tokens = word_tokenize(r.descripcion.lower())
            filtrados = [t for t in tokens if t.isalpha() and t not in stop_words]
            todas.extend(filtrados)

        conteo = Counter(todas)
        return conteo.most_common(num_palabras)    
    
    def obtenerMedianas(self, reclamos):
        """
        Calcula las medianas de los tiempos de resolución de los reclamos con estado "en proceso" y "resueltos".

        Args:
            reclamos (list): Lista de objetos Reclamo.

        Returns:
            float: Mediana de los tiempos de resolución.
        """
        medianaEnProceso = None
        medianaResueltos = None
        monticuloEnProceso = MonticuloMediana()
        monticuloResuelto = MonticuloMediana()

        for r in reclamos:
            if r.tiempoResolucion is not None and r.estado == "en proceso":
                monticuloEnProceso.agregarValor(r.tiempoResolucion)

        medianaEnProceso = monticuloEnProceso.obtenerMediana()

        for r in reclamos:
            if r.tiempoResolucion is not None and r.estado == "resuelto":
                monticuloResuelto.agregarValor(r.tiempoResolucion)

        medianaResueltos = monticuloResuelto.obtenerMediana()

        return (medianaEnProceso, medianaResueltos)




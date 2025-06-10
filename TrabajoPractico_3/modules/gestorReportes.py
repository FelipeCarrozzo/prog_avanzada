from generadorDeEstadisticas import generadorDeEstadisticas
from graficador import Graficador
from repositorioAbstractoBD import RepositorioAbstractoBD

class GestorReportes:
    def __init__(self, repo: RepositorioAbstractoBD, departamento=None):
        self.__departamento = departamento
        self.__repositorio = repo
        self.__generadorDeEstadisticas = generadorDeEstadisticas()
        self.__graficador = Graficador()

        self.__reportes = None

    
    def generarEstadisticas(self, departamento=None):
        """
        Genera estadísticas de los reclamos y devuelve las palabras clave más frecuentes.
        
        Args:
            reclamos (list): Lista de objetos Reclamo.
            num_palabras (int): Número de palabras clave a devolver.
        
        Returns:
            list: Lista de tuplas con las palabras clave y su frecuencia.
        """

        palabras_clave = self.__generadorDeEstadisticas.obtenerPalabrasClave(self.__repositorio.obtenerRegistrosFiltro("departamento", departamento))
        medianas = self.__generadorDeEstadisticas.obtenerMedianas(self.__repositorio.obtenerRegistrosFiltro("departamento", departamento))
        porcentajes = self.__generadorDeEstadisticas.obtenerPorcentajesReclamos(self.__repositorio.obtenerRegistrosFiltro("departamento", departamento))
        return (palabras_clave, medianas, porcentajes)

    def generarGraficos(self):
        """
        Genera gráficos a partir de los reclamos y los muestra en la interfaz.

        Args:
            reclamos (list): Lista de objetos Reclamo.
        """
        palabras_clave = self.generarEstadisticas(self.__departamento)[0]
        rutaGraficoNube = self.__graficador.graficarPalabrasClave(palabras_clave)

        porcentajes = self.generarEstadisticas(self.__departamento)[2]
        rutaGraficoTorta = self.__graficador.graficarPorcentajesReclamos(porcentajes)

        return (rutaGraficoNube, rutaGraficoTorta)


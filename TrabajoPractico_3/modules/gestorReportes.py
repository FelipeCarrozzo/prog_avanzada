from modules.generadorDeEstadisticas import generadorDeEstadisticas
from modules.graficador import Graficador
from modules.gestorExportacion import GestorExportacion, ExportadorPDF, ExportadorHTML
from modules.repositorioAbstractoBD import RepositorioAbstractoBD

class GestorReportes:
    def __init__(self, repo: RepositorioAbstractoBD, departamento=None):
        self.__departamento = departamento
        self.__repositorio = repo
        self.__generadorDeEstadisticas = generadorDeEstadisticas()
        self.__graficador = Graficador()
        #self.__gestorExportacion = GestorExportacion()

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
        if departamento is None: #secretario
            # Si no se especifica un departamento, se obtienen estadísticas de todos los reclamos
            cantidades = self.__generadorDeEstadisticas.obtenerCantidadesReclamos(self.__repositorio.obtenerRegistrosTotales())
            #porcentajes = self.__generadorDeEstadisticas.obtenerPorcentajesReclamos(self.__repositorio.obtenerRegistrosTotales())
            palabras_clave = self.__generadorDeEstadisticas.obtenerPalabrasClave(self.__repositorio.obtenerRegistrosTotales())
            medianas = self.__generadorDeEstadisticas.obtenerMedianas(self.__repositorio.obtenerRegistrosTotales())
        else:
            # Si se especifica un departamento, se obtienen estadísticas filtradas por ese departamento
            cantidades = self.__generadorDeEstadisticas.obtenerCantidadesReclamos(self.__repositorio.obtenerRegistrosFiltro("departamento", departamento))
            palabras_clave = self.__generadorDeEstadisticas.obtenerPalabrasClave(self.__repositorio.obtenerRegistrosFiltro("departamento", departamento))
            medianas = self.__generadorDeEstadisticas.obtenerMedianas(self.__repositorio.obtenerRegistrosFiltro("departamento", departamento))
            #porcentajes = self.__generadorDeEstadisticas.obtenerPorcentajesReclamos(self.__repositorio.obtenerRegistrosFiltro("departamento", departamento))
        
        return (cantidades, medianas, palabras_clave)
        #return (porcentajes, medianas, palabras_clave)

    def generarGraficos(self):
        """
        Genera gráficos a partir de los reclamos y los muestra en la interfaz.

        Args:
            reclamos (list): Lista de objetos Reclamo.
        """
        cantidades = self.generarEstadisticas(self.__departamento)[0]
        #porcentajes = self.generarEstadisticas(self.__departamento)[0]
        palabras_clave = self.generarEstadisticas(self.__departamento)[2]

        rutaGraficoTorta = self.__graficador.graficarCantidadesReclamos(cantidades, ruta_salida=f"./static/grafico_torta_{self.__departamento}.png" if self.__departamento else "./static/grafico_torta_secretario.png")
        #rutaGraficoTorta = self.__graficador.graficarPorcentajesReclamos(porcentajes, ruta_salida=f"./data/grafico_torta_{self.__departamento}.png" if self.__departamento else "./data/grafico_torta_secretario.png")
        rutaGraficoNube = self.__graficador.graficarPalabrasClave(palabras_clave, ruta_salida=f"./static/grafico_nube_{self.__departamento}.png" if self.__departamento else "./static/grafico_nube_secretario.png")

        return (rutaGraficoTorta, rutaGraficoNube)
    
    def generarReporte(self, departamento=None):
        """
        Devuelve un diccionario con el gráfico de torta, las medianas y el gráfico de palabras clave.
        """
        if departamento is not None:
            self.__departamento = departamento

        return {
            "graficoTorta": self.generarGraficos()[0],
            "medianas": self.generarEstadisticas(self.__departamento)[1],
            "graficoNube": self.generarGraficos()[1]
        }

    
    def exportarReporte(self, formato, departamento=None):
        """
        Exporta el reporte en el formato especificado (PDF o HTML).

        Args:
            formato (str): Formato de exportación ('pdf' o 'html').

        Returns:
            str: Ruta del archivo exportado.
        """
        if departamento is not None:
            self.__departamento = departamento

        if formato == 'pdf':
            exportador = ExportadorPDF()
        elif formato == 'html':
            exportador = ExportadorHTML()
        else:
            raise ValueError("Formato de exportación no válido.")
        
        # Genera el reporte y lo exporta
        rutaReporte = exportador.exportar(self.generarReporte(self.__departamento), self.__departamento)

        return rutaReporte

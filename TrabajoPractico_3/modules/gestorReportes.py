from modules.generadorDeEstadisticas import generadorDeEstadisticas
from modules.graficador import Graficador
from modules.gestorExportacion import GestorExportacion, ExportadorPDF, ExportadorHTML
from modules.repositorioAbstractoBD import RepositorioAbstractoBD

class GestorReportes:
    """
    Clase para gestionar la generación de reportes de reclamos.
    Permite generar estadísticas, gráficos y exportar reportes en diferentes formatos.
    """

    def __init__(self, repo: RepositorioAbstractoBD):

        self.__repositorio = repo
        self.__generadorDeEstadisticas = generadorDeEstadisticas()
        self.__graficador = Graficador()

    def obtenerReclamos(self, departamento=None):
        """
        Obtiene los reclamos según el departamento actual.
        Args:
            departamento (str): Nombre del departamento para filtrar los reclamos.
        Returns:
            list: Lista de objetos Reclamo filtrados por departamento o todos los reclamos.
        """
        if departamento:
            reclamos = self.__repositorio.obtenerRegistrosFiltro("departamento", departamento)
        else:
            reclamos = self.__repositorio.obtenerRegistrosTotales()

        return reclamos or []
    

    def generarEstadisticas(self, departamento=None):
        """
        Calcula estadísticas a partir de los reclamos.
        Args:
            departamento (str): Nombre del departamento para filtrar los reclamos.
        Returns:
            tuple: (cantidades, medianas, palabrasClave)
        """
        reclamos = self.obtenerReclamos(departamento)
        if not reclamos:
            return {}, {}, {}

        cantidades = self.__generadorDeEstadisticas.obtenerCantidadesReclamos(reclamos)
        palabrasClave = self.__generadorDeEstadisticas.obtenerPalabrasClave(reclamos)
        medianas = self.__generadorDeEstadisticas.obtenerMedianas(reclamos)

        return cantidades, medianas, palabrasClave
    
    def generarGraficos(self, cantidades, palabrasClave, departamento=None):
        """
        Genera gráficos a partir de los datos ya calculados.
        Returns:
            tuple: rutas de los gráficos generados
        """
        depto = departamento or "secretariaTecnica" 
        rutaGraficoTorta = self.__graficador.graficarCantidadesReclamos(
            cantidades, rutaSalida=f"./data/grafico_torta_{depto}.png"
        )
        rutaGraficoNube = self.__graficador.graficarPalabrasClave(
            palabrasClave, rutaSalida=f"./data/grafico_nube_{depto}.png"
        )
        return rutaGraficoTorta, rutaGraficoNube

    def generarReporte(self, departamento=None):
        """
        Genera un reporte de reclamos para el departamento especificado.
        Devuelve un diccionario con gráficos y datos estadísticos.
        """
        cantidades, medianas, palabrasClave = self.generarEstadisticas(departamento)
        if not cantidades:
            raise ValueError("No hay reclamos para generar el reporte.")
        
        graficoTorta, graficoNube = self.generarGraficos(cantidades, palabrasClave)

        return {
            "graficoTorta": graficoTorta,
            "graficoNube": graficoNube,
            "medianas": medianas
        }

    def exportarReporte(self, formato, departamento=None):
        """
        Exporta el reporte en PDF o HTML.
        """
        datos = self.generarReporte(departamento)

        if formato == 'pdf':
            exportador = ExportadorPDF()
        elif formato == 'html':
            exportador = ExportadorHTML()
        else:
            raise ValueError("Formato de exportación no válido.")

        return exportador.exportar(datos, departamento)
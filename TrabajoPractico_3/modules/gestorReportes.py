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

    def obtenerReclamos(self):
        """
        Obtiene los reclamos según el departamento actual.
        Returns:
            list: Lista de objetos Reclamo filtrados por departamento o todos los reclamos.
        """
        if self.__departamento:
            reclamos = self.__repositorio.obtenerRegistrosFiltro("departamento", self.__departamento)
        else:
            reclamos = self.__repositorio.obtenerRegistrosTotales()

        return reclamos or []
    

    def generarEstadisticas(self):
        """
        Calcula estadísticas a partir de los reclamos.
        Returns:
            tuple: (cantidades, medianas, palabrasClave)
        """
        reclamos = self.obtenerReclamos()
        if not reclamos:
            return {}, {}, {}

        cantidades = self.__generadorDeEstadisticas.obtenerCantidadesReclamos(reclamos)
        palabrasClave = self.__generadorDeEstadisticas.obtenerPalabrasClave(reclamos)
        medianas = self.__generadorDeEstadisticas.obtenerMedianas(reclamos)

        return cantidades, medianas, palabrasClave

    def generarGraficos(self, cantidades, palabrasClave):
        """
        Genera gráficos a partir de los datos ya calculados.
        Returns:
            tuple: rutas de los gráficos generados
        """
        depto_str = self.__departamento or "secretariaTecnica"
        rutaGraficoTorta = self.__graficador.graficarCantidadesReclamos(
            cantidades, rutaSalida=f"./data/grafico_torta_{depto_str}.png"
        )
        rutaGraficoNube = self.__graficador.graficarPalabrasClave(
            palabrasClave, rutaSalida=f"./data/grafico_nube_{depto_str}.png"
        )
        return rutaGraficoTorta, rutaGraficoNube

    def generarReporte(self, departamento=None):
        """
        Genera un reporte de reclamos para el departamento especificado.
        Devuelve un diccionario con gráficos y datos estadísticos.
        """
        if departamento is not None:
            self.__departamento = departamento

        cantidades, medianas, palabrasClave = self.generarEstadisticas()
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
        if departamento is not None:
            self.__departamento = departamento

        datos = self.generarReporte()

        if formato == 'pdf':
            exportador = ExportadorPDF()
        elif formato == 'html':
            exportador = ExportadorHTML()
        else:
            raise ValueError("Formato de exportación no válido.")

        return exportador.exportar(datos, self.__departamento)

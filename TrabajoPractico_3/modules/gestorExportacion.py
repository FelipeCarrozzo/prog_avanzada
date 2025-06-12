from abc import ABC, abstractmethod
from datetime import datetime
from modules.repositorioAbstractoBD import RepositorioAbstractoBD

class GestorExportacion(ABC):
    def __init__(self, datosReporte):
        self.datosReporte = datosReporte

    @abstractmethod
    def exportar(self, datosReporte, departamento=None):
        pass

class ExportadorPDF(GestorExportacion):
    def exportar(self, datosReporte, departamento=None):
        ruta = f"./data/reporte_{departamento or 'todos'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(datosReporte['graficoTorta'] + "\n")
            f.write(f"Mediana de tiempo de resolución de reclamos en proceso: {datosReporte['medianas'][0]} días\n")
            f.write(f"Mediana de tiempo de resolución de reclamos resueltos: {datosReporte['medianas'][1]} días\n")
            f.write("Palabras clave más frecuentes:\n")
            f.write(datosReporte['graficoNube'] + "\n")
        return ruta

class ExportadorHTML(GestorExportacion):
    def exportar(self, datosReporte, departamento=None):
        ruta = f"./data/reporte_{departamento or 'todos'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("<html><body>")
            f.write("<h1>📊 Reporte HTML</h1>")
            f.write(f"<img src='{datosReporte['graficoTorta']}' width='400'><br>")
            f.write(f"<p><strong>Medianas de tiempo de resolución de reclamos en proceso:</strong> {datosReporte['medianas'][0]} días</p>")
            f.write(f"<p><strong>Medianas de tiempo de resolución de reclamos resueltos:</strong> {datosReporte['medianas'][1]} días</p>")
            f.write("<h2>Palabras clave más frecuentes:</h2>")
            f.write(f"<img src='{datosReporte['graficoNube']}' width='400'>")
            f.write("</body></html>")
        return ruta
from abc import ABC, abstractmethod
from datetime import datetime
from modules.repositorioAbstractoBD import RepositorioAbstractoBD
import shutil
import os

class GestorExportacion(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def exportar(self, datosReporte, departamento=None):
        pass

class ExportadorPDF(GestorExportacion):
    def exportar(self, datosReporte, departamento=None):
        ruta = f"./data/reporte_{departamento or 'todos'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(datosReporte['graficoTorta'] + "\n")
            f.write(f"Mediana de tiempo de resolución de reclamos en proceso: {datosReporte['medianas'].get('enProceso', 0)} días\n")
            f.write(f"Mediana de tiempo de resolución de reclamos resueltos: {datosReporte['medianas'].get('resueltos', 0)} días\n")
            f.write("Palabras clave más frecuentes:\n")
            f.write(datosReporte['graficoNube'] + "\n")
        return ruta

class ExportadorHTML(GestorExportacion):
    def exportar(self, datosReporte, departamento=None):
        nombre = f"reporte_{departamento or 'todos'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        carpeta = "data"
        os.makedirs(carpeta, exist_ok=True)

        # Copiar imágenes al mismo directorio que el HTML
        ruta_torta = os.path.join(carpeta, f"{nombre}_torta.png")
        ruta_nube = os.path.join(carpeta, f"{nombre}_nube.png")
        shutil.copy(datosReporte["graficoTorta"], ruta_torta)
        shutil.copy(datosReporte["graficoNube"], ruta_nube)

        ruta_html = os.path.join(carpeta, f"{nombre}.html")
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write("<html><body>")
            f.write("<h1>Reporte HTML</h1>")
            f.write(f"<img src='{os.path.basename(ruta_torta)}' width='400'><br>")
            f.write(f"<p><strong>Medianas en proceso:</strong> {datosReporte['medianas'].get('enProceso', 0)} días</p>")
            f.write(f"<p><strong>Medianas resueltos:</strong> {datosReporte['medianas'].get('resueltos', 0)} días</p>")
            f.write("<h2>Palabras clave más frecuentes:</h2>")
            f.write(f"<img src='{os.path.basename(ruta_nube)}' width='400'>")
            f.write("</body></html>")

        return ruta_html

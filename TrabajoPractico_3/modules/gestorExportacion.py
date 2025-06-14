from abc import ABC, abstractmethod
from datetime import datetime
from modules.repositorioAbstractoBD import RepositorioAbstractoBD
import os
from fpdf import FPDF

class GestorExportacion(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def exportar(self, datosReporte, departamento=None):
        pass

class ExportadorPDF(GestorExportacion):
    def exportar(self, datosReporte, departamento=None):
        nombre = f"reporte_{departamento or 'todos'}"
        ruta = f"./data/{nombre}.pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Reporte de Reclamos", ln=True, align="C")
        pdf.ln(10)

        pdf.cell(200, 10, txt="Mediana de tiempo de resolución de reclamos en proceso (en días): " +
                 str(datosReporte['medianas'].get('enProceso', 0)), ln=True)
        pdf.cell(200, 10, txt="Mediana de tiempo de resolución de reclamos resueltos (en días): " +
                 str(datosReporte['medianas'].get('resueltos', 0)), ln=True)

        # Agregar gráficos (solo si fpdf puede cargar imágenes)
        pdf.ln(10)
        pdf.cell(200, 10, txt="Porcentaje de reclamos por estado:", ln=True)
        pdf.image(datosReporte['graficoTorta'], w=160)

        pdf.ln(10)
        pdf.cell(200, 10, txt="Palabras clave:", ln=True)
        pdf.image(datosReporte['graficoNube'], w=160)

        pdf.output(ruta)
        return ruta

class ExportadorHTML(GestorExportacion):
    def exportar(self, datosReporte, departamento=None):
        import shutil

        nombre = f"reporte_{departamento or 'todos'}"
        carpeta = "data"
        os.makedirs(carpeta, exist_ok=True)

        ruta_css_original = os.path.join("static", "style.css")
        ruta_css_destino = os.path.join(carpeta, "style.css")
        if os.path.exists(ruta_css_original) and not os.path.exists(ruta_css_destino):
            shutil.copy(ruta_css_original, ruta_css_destino)

        ruta_torta = datosReporte["graficoTorta"]
        ruta_nube = datosReporte["graficoNube"]

        nombre_torta = os.path.basename(ruta_torta)
        nombre_nube = os.path.basename(ruta_nube)

        nueva_ruta_torta = os.path.join(carpeta, nombre_torta)
        nueva_ruta_nube = os.path.join(carpeta, nombre_nube)

        # Copiar si no existen
        if not os.path.exists(nueva_ruta_torta):
            shutil.copy(ruta_torta, nueva_ruta_torta)
        if not os.path.exists(nueva_ruta_nube):
            shutil.copy(ruta_nube, nueva_ruta_nube)

        ruta_html = os.path.join(carpeta, f"{nombre}.html")
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>")
            f.write("<html lang='es'>")
            f.write("<head>")
            f.write("<meta charset='UTF-8'>")
            f.write("<title>Reporte HTML</title>")
            f.write("<link rel='stylesheet' href='style.css'>")  # Apunta al CSS en la misma carpeta
            f.write("</head>")
            f.write("<body>")
            f.write("<h1>Reporte HTML</h1>")
            f.write(f"<img src='{nombre_torta}' width='400'><br>")
            f.write(f"<p><strong>Medianas en proceso:</strong> {datosReporte['medianas'].get('enProceso', 0)} días</p>")
            f.write(f"<p><strong>Medianas resueltos:</strong> {datosReporte['medianas'].get('resueltos', 0)} días</p>")
            f.write("<h2>Palabras clave más frecuentes:</h2>")
            f.write(f"<img src='{nombre_nube}' width='400'>")
            f.write("</body></html>")

        return ruta_html
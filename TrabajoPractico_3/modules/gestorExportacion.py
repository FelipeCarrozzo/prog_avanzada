from abc import ABC, abstractmethod
from datetime import datetime
from modules.repositorioAbstractoBD import RepositorioAbstractoBD
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


class GestorExportacion(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def exportar(self, datosReporte, departamento=None):
        pass

class ExportadorPDF(GestorExportacion):
    """
    Clase para exportar reportes en formato PDF.
    Utiliza ReportLab para generar el PDF con los datos del reporte.
    """
    def exportar(self, datosReporte, departamento=None):
        nombre = f"reporte_{departamento or 'todos'}"
        ruta = os.path.join("data", f"{nombre}.pdf")

        doc = SimpleDocTemplate(ruta, pagesize=letter, title="Reporte de reclamos")
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Reporte de reclamos", styles["Title"]))
        elements.append(Spacer(1, 12))

        # Tabla de reclamos
        reclamos = datosReporte.get("reclamos", [])
        if reclamos:
            elements.append(Paragraph("Listado de Reclamos", styles["Heading2"]))
            data = [["ID", "Estado", "Descripción"]]
            for r in reclamos:
                if isinstance(r, dict):
                    rid = r.get("id", "")
                    estado = r.get("estado", "")
                    descripcion = r.get("descripcion", "")
                else:
                    rid = getattr(r, "id", "")
                    estado = getattr(r, "estado", "")
                    descripcion = getattr(r, "descripcion", "")
                data.append([str(rid), str(estado), str(descripcion)])
            table = Table(data, colWidths=[50, 100, 300])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 18))

        # Analítica
        elements.append(Paragraph("Datos de Analítica", styles["Heading2"]))
        elements.append(Paragraph(
            f"Mediana de tiempos de resolución de reclamos en proceso (en días): {datosReporte['medianas'].get('enProceso', 0)}",
            styles["Normal"]))
        elements.append(Paragraph(
            f"Mediana de tiempos de resolución de reclamos resueltos (en días): {datosReporte['medianas'].get('resueltos', 0)}",
            styles["Normal"]))
        elements.append(Spacer(1, 12))

        # Gráfico torta
        if os.path.exists(datosReporte['graficoTorta']):
            elements.append(Paragraph("Gráfico de reclamos por estado:", styles["Heading3"]))
            img_torta = Image(datosReporte['graficoTorta'])
            img_torta._restrictSize(400, 300)
            elements.append(img_torta)
            elements.append(Spacer(1, 12))

        # Gráfico nube
        if os.path.exists(datosReporte['graficoNube']):
            elements.append(Paragraph("Nube de palabras clave:", styles["Heading3"]))
            img_nube = Image(datosReporte['graficoNube'])
            img_nube._restrictSize(400, 300)
            elements.append(img_nube)
            elements.append(Spacer(1, 12))

        doc.build(elements)
        return ruta

class ExportadorHTML(GestorExportacion):
    """
    Clase para exportar reportes en formato HTML.
    Genera un archivo HTML con los datos del reporte y gráficos.
    """
    def exportar(self, datosReporte, departamento=None):
        import shutil

        nombre = f"reporte_{departamento or 'todos'}"
        carpeta = "data"
        os.makedirs(carpeta, exist_ok=True)

        ruta_torta = os.path.abspath(datosReporte["graficoTorta"])
        ruta_nube = os.path.abspath(datosReporte["graficoNube"])

        ruta_html = os.path.join(carpeta, f"{nombre}.html")

        css_content = """
        body { font-family: 'Segoe UI', sans-serif; background-color: #f5f7fa; color: #2c3e50; padding: 40px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        h1, h2, h3 { color: #2c3e50; }
        p { font-size: 1em; margin-top: 20px; }
        img { display: block; margin: 20px auto; max-width: 90%; height: auto; border: 1px solid #ccc; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f2f2f2; }
        """

        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html><html lang='es'><head>")
            f.write("<meta charset='UTF-8'><title>Reporte</title>")
            f.write(f"<style>{css_content}</style>")
            f.write("</head><body>")
            f.write("<h1>Reporte HTML de Reclamos</h1>")

            # Tabla de reclamos
            reclamos = datosReporte.get("reclamos", [])
            if reclamos:
                f.write("<h2>Listado de Reclamos</h2>")
                f.write("<table><tr><th>ID</th><th>Estado</th><th>Descripción</th></tr>")
                for r in reclamos:
                    rid = getattr(r, "id", None)
                    if rid is None and isinstance(r, dict):
                        rid = r.get("id")
                    estado = getattr(r, "estado", None)
                    if estado is None and isinstance(r, dict):
                        estado = r.get("estado")
                    descripcion = getattr(r, "descripcion", None)
                    if descripcion is None and isinstance(r, dict):
                        descripcion = r.get("descripcion")
                    f.write(f"<tr><td>{rid}</td><td>{estado}</td><td>{descripcion}</td></tr>")
                f.write("</table>")

            # Analítica
            f.write("<h2>Datos de Analítica</h2>")
            f.write(f"<p><strong>Mediana de tiempos de resolución de reclamos en proceso (en días):</strong> {datosReporte['medianas'].get('enProceso', 0)}</p>")
            f.write(f"<p><strong>Mediana de tiempos de resolución de reclamos resueltos (en días):</strong> {datosReporte['medianas'].get('resueltos', 0)}</p>")

            f.write("<h3>Gráfico de reclamos por estado</h3>")
            f.write(f"<img src='file:///{ruta_torta}' width='500'>")

            f.write("<h3>Nube de palabras clave</h3>")
            f.write(f"<img src='file:///{ruta_nube}' width='500'>")

            f.write("</body></html>")

        return ruta_html
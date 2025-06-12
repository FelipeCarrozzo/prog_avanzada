#clase abstracta GestorExportacion que tiene como hijas ExportadorPDF y ExportadorHTML
from abc import ABC, abstractmethod
from datetime import datetime
from modules.repositorioAbstractoBD import RepositorioAbstractoBD

class GestorExportacion(ABC):
    def __init__(self, gestor):
        self.gestor = gestor

    @abstractmethod
    def exportar(self, formato):
        pass

class ExportadorPDF(GestorExportacion):
    
    def exportar(self, formato):
        if formato == 'pdf':
            return self.exportar_pdf()
        else:
            return super().exportar(formato)

    def exportar_pdf(self):
        # Implementación de la exportación a PDF
        pass

class ExportadorHTML(GestorExportacion):
    def exportar(self, formato):
        if formato == 'html':
            return self.exportar_html()
        else:
            return super().exportar(formato)

    def exportar_html(self):
        # Implementación de la exportación a HTML
        pass
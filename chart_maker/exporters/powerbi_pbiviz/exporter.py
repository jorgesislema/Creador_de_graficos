# exporter.py
# Exportador para Power BI pbiviz
from ..base import IExporter

class PowerBIPbivizExporter(IExporter):
    def export(self, spec, output_path: str):
        # Lógica para exportar a pbiviz usando plantillas
        pass

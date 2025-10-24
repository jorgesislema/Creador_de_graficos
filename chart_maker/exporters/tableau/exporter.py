# exporter.py
# Exportador para Tableau
from ..base import IExporter

TWB_TEMPLATE = """
<?xml version='1.0' encoding='utf-8' ?>
<workbook original-version='2022.1'>
    <worksheets>
        <worksheet name='Hoja 1'>
            <!-- Marcador de posición generado automáticamente -->
        </worksheet>
    </worksheets>
    <windows>
        <window>
            <view name='Hoja 1'/>
        </window>
    </windows>
</workbook>
"""

class TableauExporter(IExporter):
    def export(self, spec, output_path: str):
                # Implementación mínima: escribimos un TWB básico
                with open(output_path, "w", encoding="utf-8") as f:
                        f.write(TWB_TEMPLATE)
                return True

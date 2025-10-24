# exporter.py
# Exportador para script Python de Power BI
from ..base import IExporter
import json

class PowerBIPythonExporter(IExporter):
    def export(self, spec, output_path: str):
        # Implementación mínima: escribimos un script Python genérico con metadatos
        content = (
            "# Power BI Python Visual Script\n"
            "# Este script es un marcador de posición generado automáticamente.\n\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n\n"
            "# Datos: el usuario debe conectar el dataset de Power BI a 'dataset'\n"
            "# dataset = pd.DataFrame(...)\n\n"
            f"# Spec: {json.dumps(getattr(spec, 'dict', lambda: spec)(), ensure_ascii=False) if hasattr(spec, 'dict') else str(spec)}\n"
            "plt.figure()\n"
            "plt.title('Gráfico generado - marcador de posición')\n"
            "plt.plot([0,1],[0,1])\n"
            "plt.show()\n"
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

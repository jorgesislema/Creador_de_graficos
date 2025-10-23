# exporter.py
# Exportador para Looker Studio
from ..base import IExporter
import json

class LookerStudioExporter(IExporter):
    def export(self, spec, output_path: str):
        # Implementación mínima: JSON con metadatos de marcador de posición
        payload = {
            "type": "looker_studio_report",
            "title": "Reporte de ejemplo",
            "spec": spec.dict() if hasattr(spec, "dict") else str(spec),
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        return True

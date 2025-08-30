# __init__.py
# Exportadores disponibles

from .base import IExporter
from .powerbi_python.exporter import PowerBIPythonExporter
from .tableau.exporter import TableauExporter
from .looker.exporter import LookerExporter
from .looker_studio.exporter import LookerStudioExporter

# Registro de exportadores disponibles
EXPORTERS = {
    'powerbi_python': PowerBIPythonExporter,
    'tableau': TableauExporter,
    'looker': LookerExporter,
    'looker_studio': LookerStudioExporter
}

def get_exporter(exporter_type: str) -> IExporter:
    """
    Obtiene una instancia del exportador solicitado
    """
    if exporter_type not in EXPORTERS:
        raise ValueError(f"Exportador no soportado: {exporter_type}. Disponibles: {list(EXPORTERS.keys())}")
    
    return EXPORTERS[exporter_type]()

def list_exporters():
    """
    Lista todos los exportadores disponibles
    """
    return list(EXPORTERS.keys())
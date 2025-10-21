"""
Registro de exportadores y funciones de acceso.
"""

from .powerbi_python.exporter_new import PowerBIPythonExporter
from .tableau.exporter_new import TableauExporter
from .looker.exporter import LookerExporter
from .looker_studio.exporter import LookerStudioExporter

_EXPORTERS = {
	"powerbi_python": PowerBIPythonExporter,
	"tableau": TableauExporter,
	"looker": LookerExporter,
	"looker_studio": LookerStudioExporter,
}


def list_exporters():
	"""Devolvemos la lista de claves de exportadores disponibles."""
	return list(_EXPORTERS.keys())


def get_exporter(name: str):
	"""Obtenemos una instancia de exportador por nombre."""
	cls = _EXPORTERS.get(name)
	if not cls:
		raise ValueError(f"Exportador desconocido: {name}")
	return cls()


"""
Interfaz base para exportadores.
Cada exportador debe implementar el método export(spec, output_path) y devolver True en caso de éxito.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IExporter(ABC):
    """Contrato mínimo de un exportador."""

    @abstractmethod
    def export(self, spec: Any, output_path: str) -> bool:
        """
        Genera el artefacto de salida en output_path a partir de spec.
        Debe devolver True si el archivo se generó correctamente.
        """
        raise NotImplementedError

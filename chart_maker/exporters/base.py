# base.py
# Interfaz base para exportadores
from abc import ABC, abstractmethod

class IExporter(ABC):
    @abstractmethod
    def export(self, spec, output_path: str):
        pass

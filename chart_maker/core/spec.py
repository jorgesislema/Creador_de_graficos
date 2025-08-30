# spec.py
# Definición de ChartSpec usando Pydantic
from pydantic import BaseModel, validator, Field
from typing import Any, Dict, List, Union, Optional
from .chart_types import CHART_TYPES

class ChartSpec(BaseModel):
    type: str = Field(..., description="Tipo de gráfico")
    data: Union[List[Dict], Dict] = Field(..., description="Datos del gráfico")
    encoding: Dict[str, Any] = Field(..., description="Codificación visual")
    options: Dict[str, Any] = Field(default_factory=dict, description="Opciones adicionales")
    
    @validator('type')
    def validate_chart_type(cls, v):
        if v not in CHART_TYPES:
            raise ValueError(f'Tipo de gráfico no soportado: {v}. Tipos válidos: {CHART_TYPES}')
        return v
    
    @validator('data')
    def validate_data(cls, v):
        if not v:
            raise ValueError('Los datos no pueden estar vacíos')
        return v
    
    @validator('encoding')
    def validate_encoding(cls, v, values):
        # Permitir encoding vacío para ciertos tipos de gráficos
        allowed_empty_encoding = ['table', 'kpi', 'gauge']
        chart_type = values.get('type')
        
        if not v and chart_type not in allowed_empty_encoding:
            raise ValueError('La codificación no puede estar vacía para este tipo de gráfico')
        return v

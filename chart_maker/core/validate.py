# validate.py
# Validación de ChartSpec
from .spec import ChartSpec
from pydantic import ValidationError

def validate_chart_spec(data) -> ChartSpec:
    try:
        return ChartSpec(**data)
    except ValidationError as e:
        raise ValueError(f"Spec inválida: {e}")

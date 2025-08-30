# transform.py
# Transforma ChartSpec a Vega-Lite
from .spec import ChartSpec
from typing import Dict, Any

def chartspec_to_vegalite(spec: ChartSpec) -> Dict[str, Any]:
    # Ejemplo simple, expandir según necesidades
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "mark": spec.type,
        "data": {"values": spec.data},
        "encoding": spec.encoding,
        **spec.options
    }

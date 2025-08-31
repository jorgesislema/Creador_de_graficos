# exporter.py
# Exportador para Looker Studio
from ..base import IExporter
import json
from typing import Dict, Any
import uuid

class LookerStudioExporter(IExporter):
    def export(self, spec, output_path: str):
        """
        Exporta un ChartSpec a formato JSON de Looker Studio
        """
        studio_config = self._generate_studio_config(spec)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(studio_config, f, indent=2, ensure_ascii=False)
        
        return True
    
    def _generate_studio_config(self, spec) -> Dict[str, Any]:
        """
        Genera la configuración JSON para Looker Studio
        """
        chart_id = str(uuid.uuid4())
        
        config = {
            "version": "1.0",
            "type": "report",
            "id": chart_id,
            "name": "Generated Chart Report",
            "description": "Reporte generado automáticamente",
            "pages": [
                {
                    "id": f"page_{chart_id}",
                    "name": "Chart Page",
                    "elements": [
                        self._create_chart_element(spec, chart_id)
                    ]
                }
            ],
            "dataSources": [
                self._create_data_source(spec)
            ],
            "style": {
                "theme": "DEFAULT",
                "colorPalette": "DEFAULT"
            }
        }
        
        return config
    
    def _create_chart_element(self, spec, chart_id: str) -> Dict[str, Any]:
        """
        Crea el elemento de gráfico para Looker Studio
        """
        studio_chart_type = self._map_to_studio_chart_type(spec.type)
        
        element = {
            "id": f"chart_{chart_id}",
            "type": "CHART",
            "chartType": studio_chart_type,
            "position": {
                "x": 0,
                "y": 0,
                "width": 400,
                "height": 300
            },
            "dataMappings": self._create_data_mappings(spec),
            "style": self._create_chart_style(spec),
            "interactions": {
                "allowDrilldown": True,
                "allowFiltering": True
            }
        }
        
        return element
    
    def _create_data_source(self, spec) -> Dict[str, Any]:
        """
        Crea la fuente de datos para Looker Studio
        """
        data_source_id = str(uuid.uuid4())
        
        # Crear esquema basado en los datos
        schema = []
        if spec.data and len(spec.data) > 0:
            sample_row = spec.data[0]
            for field_name, field_value in sample_row.items():
                field_type = self._get_studio_field_type(field_value)
                schema.append({
                    "name": field_name,
                    "type": field_type,
                    "label": field_name.title(),
                    "description": f"Campo {field_name}"
                })
        
        data_source = {
            "id": data_source_id,
            "name": "Chart Data Source",
            "type": "CSV",
            "schema": schema,
            "data": spec.data
        }
        
        return data_source
    
    def _create_data_mappings(self, spec) -> Dict[str, Any]:
        """
        Crea los mapeos de datos basados en el encoding
        """
        mappings = {}
        
        if 'x' in spec.encoding:
            field_name = spec.encoding['x']['field']
            field_type = spec.encoding['x'].get('type', 'nominal')
            
            if field_type in ['nominal', 'ordinal']:
                mappings['dimensions'] = [{"field": field_name}]
            else:
                mappings['dateRanges'] = [{"field": field_name}]
        
        if 'y' in spec.encoding:
            field_name = spec.encoding['y']['field']
            mappings['metrics'] = [{"field": field_name, "aggregation": "SUM"}]
        
        if 'color' in spec.encoding:
            field_name = spec.encoding['color']['field']
            mappings['breakdowns'] = [{"field": field_name}]
        
        if 'size' in spec.encoding:
            field_name = spec.encoding['size']['field']
            if 'metrics' not in mappings:
                mappings['metrics'] = []
            mappings['metrics'].append({"field": field_name, "aggregation": "SUM"})
        
        return mappings
    
    def _create_chart_style(self, spec) -> Dict[str, Any]:
        """
        Crea el estilo del gráfico para Looker Studio
        """
        style = {
            "title": {
                "text": f"Gráfico {spec.type.title()}",
                "fontSize": 16,
                "fontFamily": "Roboto",
                "color": "#000000"
            },
            "backgroundColor": "#FFFFFF",
            "border": {
                "type": "SOLID",
                "color": "#E0E0E0",
                "width": 1
            }
        }
        
        # Estilos específicos por tipo de gráfico
        if spec.type in ['bar', 'stacked_bar']:
            style.update({
                "bars": {
                    "showValues": True,
                    "orientation": "VERTICAL"
                }
            })
        
        elif spec.type == 'line':
            style.update({
                "lines": {
                    "showPoints": True,
                    "lineWidth": 2,
                    "smooth": False
                }
            })
        
        elif spec.type in ['pie', 'donut']:
            style.update({
                "pie": {
                    "showValues": True,
                    "showLabels": True,
                    "innerRadius": 0.5 if spec.type == 'donut' else 0
                }
            })
        
        elif spec.type == 'scatter':
            style.update({
                "scatter": {
                    "pointSize": 5,
                    "showTrendLine": False
                }
            })
        
        elif spec.type == 'table':
            style.update({
                "table": {
                    "showHeader": True,
                    "showRowNumbers": True,
                    "alternatingRowColors": True
                }
            })
        
        return style
    
    def _map_to_studio_chart_type(self, chart_type: str) -> str:
        """
        Mapea tipos de gráficos a tipos de Looker Studio
        """
        mapping = {
            'bar': 'COLUMN',
            'stacked_bar': 'STACKED_COLUMN',
            'line': 'LINE',
            'area': 'AREA',
            'stacked_area': 'STACKED_AREA',
            'scatter': 'SCATTER',
            'bubble': 'BUBBLE',
            'pie': 'PIE',
            'donut': 'DONUT',
            'table': 'TABLE',
            'heatmap': 'HEATMAP',
            'histogram': 'HISTOGRAM',
            'boxplot': 'CANDLESTICK',  # Aproximación
            'treemap': 'TREEMAP',
            'gauge': 'GAUGE',
            'waterfall': 'WATERFALL'
        }
        
        return mapping.get(chart_type, 'COLUMN')
    
    def _get_studio_field_type(self, value) -> str:
        """
        Determina el tipo de campo de Looker Studio basado en el valor
        """
        if isinstance(value, bool):
            return 'BOOLEAN'
        elif isinstance(value, int):
            return 'NUMBER'
        elif isinstance(value, float):
            return 'NUMBER'
        elif isinstance(value, str):
            try:
                # Intentar parsear como fecha
                from datetime import datetime
                datetime.fromisoformat(value.replace('Z', '+00:00'))
                return 'DATE'
            except:
                return 'TEXT'
        else:
            return 'TEXT'

# exporter.py
# Exportador para Looker
from ..base import IExporter
import json
from typing import Dict, Any

class LookerExporter(IExporter):
    def export(self, spec, output_path: str):
        """
        Exporta un ChartSpec a formato LookML para Looker
        """
        lookml_content = self._generate_lookml_content(spec)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(lookml_content)
        
        return True
    
    def _generate_lookml_content(self, spec) -> str:
        """
        Genera el contenido LookML para Looker
        """
        chart_name = "generated_chart"
        
        # Generar vista (view)
        view_content = self._generate_view(spec, chart_name)
        
        # Generar modelo (model)
        model_content = self._generate_model(spec, chart_name)
        
        # Generar dashboard
        dashboard_content = self._generate_dashboard(spec, chart_name)
        
        # Combinar todo
        content = f"""# Archivo LookML generado automáticamente
# Vista de datos
{view_content}

# Modelo
{model_content}

# Dashboard
{dashboard_content}
"""
        
        return content
    
    def _generate_view(self, spec, chart_name: str) -> str:
        """
        Genera la vista LookML basada en los datos del spec
        """
        view_lines = [f"view: {chart_name}_view {{"]
        
        # Determinar tabla base (simulada)
        view_lines.append('  sql_table_name: public.chart_data ;;')
        view_lines.append('')
        
        # Generar dimensiones y medidas basadas en los datos
        if spec.data and len(spec.data) > 0:
            sample_row = spec.data[0]
            
            for field_name, field_value in sample_row.items():
                if isinstance(field_value, str):
                    # Dimensión categórica
                    view_lines.extend([
                        f'  dimension: {field_name} {{',
                        '    type: string',
                        f'    sql: ${{TABLE}}.{field_name} ;;',
                        '  }',
                        ''
                    ])
                elif isinstance(field_value, (int, float)):
                    # Dimensión numérica
                    view_lines.extend([
                        f'  dimension: {field_name} {{',
                        '    type: number',
                        f'    sql: ${{TABLE}}.{field_name} ;;',
                        '  }',
                        ''
                    ])
                    
                    # También crear medida de suma
                    view_lines.extend([
                        f'  measure: total_{field_name} {{',
                        '    type: sum',
                        f'    sql: ${{{field_name}}} ;;',
                        '  }',
                        ''
                    ])
        
        # Medida de conteo por defecto
        view_lines.extend([
            '  measure: count {',
            '    type: count',
            '    drill_fields: [*]',
            '  }'
        ])
        
        view_lines.append('}')
        
        return '\n'.join(view_lines)
    
    def _generate_model(self, spec, chart_name: str) -> str:
        """
        Genera el modelo LookML
        """
        model_lines = [
            f"connection: \"chart_database\"",
            f"include: \"{chart_name}_view.view.lkml\"",
            "",
            f"explore: {chart_name}_explore {{",
            f"  from: {chart_name}_view",
            f"  label: \"Chart Data Analysis\"",
            "}"
        ]
        
        return '\n'.join(model_lines)
    
    def _generate_dashboard(self, spec, chart_name: str) -> str:
        """
        Genera el dashboard LookML con la visualización
        """
        # Determinar tipo de visualización de Looker
        looker_vis_type = self._map_to_looker_vis_type(spec.type)
        
        dashboard_lines = [
            f"dashboard: {chart_name}_dashboard {{",
            f"  title: \"Generated Chart Dashboard\"",
            "  layout: newspaper",
            "",
            "  element: chart_element {",
            "    title: \"Chart Visualization\"",
            f"    type: looker_{looker_vis_type}",
            f"    explore: {chart_name}_explore",
            "    dimensions: [" + self._get_dimension_fields(spec) + "]",
            "    measures: [" + self._get_measure_fields(spec) + "]",
            self._generate_chart_settings(spec),
            "  }",
            "}"
        ]
        
        return '\n'.join(dashboard_lines)
    
    def _map_to_looker_vis_type(self, chart_type: str) -> str:
        """
        Mapea tipos de gráficos a tipos de visualización de Looker
        """
        mapping = {
            'bar': 'column',
            'stacked_bar': 'column',
            'line': 'line',
            'area': 'area',
            'scatter': 'scatter',
            'pie': 'pie',
            'donut': 'pie',
            'table': 'table',
            'heatmap': 'heatmap',
            'histogram': 'column',
            'boxplot': 'boxplot'
        }
        
        return mapping.get(chart_type, 'column')
    
    def _get_dimension_fields(self, spec) -> str:
        """
        Extrae campos de dimensión del encoding
        """
        dimensions = []
        
        if 'x' in spec.encoding and spec.encoding['x'].get('type') in ['nominal', 'ordinal']:
            field_name = spec.encoding['x']['field']
            dimensions.append(f"{spec.type}_view.{field_name}")
        
        if 'color' in spec.encoding:
            field_name = spec.encoding['color']['field']
            dimensions.append(f"{spec.type}_view.{field_name}")
        
        return ', '.join(dimensions) if dimensions else f"{spec.type}_view.count"
    
    def _get_measure_fields(self, spec) -> str:
        """
        Extrae campos de medida del encoding
        """
        measures = []
        
        if 'y' in spec.encoding and spec.encoding['y'].get('type') == 'quantitative':
            field_name = spec.encoding['y']['field']
            measures.append(f"{spec.type}_view.total_{field_name}")
        
        if 'size' in spec.encoding:
            field_name = spec.encoding['size']['field']
            measures.append(f"{spec.type}_view.total_{field_name}")
        
        return ', '.join(measures) if measures else f"{spec.type}_view.count"
    
    def _generate_chart_settings(self, spec) -> str:
        """
        Genera configuraciones específicas del gráfico
        """
        settings = []
        
        if spec.type in ['pie', 'donut']:
            settings.append('    show_value_labels: true')
            
        if spec.type == 'donut':
            settings.append('    inner_radius: 50')
        
        if spec.type in ['bar', 'column']:
            settings.append('    show_totals: true')
            settings.append('    show_row_totals: true')
        
        if spec.type == 'line':
            settings.append('    interpolation: linear')
            settings.append('    point_style: circle')
        
        # Configuraciones generales
        settings.extend([
            '    show_view_names: false',
            '    show_row_numbers: true',
            '    transpose: false',
            '    truncate_text: true',
            '    hide_totals: false',
            '    hide_row_totals: false',
            '    size_to_fit: true'
        ])
        
        return '\n'.join(settings)

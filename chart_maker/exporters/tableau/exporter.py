# exporter.py
# Exportador para Tableau
from ..base import IExporter
import xml.etree.ElementTree as ET
import json
from typing import Dict, Any
import os

class TableauExporter(IExporter):
    def export(self, spec, output_path: str):
        """
        Exporta un ChartSpec a formato TWB de Tableau
        """
        twb_content = self._generate_twb_content(spec)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(twb_content)
        
        return True
    
    def _generate_twb_content(self, spec) -> str:
        """
        Genera el contenido TWB (XML) para Tableau
        """
        # Crear el workbook root
        workbook = ET.Element('workbook')
        workbook.set('version', '18.1')
        workbook.set('source-build', '20221.21.1213.1449')
        
        # Preferences
        preferences = ET.SubElement(workbook, 'preferences')
        
        # Datasources
        datasources = ET.SubElement(workbook, 'datasources')
        datasource = self._create_datasource(datasources, spec)
        
        # Worksheets
        worksheets = ET.SubElement(workbook, 'worksheets')
        worksheet = self._create_worksheet(worksheets, spec, datasource)
        
        # Windows
        windows = ET.SubElement(workbook, 'windows')
        self._create_window(windows, worksheet)
        
        # Convertir a string con formato XML
        ET.indent(workbook, space="  ", level=0)
        xml_str = ET.tostring(workbook, encoding='unicode')
        
        # Agregar declaración XML
        return '<?xml version="1.0" encoding="utf-8"?>\n' + xml_str
    
    def _create_datasource(self, parent, spec) -> ET.Element:
        """
        Crea el elemento datasource con los datos del spec
        """
        datasource = ET.SubElement(parent, 'datasource')
        datasource.set('caption', 'Chart Data')
        datasource.set('name', 'federated.0rhj4jg1kzm3yq1bek2m91kx91b4')
        datasource.set('version', '18.1')
        
        # Connection
        connection = ET.SubElement(datasource, 'connection')
        connection.set('class', 'federated')
        
        # Named-connections
        named_connections = ET.SubElement(connection, 'named-connections')
        named_connection = ET.SubElement(named_connections, 'named-connection')
        named_connection.set('caption', 'Chart Data')
        named_connection.set('name', 'textscan.1234567890')
        
        text_connection = ET.SubElement(named_connection, 'connection')
        text_connection.set('class', 'textscan')
        text_connection.set('directory', os.path.dirname(os.path.abspath('.')))
        text_connection.set('filename', 'chart_data.csv')
        text_connection.set('password', '')
        text_connection.set('server', '')
        
        # Columns
        columns = ET.SubElement(datasource, 'columns')
        
        # Crear columnas basadas en los datos
        if spec.data and len(spec.data) > 0:
            sample_row = spec.data[0]
            for field_name, field_value in sample_row.items():
                column = ET.SubElement(columns, 'column')
                column.set('datatype', self._get_tableau_datatype(field_value))
                column.set('name', f'[{field_name}]')
                column.set('ordinal', str(len(columns)))
        
        return datasource
    
    def _create_worksheet(self, parent, spec, datasource) -> ET.Element:
        """
        Crea la hoja de trabajo con la visualización
        """
        worksheet = ET.SubElement(parent, 'worksheet')
        worksheet.set('name', 'Chart')
        
        # Table
        table = ET.SubElement(worksheet, 'table')
        table.set('name', 'Worksheet')
        table.set('type', 'worksheet')
        
        # View
        view = ET.SubElement(table, 'view')
        view.set('type', 'worksheet')
        
        # Datasources
        datasources = ET.SubElement(view, 'datasources')
        datasource_ref = ET.SubElement(datasources, 'datasource')
        datasource_ref.set('caption', 'Chart Data')
        datasource_ref.set('name', 'federated.0rhj4jg1kzm3yq1bek2m91kx91b4')
        
        # Datasource-dependencies
        deps = ET.SubElement(view, 'datasource-dependencies')
        deps.set('datasource', 'federated.0rhj4jg1kzm3yq1bek2m91kx91b4')
        
        # Agregar columnas como dependencias
        if spec.data and len(spec.data) > 0:
            sample_row = spec.data[0]
            for field_name in sample_row.keys():
                column_dep = ET.SubElement(deps, 'column')
                column_dep.set('datatype', self._get_tableau_datatype(sample_row[field_name]))
                column_dep.set('name', f'[{field_name}]')
                column_dep.set('role', 'dimension' if isinstance(sample_row[field_name], str) else 'measure')
                column_dep.set('type', 'nominal' if isinstance(sample_row[field_name], str) else 'quantitative')
        
        # Shelves y encoding
        shelves = ET.SubElement(view, 'shelves')
        self._add_shelves_from_encoding(shelves, spec.encoding)
        
        return worksheet
    
    def _create_window(self, parent, worksheet):
        """
        Crea la ventana principal
        """
        window = ET.SubElement(parent, 'window')
        window.set('class', 'worksheet')
        window.set('name', 'Chart')
        
        cards = ET.SubElement(window, 'cards')
        edge = ET.SubElement(cards, 'edge')
        edge.set('name', 'left')
        
        strip = ET.SubElement(edge, 'strip')
        strip.set('size', '160')
        
        card = ET.SubElement(strip, 'card')
        card.set('type', 'pages')
        
        edge_top = ET.SubElement(cards, 'edge')
        edge_top.set('name', 'top')
        
        strip_top = ET.SubElement(edge_top, 'strip')
        strip_top.set('size', '2147483647')
        
        card_top = ET.SubElement(strip_top, 'card')
        card_top.set('type', 'columns')
        
        card_top2 = ET.SubElement(strip_top, 'card')
        card_top2.set('type', 'rows')
        
    def _add_shelves_from_encoding(self, parent, encoding: Dict):
        """
        Agrega shelves basados en el encoding del gráfico
        """
        if 'x' in encoding:
            shelf = ET.SubElement(parent, 'shelf')
            shelf.set('name', 'columns')
            field_ref = ET.SubElement(shelf, 'field')
            field_ref.set('name', f'[{encoding["x"]["field"]}]')
        
        if 'y' in encoding:
            shelf = ET.SubElement(parent, 'shelf')
            shelf.set('name', 'rows')
            field_ref = ET.SubElement(shelf, 'field')
            field_ref.set('name', f'[{encoding["y"]["field"]}]')
        
        if 'color' in encoding:
            shelf = ET.SubElement(parent, 'shelf')
            shelf.set('name', 'color')
            field_ref = ET.SubElement(shelf, 'field')
            field_ref.set('name', f'[{encoding["color"]["field"]}]')
        
        if 'size' in encoding:
            shelf = ET.SubElement(parent, 'shelf')
            shelf.set('name', 'size')
            field_ref = ET.SubElement(shelf, 'field')
            field_ref.set('name', f'[{encoding["size"]["field"]}]')
    
    def _get_tableau_datatype(self, value) -> str:
        """
        Determina el tipo de dato de Tableau basado en el valor
        """
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            return 'real'
        elif isinstance(value, str):
            try:
                # Intentar parsear como fecha
                from datetime import datetime
                datetime.fromisoformat(value.replace('Z', '+00:00'))
                return 'date'
            except:
                return 'string'
        else:
            return 'string'

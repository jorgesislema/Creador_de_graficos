# exporter.py
# Exportador para archivos .twb/.twbx de Tableau
from ..base import IExporter
import json
import xml.etree.ElementTree as ET
import zipfile
import os
from datetime import datetime

class TableauExporter(IExporter):
    def export(self, spec, output_path: str):
        """Genera un archivo .twb o .twbx para Tableau con la especificación del gráfico"""
        try:
            # Extraer información del spec
            spec_dict = getattr(spec, 'dict', lambda: spec)() if hasattr(spec, 'dict') else spec
            chart_type = spec_dict.get('type', 'barras_vertical')
            title = spec_dict.get('title', 'Gráfico Sin Título')
            description = spec_dict.get('description', 'Gráfico creado con Creador de Gráficos')
            width = spec_dict.get('width', 800)
            height = spec_dict.get('height', 600)
            
            # Mapeo de tipos de gráfico a Tableau
            tableau_chart_types = {
                'barras_vertical': 'bar',
                'bar_chart_vertical': 'bar',
                'barras_horizontal': 'horizontal-bar',
                'bar_chart_horizontal': 'horizontal-bar',
                'columnas': 'bar',
                'column_chart': 'bar',
                'lineas': 'line',
                'line_chart': 'line',
                'area': 'area',
                'area_chart': 'area',
                'circular': 'pie',
                'pie_chart': 'pie',
                'dispersion': 'scatter',
                'scatter_plot': 'scatter',
                'mapa_calor': 'heatmap',
                'heatmap': 'heatmap'
            }
            
            tableau_type = tableau_chart_types.get(chart_type, 'bar')
            
            # Crear XML para Tableau Workbook (.twb)
            workbook = ET.Element('workbook')
            workbook.set('source-build', '2023.1.0 (20223.23.0213.2227)')
            workbook.set('source-platform', 'win')
            workbook.set('version', '18.1')
            
            # Metadata del documento
            document_format = ET.SubElement(workbook, 'document-format-change-manifest')
            ET.SubElement(document_format, 'SheetIdentifierTracking', enabled='true')
            ET.SubElement(document_format, 'WindowsPersistSimpleIdentifiers')
            
            # Sección de propiedades del repositorio
            repository_location = ET.SubElement(workbook, 'repository-location')
            repository_location.set('id', 'localRepositoryLocation')
            repository_location.set('path', os.path.basename(output_path))
            repository_location.set('revision', '1.0')
            
            # Datasource - estructura básica para datos de ejemplo
            datasources = ET.SubElement(workbook, 'datasources')
            datasource = ET.SubElement(datasources, 'datasource')
            datasource.set('caption', 'Datos del Gráfico')
            datasource.set('inline', 'true')
            datasource.set('name', 'federated.datasource')
            datasource.set('version', '18.1')
            
            # Conexión de datos
            connection = ET.SubElement(datasource, 'connection')
            connection.set('class', 'federated')
            
            named_connections = ET.SubElement(connection, 'named-connections')
            named_connection = ET.SubElement(named_connections, 'named-connection')
            named_connection.set('caption', 'DatosEjemplo')
            named_connection.set('name', 'excel-direct.datos_ejemplo')
            
            # Datos de ejemplo incrustados
            connection_data = ET.SubElement(named_connection, 'connection')
            connection_data.set('class', 'excel-direct')
            connection_data.set('cleaning', 'no')
            connection_data.set('compat', 'no')
            connection_data.set('dataRefreshTime', '')
            connection_data.set('filename', 'datos_ejemplo.xlsx')
            connection_data.set('interpretationMode', '0')
            connection_data.set('password', '')
            connection_data.set('server', '')
            connection_data.set('validate', 'no')
            
            # Columnas de datos
            cols = ET.SubElement(datasource, 'cols')
            
            # Columna categoría
            col_cat = ET.SubElement(cols, 'column')
            col_cat.set('datatype', 'string')
            col_cat.set('name', '[Categoría]')
            col_cat.set('role', 'dimension')
            col_cat.set('semantic-role', '[Category]')
            col_cat.set('type', 'nominal')
            
            # Columna valor
            col_val = ET.SubElement(cols, 'column')
            col_val.set('datatype', 'integer')
            col_val.set('name', '[Valor]')
            col_val.set('role', 'measure')
            col_val.set('type', 'quantitative')
            
            # Worksheets (hojas de trabajo)
            worksheets = ET.SubElement(workbook, 'worksheets')
            worksheet = ET.SubElement(worksheets, 'worksheet')
            worksheet.set('name', f'{title}')
            
            # Layout de la hoja
            layout = ET.SubElement(worksheet, 'layout')
            layout.set('dim-ordering', 'alphabetic')
            layout.set('dim-percentage', '0.5')
            layout.set('measure-ordering', 'alphabetic')
            layout.set('measure-percentage', '0.4')
            layout.set('show-structure', 'true')
            
            # Vista de la hoja
            view = ET.SubElement(worksheet, 'table')
            view.set('name', f'[{title}]')
            view.set('type', 'view')
            
            # Configuración de la vista según el tipo de gráfico
            view_config = ET.SubElement(view, 'view')
            view_config.set('name', f'[{title}]')
            
            # Panes (paneles)
            panes = ET.SubElement(view, 'panes')
            pane = ET.SubElement(panes, 'pane')
            pane.set('selection-relaxation-option', 'selection-relaxation-allow')
            
            # Configuración de marcas según el tipo de gráfico
            marks = ET.SubElement(pane, 'marks')
            marks.set('class', tableau_type)
            
            # Codificaciones (encoding)
            encodings = ET.SubElement(marks, 'encodings')
            
            # Eje X
            x_encoding = ET.SubElement(encodings, 'text')
            x_encoding.set('column', '[Categoría]')
            
            # Eje Y  
            y_encoding = ET.SubElement(encodings, 'text')
            y_encoding.set('column', '[Valor]')
            
            # Estilo de marcas
            style = ET.SubElement(marks, 'style')
            
            format_elem = ET.SubElement(style, 'format')
            format_elem.set('attr', 'size')
            format_elem.set('value', '10')
            
            # Dashboards
            dashboards = ET.SubElement(workbook, 'dashboards')
            dashboard = ET.SubElement(dashboards, 'dashboard')
            dashboard.set('name', f'Dashboard - {title}')
            
            # Tamaño del dashboard
            size = ET.SubElement(dashboard, 'size')
            size.set('maxheight', str(height))
            size.set('maxwidth', str(width))
            size.set('minheight', str(height))
            size.set('minwidth', str(width))
            
            # Objetos del dashboard
            zones = ET.SubElement(dashboard, 'zones')
            zone = ET.SubElement(zones, 'zone')
            zone.set('h', str(height))
            zone.set('id', '3')
            zone.set('type', 'layout-flow')
            zone.set('w', str(width))
            zone.set('x', '0')
            zone.set('y', '0')
            
            # Windows (ventanas)
            windows = ET.SubElement(workbook, 'windows')
            window = ET.SubElement(windows, 'window')
            window.set('class', 'worksheet')
            window.set('name', f'{title}')
            
            # Cards (tarjetas de información)
            cards = ET.SubElement(window, 'cards')
            
            # Card para información del gráfico
            card = ET.SubElement(cards, 'edge')
            card.set('name', 'left')
            
            info_strip = ET.SubElement(card, 'strip')
            info_strip.set('size', '160')
            
            # Información adicional en comentarios XML
            comment_info = f"""
Gráfico generado por Creador de Gráficos
Tipo: {chart_type}
Título: {title}
Descripción: {description}
Especificación completa: {json.dumps(spec_dict, indent=2)}
"""
            
            workbook.append(ET.Comment(comment_info))
            
            # Escribir el archivo .twb
            tree = ET.ElementTree(workbook)
            ET.indent(tree, space="  ", level=0)
            
            # Determinar si crear .twb o .twbx
            if output_path.endswith('.twbx'):
                # Crear archivo .twbx (es un ZIP con el .twb y datos)
                temp_dir = os.path.join(os.path.dirname(output_path), 'temp_twbx')
                os.makedirs(temp_dir, exist_ok=True)
                
                # Guardar el .twb en el directorio temporal
                twb_path = os.path.join(temp_dir, 'workbook.twb')
                tree.write(twb_path, encoding='utf-8', xml_declaration=True)
                
                # Crear datos de ejemplo
                data_dir = os.path.join(temp_dir, 'Data')
                os.makedirs(data_dir, exist_ok=True)
                
                # Crear archivo de datos de ejemplo (CSV)
                data_csv = os.path.join(data_dir, 'datos_ejemplo.csv')
                with open(data_csv, 'w', encoding='utf-8') as f:
                    f.write('Categoría,Valor\\n')
                    f.write('A,23\\n')
                    f.write('B,45\\n') 
                    f.write('C,56\\n')
                    f.write('D,78\\n')
                    f.write('E,32\\n')
                
                # Crear el archivo .twbx
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arc_name = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arc_name)
                
                # Limpiar directorio temporal
                import shutil
                shutil.rmtree(temp_dir)
            else:
                # Crear archivo .twb simple
                tree.write(output_path, encoding='utf-8', xml_declaration=True)
            
            return True
            
        except Exception as e:
            print(f"Error creando archivo Tableau: {e}")
            return False

# Función de exportación
def export_to_tableau(spec, output_path: str):
    """Función wrapper para exportar a Tableau"""
    exporter = TableauExporter()
    return exporter.export(spec, output_path)
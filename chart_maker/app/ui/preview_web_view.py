"""
Componente de vista previa simplificada que muestra información del gráfico
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import json
from typing import Dict, Any, Optional


class PreviewWebView(QWidget):
    """Widget de vista previa simplificada que muestra información del gráfico"""
    
    def __init__(self):
        super().__init__()
        self.current_spec = None
        self.init_ui()
        
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout()
        
        # Encabezado
        header_layout = QHBoxLayout()
        header_label = QLabel("Vista Previa del Gráfico")
        header_label.setFont(QFont("Arial", 14, QFont.Bold))
        header_layout.addWidget(header_label)
        
        # Botón para abrir en navegador
        self.open_browser_btn = QPushButton("Abrir en Navegador")
        self.open_browser_btn.clicked.connect(self.open_in_browser)
        self.open_browser_btn.setEnabled(False)
        header_layout.addWidget(self.open_browser_btn)
        
        layout.addLayout(header_layout)
        
        # Vista de texto para mostrar información del gráfico
        self.text_browser = QTextBrowser()
        self.text_browser.setFont(QFont("Courier", 10))
        layout.addWidget(self.text_browser)
        
        self.setLayout(layout)
        
        # Cargar contenido inicial
        self.load_initial_content()
    
    def load_initial_content(self):
        """Carga el contenido inicial"""
        initial_html = """
        <html>
        <head>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    padding: 20px; 
                    background-color: #f8f9fa;
                }
                .welcome {
                    background-color: #e3f2fd;
                    border: 1px solid #2196f3;
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    margin-bottom: 20px;
                }
                .info {
                    background-color: #fff;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 15px;
                }
                .feature {
                    margin: 10px 0;
                    padding: 8px;
                    background-color: #f5f5f5;
                    border-left: 4px solid #4caf50;
                }
            </style>
        </head>
        <body>
            <div class="welcome">
                <h2>¡Bienvenido al Creador de Gráficos!</h2>
                <p>Utiliza los controles de la izquierda para crear tu gráfico personalizado.</p>
            </div>
            
            <div class="info">
                <h3>Características disponibles:</h3>
                <div class="feature">📊 Más de 40 tipos de gráficos diferentes</div>
                <div class="feature">🎨 Múltiples temas y esquemas de colores</div>
                <div class="feature">📁 Importación de datos JSON y CSV</div>
                <div class="feature">💾 Exportación a HTML, JSON y otros formatos</div>
                <div class="feature">🔧 Personalización completa de dimensiones y estilos</div>
            </div>
            
            <div class="info">
                <h3>Instrucciones:</h3>
                <ol>
                    <li>Selecciona un tipo de gráfico en la pestaña "Básico"</li>
                    <li>Configura tus datos en la pestaña "Datos"</li>
                    <li>Personaliza colores y temas en la pestaña "Estilo"</li>
                    <li>Haz clic en "Actualizar Vista Previa" para ver los cambios</li>
                    <li>Exporta tu gráfico cuando esté listo</li>
                </ol>
            </div>
        </body>
        </html>
        """
        self.text_browser.setHtml(initial_html)
    
    def update_chart(self, spec: Dict[str, Any]):
        """
        Actualiza la vista previa con una nueva especificación
        
        Args:
            spec: Especificación del gráfico en formato Vega-Lite
        """
        try:
            self.current_spec = spec
            self.open_browser_btn.setEnabled(True)
            
            # Generar vista previa HTML
            preview_html = self.generate_preview_html(spec)
            self.text_browser.setHtml(preview_html)
            
        except Exception as e:
            self.show_error(str(e))
    
    def generate_preview_html(self, spec: Dict[str, Any]) -> str:
        """
        Genera HTML para mostrar información del gráfico
        
        Args:
            spec: Especificación del gráfico
            
        Returns:
            HTML con la información del gráfico
        """
        try:
            # Extraer información clave
            chart_type = spec.get("mark", "No especificado")
            title = spec.get("title", "Sin título")
            description = spec.get("description", "Sin descripción")
            width = spec.get("width", "Auto")
            height = spec.get("height", "Auto")
            
            # Contar datos
            data_info = "No hay datos"
            if "data" in spec:
                if "values" in spec["data"]:
                    data_count = len(spec["data"]["values"])
                    data_info = f"{data_count} registros"
                elif "url" in spec["data"]:
                    data_info = f"Datos externos: {spec['data']['url']}"
            
            # Información de encoding
            encoding_info = "No especificado"
            if "encoding" in spec:
                fields = []
                for channel, field_def in spec["encoding"].items():
                    if isinstance(field_def, dict) and "field" in field_def:
                        fields.append(f"{channel}: {field_def['field']}")
                if fields:
                    encoding_info = ", ".join(fields)
            
            # Generar JSON formateado
            spec_json = json.dumps(spec, indent=2, ensure_ascii=False)
            
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ 
                        font-family: Arial, sans-serif; 
                        padding: 20px; 
                        background-color: #f8f9fa;
                        line-height: 1.6;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 20px;
                        border-radius: 10px;
                        text-align: center;
                        margin-bottom: 20px;
                    }}
                    .info-grid {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 15px;
                        margin-bottom: 20px;
                    }}
                    .info-card {{
                        background-color: white;
                        border: 1px solid #e0e0e0;
                        border-radius: 8px;
                        padding: 15px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .info-label {{
                        font-weight: bold;
                        color: #333;
                        margin-bottom: 5px;
                    }}
                    .info-value {{
                        color: #666;
                        font-size: 14px;
                    }}
                    .spec-container {{
                        background-color: white;
                        border: 1px solid #e0e0e0;
                        border-radius: 8px;
                        padding: 15px;
                        margin-top: 20px;
                    }}
                    .spec-json {{
                        background-color: #f8f8f8;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        padding: 10px;
                        font-family: 'Courier New', monospace;
                        font-size: 12px;
                        overflow-x: auto;
                        max-height: 300px;
                        overflow-y: auto;
                    }}
                    .chart-type {{
                        display: inline-block;
                        background-color: #4caf50;
                        color: white;
                        padding: 4px 12px;
                        border-radius: 20px;
                        font-size: 12px;
                        font-weight: bold;
                    }}
                    .note {{
                        background-color: #fff3cd;
                        border: 1px solid #ffeaa7;
                        border-radius: 4px;
                        padding: 10px;
                        margin-top: 15px;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>📊 Vista Previa del Gráfico</h2>
                    <span class="chart-type">{chart_type.upper()}</span>
                </div>
                
                <div class="info-grid">
                    <div class="info-card">
                        <div class="info-label">📝 Título</div>
                        <div class="info-value">{title}</div>
                    </div>
                    
                    <div class="info-card">
                        <div class="info-label">📄 Descripción</div>
                        <div class="info-value">{description}</div>
                    </div>
                    
                    <div class="info-card">
                        <div class="info-label">📏 Dimensiones</div>
                        <div class="info-value">{width} × {height}</div>
                    </div>
                    
                    <div class="info-card">
                        <div class="info-label">📊 Datos</div>
                        <div class="info-value">{data_info}</div>
                    </div>
                    
                    <div class="info-card">
                        <div class="info-label">🎯 Codificación</div>
                        <div class="info-value">{encoding_info}</div>
                    </div>
                    
                    <div class="info-card">
                        <div class="info-label">🎨 Tipo de Gráfico</div>
                        <div class="info-value">{chart_type}</div>
                    </div>
                </div>
                
                <div class="note">
                    <strong>💡 Sugerencia:</strong> Haz clic en "Abrir en Navegador" para ver el gráfico interactivo completo con Vega-Lite.
                </div>
                
                <div class="spec-container">
                    <h3>🔧 Especificación Vega-Lite</h3>
                    <div class="spec-json">{spec_json}</div>
                </div>
            </body>
            </html>
            """
            
            return html_content
            
        except Exception as e:
            return self.get_error_html(f"Error al generar vista previa: {e}")
    
    def get_error_html(self, error_message: str) -> str:
        """Genera HTML para mostrar errores"""
        return f"""
        <html>
        <head>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    padding: 20px; 
                    background-color: #ffebee;
                }}
                .error-container {{
                    background-color: #f44336;
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                }}
                .error-details {{
                    background-color: white;
                    color: #d32f2f;
                    padding: 15px;
                    border-radius: 4px;
                    margin-top: 15px;
                    font-family: monospace;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <h2>❌ Error en la Vista Previa</h2>
                <div class="error-details">{error_message}</div>
            </div>
        </body>
        </html>
        """
    
    def show_error(self, error_message: str):
        """
        Muestra un mensaje de error en la vista previa
        
        Args:
            error_message: Mensaje de error a mostrar
        """
        error_html = self.get_error_html(error_message)
        self.text_browser.setHtml(error_html)
        self.open_browser_btn.setEnabled(False)
    
    def clear_preview(self):
        """Limpia la vista previa"""
        self.load_initial_content()
        self.current_spec = None
        self.open_browser_btn.setEnabled(False)
    
    def open_in_browser(self):
        """Abre el gráfico en el navegador web"""
        if not self.current_spec:
            return
            
        try:
            import tempfile
            import webbrowser
            import os
            
            # Generar HTML completo con Vega-Lite
            html_content = self.get_vega_template(self.current_spec)
            
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_file = f.name
            
            # Abrir en navegador
            webbrowser.open(f'file://{temp_file}')
            
        except Exception as e:
            print(f"Error al abrir en navegador: {e}")
    
    def get_vega_template(self, spec: Optional[Dict[str, Any]] = None) -> str:
        """
        Genera el template HTML completo con Vega-Lite para navegador
        
        Args:
            spec: Especificación del gráfico en formato Vega-Lite
            
        Returns:
            HTML con el gráfico embebido y funcional
        """
        default_spec = {
            "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
            "description": "Gráfico de ejemplo",
            "data": {
                "values": [
                    {"category": "A", "value": 28},
                    {"category": "B", "value": 55},
                    {"category": "C", "value": 43},
                    {"category": "D", "value": 91},
                    {"category": "E", "value": 81}
                ]
            },
            "mark": "bar",
            "encoding": {
                "x": {"field": "category", "type": "nominal"},
                "y": {"field": "value", "type": "quantitative"}
            },
            "width": 400,
            "height": 300
        }
        
        vega_spec = spec if spec else default_spec
        
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Gráfico - Creador de Gráficos</title>
    <script src="https://cdn.jsdelivr.net/npm/vega@6"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@6"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@7"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        
        .header {{
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 300;
        }}
        
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 16px;
        }}
        
        .chart-container {{
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            padding: 30px;
            margin: 20px;
            min-width: 600px;
        }}
        
        #vis {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .error-message {{
            color: #d32f2f;
            background-color: #ffebee;
            border: 1px solid #e57373;
            border-radius: 8px;
            padding: 20px;
            margin: 20px;
            font-family: monospace;
            text-align: center;
        }}
        
        .actions {{
            margin-top: 20px;
            text-align: center;
        }}
        
        .actions button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            margin: 0 5px;
            transition: transform 0.2s;
        }}
        
        .actions button:hover {{
            transform: translateY(-2px);
        }}
        
        .spec-info {{
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            font-size: 14px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Creador de Gráficos</h1>
        <p>Gráfico generado con Vega-Lite</p>
    </div>
    
    <div class="chart-container">
        <div id="vis"></div>
        
        <div class="spec-info">
            <strong>Tipo:</strong> {vega_spec.get('mark', 'No especificado')} |
            <strong>Datos:</strong> {len(vega_spec.get('data', {}).get('values', [])) if vega_spec.get('data', {}).get('values') else 'Externos'} registros |
            <strong>Dimensiones:</strong> {vega_spec.get('width', 'Auto')} × {vega_spec.get('height', 'Auto')}
        </div>
        
        <div class="actions">
            <button onclick="downloadSVG()">💾 Descargar SVG</button>
            <button onclick="downloadPNG()">🖼️ Descargar PNG</button>
            <button onclick="copySpec()">📋 Copiar Especificación</button>
        </div>
    </div>
    
    <script type="text/javascript">
        const spec = {json.dumps(vega_spec, indent=2)};
        let vegaView;
        
        function renderChart() {{
            vegaEmbed('#vis', spec, {{
                theme: 'quartz',
                renderer: 'svg',
                actions: {{
                    export: true,
                    source: false,
                    compiled: false,
                    editor: false
                }}
            }}).then(result => {{
                vegaView = result.view;
                console.log('Gráfico renderizado exitosamente');
            }}).catch(error => {{
                console.error('Error al renderizar el gráfico:', error);
                document.getElementById('vis').innerHTML = 
                    '<div class="error-message">❌ Error al renderizar el gráfico: ' + error.message + '</div>';
            }});
        }}
        
        function downloadSVG() {{
            if (vegaView) {{
                vegaView.toSVG().then(svg => {{
                    const blob = new Blob([svg], {{type: 'image/svg+xml'}});
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'chart.svg';
                    a.click();
                    URL.revokeObjectURL(url);
                }});
            }}
        }}
        
        function downloadPNG() {{
            if (vegaView) {{
                vegaView.toImageURL('png', 2).then(url => {{
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'chart.png';
                    a.click();
                }});
            }}
        }}
        
        function copySpec() {{
            navigator.clipboard.writeText(JSON.stringify(spec, null, 2)).then(() => {{
                alert('📋 Especificación copiada al portapapeles');
            }});
        }}
        
        // Renderizar cuando la página esté lista
        document.addEventListener('DOMContentLoaded', renderChart);
    </script>
</body>
</html>
        """
        
        return html_template

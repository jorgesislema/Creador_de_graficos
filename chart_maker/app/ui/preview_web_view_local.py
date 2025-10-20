"""
Componente de vista previa local sin dependencias externas
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import json
from typing import Dict, Any, Optional


class PreviewWebView(QWidget):
    """Widget de vista previa local que muestra información del gráfico sin dependencias externas"""
    
    def __init__(self):
        super().__init__()
        self.current_spec = None
        self.init_ui()
        
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout()
        
        # Encabezado
        header_layout = QHBoxLayout()
        header_label = QLabel("Vista Previa Local")
        header_label.setFont(QFont("Arial", 14, QFont.Bold))
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
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
                <h2>🎨 Creador de Gráficos Local</h2>
                <p>Genera objetos visuales para Power BI (.pbiviz) y Tableau (.twb/.twbx) completamente offline</p>
            </div>
            
            <div class="info">
                <h3>Características disponibles:</h3>
                <div class="feature">📊 Más de 50 tipos de gráficos en español e inglés</div>
                <div class="feature">🎨 Sin dependencias de internet - 100% local</div>
                <div class="feature">📁 Importación de datos JSON y CSV</div>
                <div class="feature">💾 Exportación directa a .pbiviz y .twb/.twbx</div>
                <div class="feature">🔧 Personalización completa de dimensiones y estilos</div>
            </div>
            
            <div class="info">
                <h3>Instrucciones:</h3>
                <ol>
                    <li>Selecciona un tipo de gráfico (español o inglés)</li>
                    <li>Configura tus datos en la pestaña "Datos"</li>
                    <li>Personaliza colores y temas en la pestaña "Estilo"</li>
                    <li>Exporta directamente a Power BI o Tableau</li>
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
            
            # Generar vista previa HTML
            preview_html = self.generate_preview_html(spec)
            self.text_browser.setHtml(preview_html)
            
        except Exception as e:
            self.show_error(str(e))
    
    def generate_preview_html(self, spec: Dict[str, Any]) -> str:
        """
        Genera HTML local para mostrar información del gráfico
        
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
                    .local-note {{
                        background-color: #e8f5e8;
                        border: 1px solid #4caf50;
                        border-radius: 4px;
                        padding: 10px;
                        margin-top: 15px;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h2>📊 Vista Previa Local</h2>
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
                
                <div class="local-note">
                    <strong>🔒 Modo Local:</strong> Esta aplicación funciona completamente sin conexión a internet. 
                    Exporta directamente a Power BI (.pbiviz) y Tableau (.twb/.twbx) para usar con tus datos.
                </div>
                
                <div class="spec-container">
                    <h3>🔧 Especificación del Gráfico</h3>
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
    
    def clear_preview(self):
        """Limpia la vista previa"""
        self.load_initial_content()
        self.current_spec = None
    
    def get_chart_summary(self, spec: Optional[Dict[str, Any]] = None) -> str:
        """
        Genera un resumen del gráfico para exportación local
        
        Args:
            spec: Especificación del gráfico
            
        Returns:
            Resumen de texto del gráfico
        """
        if not spec:
            spec = self.current_spec
            
        if not spec:
            return "No hay especificación de gráfico disponible"
            
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
        
        summary = f"""
        Título: {title}
        Descripción: {description}
        Tipo: {chart_type}
        Dimensiones: {width} × {height}
        Datos: {data_info}
        """
        
        return summary.strip()
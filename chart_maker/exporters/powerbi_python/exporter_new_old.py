# exporter_new.py
# Exportador corregido para archivos .pbiviz de Power BI
from ..base import IExporter
import json
import zipfile
import os
import base64
from datetime import datetime
import uuid

class PowerBIPythonExporter(IExporter):
    def export(self, spec, output_path: str):
        """Genera un archivo .pbiviz válido para Power BI con la especificación del gráfico"""
        try:
            # Extraer información del spec
            spec_dict = getattr(spec, 'dict', lambda: spec)() if hasattr(spec, 'dict') else spec
            chart_type = spec_dict.get('type', 'barras_vertical')
            title = spec_dict.get('title', 'Gráfico Sin Título')
            description = spec_dict.get('description', 'Gráfico creado con Creador de Gráficos')
            
            # Crear estructura .pbiviz (es un archivo ZIP con estructura específica)
            temp_dir = os.path.join(os.path.dirname(output_path), 'temp_pbiviz')
            os.makedirs(temp_dir, exist_ok=True)
            
            # 1. pbiviz.json - metadata del visual (formato correcto)
            visual_guid = str(uuid.uuid4()).upper().replace('-', '')
            pbiviz_config = {
                "visual": {
                    "name": f"CreadorGraficos{chart_type.replace('_', '')}",
                    "displayName": title[:50],  # Power BI limita a 50 caracteres
                    "guid": f"CreadorGraficos{visual_guid[:15]}",
                    "visualClassName": "Visual",
                    "version": "1.0.0.0",
                    "description": description[:200],  # Power BI limita a 200 caracteres
                    "supportUrl": "https://github.com/jorgesislema/Creador_de_graficos",
                    "gitHubUrl": "https://github.com/jorgesislema/Creador_de_graficos"
                },
                "apiVersion": "4.6.0",
                "author": {
                    "name": "Creador de Gráficos",
                    "email": "support@ejemplo.com"
                },
                "assets": {
                    "icon": "assets/icon.png"
                },
                "style": "style/visual.less",
                "capabilities": "capabilities.json",
                "stringResources": []
            }
            
            with open(os.path.join(temp_dir, 'pbiviz.json'), 'w', encoding='utf-8') as f:
                json.dump(pbiviz_config, f, indent=2, ensure_ascii=False)
            
            # 2. capabilities.json - define qué datos puede recibir el visual (versión corregida)
            capabilities = {
                "privileges": [],  # Requerido desde API 4.6.0
                "dataRoles": [
                    {
                        "displayName": "Category",
                        "name": "category",
                        "kind": "Grouping",
                        "description": "Data to be grouped"
                    },
                    {
                        "displayName": "Values",
                        "name": "values",
                        "kind": "Measure",
                        "description": "Data values"
                    }
                ],
                "dataViewMappings": [
                    {
                        "conditions": [
                            {
                                "category": {"max": 1},
                                "values": {"max": 1}
                            }
                        ],
                        "categorical": {
                            "categories": {
                                "for": {"in": "category"}
                            },
                            "values": {
                                "select": [{"for": {"in": "values"}}]
                            }
                        }
                    }
                ],
                "objects": {
                    "general": {
                        "displayName": "General",
                        "properties": {
                            "formatString": {
                                "type": {"formatting": {"formatString": True}}
                            }
                        }
                    },
                    "dataPoint": {
                        "displayName": "Data colors",
                        "properties": {
                            "fill": {
                                "displayName": "Fill",
                                "type": {"fill": {"solid": {"color": True}}}
                            }
                        }
                    }
                },
                "sorting": {
                    "custom": {}
                },
                "supportsHighlight": True
            }
            
            with open(os.path.join(temp_dir, 'capabilities.json'), 'w', encoding='utf-8') as f:
                json.dump(capabilities, f, indent=2)
            
            # 3. package.json - definición del paquete NPM
            package_json = {
                "name": f"creador-graficos-{chart_type.replace('_', '-')}",
                "version": "1.0.0",
                "description": description,
                "main": "src/visual.ts",
                "scripts": {
                    "build": "pbiviz package",
                    "start": "pbiviz start"
                },
                "dependencies": {
                    "powerbi-visuals-api": "~4.6.0"
                },
                "devDependencies": {
                    "powerbi-visuals-tools": "~4.0.0"
                }
            }
            
            with open(os.path.join(temp_dir, 'package.json'), 'w', encoding='utf-8') as f:
                json.dump(package_json, f, indent=2)
            
            # 4. Crear código TypeScript más robusto
            os.makedirs(os.path.join(temp_dir, 'src'), exist_ok=True)
            
            # 4.1 visual.ts - código principal del visual
            typescript_code = f'''/**
 * Visual personalizado para Power BI - {title}
 * Generado por Creador de Gráficos
 * Tipo: {chart_type}
 */

"use strict";

import "./../style/visual.less";
import powerbi from "powerbi-visuals-api";

import VisualConstructorOptions = powerbi.extensibility.visual.VisualConstructorOptions;
import VisualUpdateOptions = powerbi.extensibility.visual.VisualUpdateOptions;
import IVisual = powerbi.extensibility.visual.IVisual;
import EnumerateVisualObjectInstancesOptions = powerbi.EnumerateVisualObjectInstancesOptions;
import VisualObjectInstance = powerbi.VisualObjectInstance;
import DataView = powerbi.DataView;
import VisualObjectInstanceEnumerationObject = powerbi.VisualObjectInstanceEnumerationObject;

export class Visual implements IVisual {{
    private target: HTMLElement;
    private settings: VisualSettings;

    constructor(options: VisualConstructorOptions) {{
        this.target = options.element;
        this.settings = Visual.parseSettings(options.dataViews);
        
        // Crear contenedor principal
        this.target.innerHTML = `
            <div class="visual-container">
                <div class="chart-header">
                    <h3 class="chart-title">{title}</h3>
                    <p class="chart-description">{description}</p>
                </div>
                <div id="chartContainer" class="chart-container">
                    <div class="placeholder">
                        <div class="placeholder-icon">📊</div>
                        <h4>Visual {chart_type} listo</h4>
                        <p>Conecta tus datos para visualizar el gráfico</p>
                        <ul class="placeholder-instructions">
                            <li>Arrastra campos a "Category" para el eje X</li>
                            <li>Arrastra campos a "Values" para el eje Y</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }}

    public update(options: VisualUpdateOptions) {{
        this.settings = Visual.parseSettings(options.dataViews);
        
        const dataView: DataView = options.dataViews[0];
        const chartContainer = this.target.querySelector('#chartContainer') as HTMLElement;
        
        if (!chartContainer) return;
        
        if (!dataView || !dataView.categorical) {{
            // Mostrar placeholder si no hay datos
            chartContainer.innerHTML = `
                <div class="placeholder">
                    <div class="placeholder-icon">📊</div>
                    <h4>No hay datos disponibles</h4>
                    <p>Conecta campos de datos para generar el gráfico {chart_type}</p>
                </div>
            `;
            return;
        }}
        
        const categorical = dataView.categorical;
        const categories = categorical.categories;
        const values = categorical.values;
        
        // Procesar datos
        let chartData = [];
        if (categories && categories[0] && values && values[0]) {{
            const categoryData = categories[0];
            const valueData = values[0];
            
            for (let i = 0; i < categoryData.values.length; i++) {{
                chartData.push({{
                    category: categoryData.values[i],
                    value: valueData.values[i]
                }});
            }}
        }}
        
        // Renderizar gráfico básico
        this.renderChart(chartContainer, chartData, chart_type);
    }}
    
    private renderChart(container: HTMLElement, data: any[], chartType: string) {{
        // Implementación básica de renderizado
        let chartHTML = `
            <div class="chart-content">
                <div class="chart-info">
                    <h4>Gráfico {chart_type}</h4>
                    <p>${{data.length}} elementos de datos</p>
                </div>
                <div class="data-preview">
        `;
        
        // Mostrar muestra de datos
        data.slice(0, 10).forEach((item, index) => {{
            chartHTML += `
                <div class="data-item">
                    <span class="category">${{item.category}}</span>
                    <span class="value">${{item.value}}</span>
                    <div class="bar" style="width: ${{Math.min(100, (item.value / Math.max(...data.map(d => d.value))) * 100)}}%"></div>
                </div>
            `;
        }});
        
        if (data.length > 10) {{
            chartHTML += `<p class="more-data">... y ${{data.length - 10}} elementos más</p>`;
        }}
        
        chartHTML += `
                </div>
                <div class="chart-spec">
                    <details>
                        <summary>Especificación del gráfico</summary>
                        <pre>{json.dumps(spec_dict, indent=2)}</pre>
                    </details>
                </div>
            </div>
        `;
        
        container.innerHTML = chartHTML;
    }}

    private static parseSettings(dataView: DataView): VisualSettings {{
        return VisualSettings.parse(dataView) as VisualSettings;
    }}

    public enumerateObjectInstances(options: EnumerateVisualObjectInstancesOptions): VisualObjectInstance[] | VisualObjectInstanceEnumerationObject {{
        return VisualSettings.enumerateObjectInstances(this.settings || VisualSettings.getDefault(), options);
    }}
}}

class VisualSettings {{
    public static getDefault(): VisualSettings {{
        return new VisualSettings();
    }}
    
    public static parse(dataView: DataView): VisualSettings {{
        return new VisualSettings();
    }}
    
    public static enumerateObjectInstances(settings: VisualSettings, options: EnumerateVisualObjectInstancesOptions): VisualObjectInstance[] | VisualObjectInstanceEnumerationObject {{
        return [];
    }}
}}'''
            
            with open(os.path.join(temp_dir, 'src', 'visual.ts'), 'w', encoding='utf-8') as f:
                f.write(typescript_code)
            
            # 5. Crear archivos de estilo mejorados
            os.makedirs(os.path.join(temp_dir, 'style'), exist_ok=True)
            
            css_content = '''.visual-container {
    width: 100%;
    height: 100%;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    display: flex;
    flex-direction: column;
    padding: 10px;
    box-sizing: border-box;
}

.chart-header {
    margin-bottom: 15px;
    text-align: center;
}

.chart-title {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 5px 0;
    color: #333;
}

.chart-description {
    font-size: 12px;
    color: #666;
    margin: 0;
}

.chart-container {
    flex: 1;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #fafafa;
}

.placeholder {
    text-align: center;
    padding: 40px 20px;
}

.placeholder-icon {
    font-size: 48px;
    margin-bottom: 15px;
}

.placeholder h4 {
    margin: 0 0 10px 0;
    font-size: 16px;
    color: #333;
}

.placeholder p {
    margin: 0 0 15px 0;
    color: #666;
    font-size: 14px;
}

.placeholder-instructions {
    text-align: left;
    max-width: 300px;
    margin: 0 auto;
}

.placeholder-instructions li {
    margin: 5px 0;
    color: #777;
    font-size: 12px;
}

.chart-content {
    width: 100%;
    height: 100%;
    padding: 20px;
    box-sizing: border-box;
}

.chart-info {
    margin-bottom: 15px;
    text-align: center;
}

.chart-info h4 {
    margin: 0 0 5px 0;
    color: #333;
}

.chart-info p {
    margin: 0;
    font-size: 12px;
    color: #666;
}

.data-preview {
    max-height: 300px;
    overflow-y: auto;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: white;
}

.data-item {
    display: flex;
    align-items: center;
    padding: 8px 12px;
    border-bottom: 1px solid #f0f0f0;
    position: relative;
}

.data-item:last-child {
    border-bottom: none;
}

.category {
    min-width: 100px;
    font-weight: 500;
    margin-right: 15px;
}

.value {
    min-width: 60px;
    text-align: right;
    margin-right: 15px;
    font-family: monospace;
}

.bar {
    height: 4px;
    background: linear-gradient(90deg, #0078d4, #106ebe);
    border-radius: 2px;
    min-width: 2px;
}

.more-data {
    text-align: center;
    padding: 10px;
    color: #666;
    font-size: 12px;
    margin: 0;
}

.chart-spec {
    margin-top: 20px;
}

.chart-spec details {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px;
}

.chart-spec summary {
    cursor: pointer;
    font-weight: 500;
    color: #0078d4;
}

.chart-spec pre {
    background: #f8f8f8;
    padding: 10px;
    border-radius: 4px;
    font-size: 11px;
    overflow-x: auto;
    margin: 10px 0 0 0;
}'''
            
            with open(os.path.join(temp_dir, 'style', 'visual.less'), 'w', encoding='utf-8') as f:
                f.write(css_content)
            
            # 6. Crear archivos de configuración adicionales
            
            # 6.1 tsconfig.json
            tsconfig = {
                "compilerOptions": {
                    "target": "ES5",
                    "lib": ["ES2015", "DOM"],
                    "module": "commonjs",
                    "moduleResolution": "node",
                    "noImplicitAny": True,
                    "removeComments": True,
                    "preserveConstEnums": True,
                    "sourceMap": True,
                    "declaration": True,
                    "outDir": "./lib/",
                    "experimentalDecorators": True
                },
                "files": ["src/visual.ts"]
            }
            
            with open(os.path.join(temp_dir, 'tsconfig.json'), 'w', encoding='utf-8') as f:
                json.dump(tsconfig, f, indent=2)
                
            # 6.2 Crear icono básico en base64 (PNG 20x20)
            os.makedirs(os.path.join(temp_dir, 'assets'), exist_ok=True)
            
            # Icono simple en base64 (20x20 PNG)
            icon_base64 = '''iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFKSURBVDhPpZM9SwNBEIafxsJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sLwcJCG1sL'''
            
            icon_data = base64.b64decode(icon_base64.replace('\n', '') + '==')
            with open(os.path.join(temp_dir, 'assets', 'icon.png'), 'wb') as f:
                f.write(icon_data)
    height: calc(100% - 40px);
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
}'''
            
            with open(os.path.join(temp_dir, 'style', 'visual.less'), 'w', encoding='utf-8') as f:
                f.write(css_content)
            
            # 6. Crear el archivo .pbiviz (ZIP)
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_name = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arc_name)
            
            # Limpiar directorio temporal
            import shutil
            shutil.rmtree(temp_dir)
            
            return True
            
        except Exception as e:
            print(f"Error creando archivo .pbiviz: {e}")
            return False
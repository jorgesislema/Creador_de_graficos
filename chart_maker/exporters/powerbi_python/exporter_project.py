# Exportador para proyectos de desarrollo Power BI 
# Genera proyectos completos listos para compilar con 'pbiviz package'
from ..base import IExporter
import json
import os
import base64
from datetime import datetime
import uuid
import shutil

class PowerBIPythonExporter(IExporter):
    def export(self, spec, output_path: str):
        """Genera un proyecto de desarrollo Power BI completo listo para compilación"""
        try:
            # Extraer información del spec
            spec_dict = getattr(spec, 'dict', lambda: spec)() if hasattr(spec, 'dict') else spec
            chart_type = spec_dict.get('type', 'barras_vertical')
            title = spec_dict.get('title', 'Gráfico Sin Título')
            description = spec_dict.get('description', 'Gráfico creado con Creador de Gráficos')
            
            # Crear directorio del proyecto (no ZIP, sino directorio completo)
            project_name = os.path.splitext(os.path.basename(output_path))[0]
            project_dir = os.path.join(os.path.dirname(output_path), f"{project_name}_PowerBI_Project")
            
            # Limpiar directorio si existe
            if os.path.exists(project_dir):
                shutil.rmtree(project_dir)
            
            os.makedirs(project_dir, exist_ok=True)
            
            # Crear estructura de directorios
            os.makedirs(os.path.join(project_dir, 'src'), exist_ok=True)
            os.makedirs(os.path.join(project_dir, 'style'), exist_ok=True) 
            os.makedirs(os.path.join(project_dir, 'assets'), exist_ok=True)
            
            # 1. pbiviz.json - metadata del visual
            visual_guid = str(uuid.uuid4()).upper().replace('-', '')
            pbiviz_config = {
                "visual": {
                    "name": f"CreadorGraficos{chart_type.replace('_', '')}",
                    "displayName": title[:50],
                    "guid": f"CreadorGraficos{visual_guid[:15]}",
                    "visualClassName": "Visual",
                    "version": "1.0.0.0",
                    "description": description[:200],
                    "supportUrl": "https://github.com/jorgesislema/Creador_de_graficos",
                    "gitHubUrl": "https://github.com/jorgesislema/Creador_de_graficos"
                },
                "apiVersion": "5.8.0",
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
            
            with open(os.path.join(project_dir, 'pbiviz.json'), 'w', encoding='utf-8') as f:
                json.dump(pbiviz_config, f, indent=2, ensure_ascii=False)
            
            # 2. capabilities.json - define qué datos puede recibir el visual
            capabilities = {
                "privileges": [],
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
            
            with open(os.path.join(project_dir, 'capabilities.json'), 'w', encoding='utf-8') as f:
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
                    "d3": "^7.0.0",
                    "@types/d3": "^7.0.0"
                },
                "devDependencies": {
                    "powerbi-visuals-tools": "latest",
                    "@typescript-eslint/eslint-plugin": "latest",
                    "@typescript-eslint/parser": "latest",
                    "eslint": "latest",
                    "typescript": "latest"
                }
            }
            
            with open(os.path.join(project_dir, 'package.json'), 'w', encoding='utf-8') as f:
                json.dump(package_json, f, indent=2)
            
            # 4. visual.ts - código principal del visual
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
import DataView = powerbi.DataView;

export class Visual implements IVisual {{
    private target: HTMLElement;

    constructor(options: VisualConstructorOptions) {{
        this.target = options.element;
        
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
        this.renderChart(chartContainer, chartData, "{chart_type}");
    }}
    
    private renderChart(container: HTMLElement, data: any[], chartType: string) {{
        let chartHTML = `
            <div class="chart-content">
                <div class="chart-info">
                    <h4>Gráfico ${{chartType}}</h4>
                    <p>${{data.length}} elementos de datos</p>
                </div>
                <div class="data-preview">
        `;
        
        // Mostrar muestra de datos
        data.slice(0, 10).forEach((item, index) => {{
            const maxValue = Math.max(...data.map(d => d.value || 0));
            const width = maxValue > 0 ? Math.min(100, (item.value / maxValue) * 100) : 0;
            chartHTML += `
                <div class="data-item">
                    <span class="category">${{item.category}}</span>
                    <span class="value">${{item.value}}</span>
                    <div class="bar" style="width: ${{width}}%"></div>
                </div>
            `;
        }});
        
        if (data.length > 10) {{
            chartHTML += `<p class="more-data">... y ${{data.length - 10}} elementos más</p>`;
        }}
        
        chartHTML += `
                </div>
            </div>
        `;
        
        container.innerHTML = chartHTML;
    }}
}}'''
            
            with open(os.path.join(project_dir, 'src', 'visual.ts'), 'w', encoding='utf-8') as f:
                f.write(typescript_code)
            
            # 5. visual.less - estilos CSS/LESS
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
}'''
            
            with open(os.path.join(project_dir, 'style', 'visual.less'), 'w', encoding='utf-8') as f:
                f.write(css_content)
            
            # 6. tsconfig.json - configuración TypeScript
            tsconfig = {
                "compilerOptions": {
                    "target": "ES6",
                    "lib": ["ES2015", "DOM"],
                    "module": "commonjs",
                    "moduleResolution": "node",
                    "noImplicitAny": False,
                    "removeComments": True,
                    "preserveConstEnums": True,
                    "sourceMap": True,
                    "declaration": True,
                    "outDir": "./lib/",
                    "experimentalDecorators": True
                },
                "files": ["src/visual.ts"]
            }
            
            with open(os.path.join(project_dir, 'tsconfig.json'), 'w', encoding='utf-8') as f:
                json.dump(tsconfig, f, indent=2)
                
            # 7. Crear icono PNG simple (base64) 
            # Icono básico 20x20 PNG en base64 
            icon_b64 = "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAACXBIWXMAABCFAAAQHQHI4BAkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAALxJREFUOI2tlE0KwjAQRl8oiKCgIoK/C1f+gJ5Ad15Al+7EpXv3LryCJ3DjSdzpCpoOPYJfoTNNvnlvJhMjhOAXax4jIgqRrfdeVlWl8zzXruuqoig0TdPPP4BSSkVRFMqyTNd1rdM01WEY6qZpNAxD3fe97vte931f971e13Utx3Gsm6ZRSilVVaX7vk9r1DRNo7Zt67qu67quK8uy1HVd67quw+8bx7EKgkBVVaXruqr3XiVJooqiUMaYrxGfw/4CWD0vDrGJXwMAAABJRU5ErkJggg=="
            
            with open(os.path.join(project_dir, 'assets', 'icon.png'), 'wb') as f:
                f.write(base64.b64decode(icon_b64))
            
            # 8. Crear archivo README con instrucciones de compilación
            readme_content = f'''# Proyecto Power BI Visual - {title}

Este es un proyecto de desarrollo de visual personalizado para Power BI generado automáticamente por **Creador de Gráficos**.

## 📊 Información del Visual

- **Tipo de gráfico**: {chart_type}
- **Título**: {title}
- **Descripción**: {description}
- **Fecha de creación**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 🚀 Instrucciones de Compilación

### Prerrequisitos

1. Instala [Node.js](https://nodejs.org/) (versión 14 o superior)
2. Instala las herramientas de Power BI:
   ```bash
   npm install -g powerbi-visuals-tools
   ```

### Compilación

1. Abre una terminal en este directorio
2. Instala las dependencias:
   ```bash
   npm install
   ```
3. Compila el proyecto:
   ```bash
   pbiviz package
   ```

Esto generará el archivo `.pbiviz` en la carpeta `dist/` que puedes importar en Power BI.

### Desarrollo

Para desarrollo en tiempo real:
```bash
pbiviz start
```

## 📁 Estructura del Proyecto

```
{project_name}_PowerBI_Project/
├── src/
│   └── visual.ts          # Código principal del visual
├── style/
│   └── visual.less        # Estilos CSS/LESS
├── assets/
│   └── icon.png           # Icono del visual (20x20px)
├── capabilities.json      # Capacidades y configuración
├── pbiviz.json           # Metadata del visual
├── package.json          # Dependencias NPM
├── tsconfig.json         # Configuración TypeScript
└── README.md             # Este archivo

```

## 🔧 Personalización

- Edita `src/visual.ts` para modificar la lógica del visual
- Modifica `style/visual.less` para cambiar los estilos
- Actualiza `capabilities.json` para cambiar los datos que acepta el visual

## ℹ️ Información Técnica

- **API Version**: 5.8.0
- **Framework**: TypeScript + D3.js
- **Generado por**: Creador de Gráficos v1.0

---

*Para más información sobre el desarrollo de visuals de Power BI, consulta la [documentación oficial de Microsoft](https://docs.microsoft.com/en-us/power-bi/developer/visuals/).*
'''

            with open(os.path.join(project_dir, 'README.md'), 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            # 9. Crear archivo .gitignore
            gitignore_content = '''# Build outputs
dist/
lib/
node_modules/
*.pbiviz

# IDE
.vscode/
.vs/

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# OS
.DS_Store
Thumbs.db

# Temp files
*.tmp
*.temp
'''

            with open(os.path.join(project_dir, '.gitignore'), 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            
            return {
                "success": True,
                "message": f"Proyecto Power BI creado exitosamente en: {project_dir}",
                "project_path": project_dir,
                "instructions": f"Para compilar: cd '{project_dir}' && npm install && pbiviz package"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error al generar proyecto Power BI: {str(e)}",
                "project_path": None,
                "instructions": None
            }
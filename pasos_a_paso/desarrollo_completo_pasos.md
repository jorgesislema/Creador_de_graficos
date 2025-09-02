# Pasos Detallados para el Desarrollo del Creador de Gráficos

## 📋 Resumen del Proyecto

**Objetivo**: Crear un programa completo para generar visualizaciones de datos y exportarlas a diferentes plataformas de análisis empresarial (Power BI, Tableau, Looker, Looker Studio).

**Duración del desarrollo**: Aproximadamente 4-6 horas de trabajo intensivo

**Tecnologías utilizadas**:
- Python 3.12
- PySide6 (GUI)
- Pydantic (validación)
- Vega-Lite (visualización)
- Jinja2 (templates)
- Pandas (datos)

## 🎯 Fase 1: Configuración del Entorno (30 minutos)

### Paso 1.1: Crear Estructura del Proyecto
```bash
# Crear directorios principales
mkdir chart_maker
cd chart_maker
mkdir app core exporters packaging tests
mkdir app/ui exporters/powerbi_python exporters/tableau exporters/looker exporters/looker_studio
```

### Paso 1.2: Configurar Entorno Python
```bash
# Crear entorno Conda
conda create -n chartmaker python=3.12 -y

# Instalar dependencias principales
pip install pyside6 pydantic jinja2 pandas
```

### Paso 1.3: Crear Archivos Base
- `__init__.py` en cada carpeta de módulo
- `requirements.txt` con dependencias
- `pyproject.toml` para configuración del proyecto

**Lección aprendida**: Es crucial configurar correctamente el PYTHONPATH para evitar errores de importación.

## 🏗️ Fase 2: Arquitectura Central (45 minutos)

### Paso 2.1: Definir Tipos de Gráficos
**Archivo**: `core/chart_types.py`
```python
CHART_TYPES = [
    "bar", "stacked_bar", "line", "area", "scatter", 
    "pie", "donut", "histogram", "boxplot", "heatmap",
    "treemap", "sankey", "waterfall", "funnel", "radar",
    # ... 43 tipos en total
]
```

### Paso 2.2: Crear Sistema de Validación
**Archivo**: `core/spec.py`
```python
from pydantic import BaseModel, validator

class ChartSpec(BaseModel):
    type: str
    data: Union[List[Dict], Dict]
    encoding: Dict[str, Any]
    options: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('type')
    def validate_chart_type(cls, v):
        if v not in CHART_TYPES:
            raise ValueError(f'Tipo no soportado: {v}')
        return v
```

### Paso 2.3: Crear Ejemplos Predefinidos
**Archivo**: `core/examples.py`
- 43 ejemplos completos, uno por cada tipo de gráfico
- Datos de muestra realistas
- Configuraciones de encoding apropiadas

**Desafío encontrado**: Los tipos en examples.py deben coincidir exactamente con chart_types.py. Tuvimos que corregir varios tipos como "point" → "scatter", "arc" → "pie".

## 🎨 Fase 3: Interfaz Gráfica (90 minutos)

### Paso 3.1: Ventana Principal
**Archivo**: `app/ui/main_window.py`

Estructura de layout:
```python
# Splitter horizontal principal
main_splitter = QSplitter(Qt.Horizontal)

# Panel izquierdo: Controles con pestañas
tab_widget = QTabWidget()
- Básico: Tipo de gráfico, encoding
- Datos: Editor JSON + importador CSV  
- Estilo: Colores, temas, opciones

# Panel derecho: Vista previa + exportación
```

### Paso 3.2: Sistema de Pestañas
- **Pestaña Básico**: ComboBox para tipos, configuración de encoding
- **Pestaña Datos**: 
  - Sub-pestaña JSON: Editor de texto con syntax highlighting
  - Sub-pestaña CSV: Importador con vista previa
- **Pestaña Estilo**: Esquemas de color, temas, opciones visuales

### Paso 3.3: Vista Previa en Tiempo Real
**Archivo**: `app/ui/preview_web_view.py`
```python
class PreviewWebView(QTextBrowser):
    def update_chart(self, spec):
        html_content = self._generate_vega_lite_html(spec)
        self.setHtml(html_content)
```

**Decisión técnica**: Usamos QTextBrowser en lugar de QWebEngineView para evitar dependencias complejas de WebEngine.

## 📊 Fase 4: Sistema de Exportación (75 minutos)

### Paso 4.1: Interfaz Base de Exportadores
**Archivo**: `exporters/base.py`
```python
from abc import ABC, abstractmethod

class IExporter(ABC):
    @abstractmethod
    def export(self, spec, output_path: str):
        pass
```

### Paso 4.2: Exportador Power BI
**Archivo**: `exporters/powerbi_python/exporter.py`

Características implementadas:
- Genera scripts Python compatibles con Power BI
- Usa matplotlib y pandas
- Soporte para múltiples tipos de gráficos
- Código limpio y comentado

```python
def _generate_bar_chart(self, encoding):
    x_field = encoding.get('x', {}).get('field', 'x')
    y_field = encoding.get('y', {}).get('field', 'y')
    
    return f"""# Crear gráfico de barras
ax = dataset.plot(kind='bar', x='{x_field}', y='{y_field}')
ax.set_title('Gráfico de Barras')
"""
```

### Paso 4.3: Exportador Tableau
**Archivo**: `exporters/tableau/exporter.py`

Características implementadas:
- Genera archivos TWB (XML)
- Estructura completa de workbook
- Datasources, worksheets, windows
- Mapeo automático de campos

### Paso 4.4: Exportador Looker
**Archivo**: `exporters/looker/exporter.py`

Características implementadas:
- Genera archivos LookML
- Views con dimensiones y medidas
- Modelos con explores
- Dashboards con elementos

### Paso 4.5: Exportador Looker Studio
**Archivo**: `exporters/looker_studio/exporter.py`

Características implementadas:
- Configuración JSON para Looker Studio
- Data sources y schema mapping
- Chart elements con estilos
- Mapeo de tipos de visualización

## 📈 Fase 5: Funcionalidad CSV (45 minutos)

### Paso 5.1: Importador CSV
```python
def load_csv_file(self):
    # Detectar dialecto automáticamente
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(sample)
    
    # Convertir tipos automáticamente
    for key, value in row.items():
        try:
            if '.' in value:
                converted_row[key] = float(value)
            else:
                converted_row[key] = int(value)
        except ValueError:
            converted_row[key] = value
```

### Paso 5.2: Vista Previa CSV
- Tabla formateada con primeras 5 filas
- Información de dimensiones (filas x columnas)
- Conversión automática a JSON para el editor

## 🐛 Fase 6: Depuración y Resolución de Problemas (60 minutos)

### Problema 1: Errores de Importación
**Error**: `ModuleNotFoundError: No module named 'chart_maker'`

**Solución**:
```bash
$env:PYTHONPATH = "$env:PYTHONPATH;."
```

### Problema 2: Validación de Tipos
**Error**: `Tipo de gráfico no soportado: point`

**Solución**: Corregir tipos en examples.py para que coincidan con chart_types.py:
- "point" → "scatter"
- "arc" → "pie" 
- "rect" → "heatmap"
- "geoshape" → "choropleth"

### Problema 3: Encoding Vacío
**Error**: `La codificación no puede estar vacía`

**Solución**: Modificar validación para permitir encoding vacío en ciertos tipos:
```python
@validator('encoding')
def validate_encoding(cls, v, values):
    allowed_empty_encoding = ['table', 'kpi', 'gauge']
    chart_type = values.get('type')
    
    if not v and chart_type not in allowed_empty_encoding:
        raise ValueError('La codificación no puede estar vacía')
    return v
```

## 🧪 Fase 7: Pruebas y Validación (30 minutos)

### Paso 7.1: Pruebas de Interfaz
- Verificar que todas las pestañas se abren correctamente
- Comprobar que los ejemplos se cargan sin errores
- Validar que la vista previa se actualiza en tiempo real

### Paso 7.2: Pruebas de Exportación
- Probar exportación a cada plataforma
- Verificar formato de archivos generados
- Confirmar que los archivos son válidos

### Paso 7.3: Pruebas de CSV
- Importar diferentes formatos CSV
- Verificar detección automática de tipos
- Comprobar vista previa y conversión a JSON

## 📚 Lecciones Aprendidas

### 1. Gestión de Dependencias
- **Problema**: Conflictos entre PySide6 y WebEngine
- **Solución**: Usar QTextBrowser como alternativa más ligera
- **Aprendizaje**: Siempre tener un plan B para dependencias complejas

### 2. Validación de Datos
- **Problema**: Validación muy estricta causaba errores en ejemplos válidos
- **Solución**: Validación contextual basada en tipo de gráfico
- **Aprendizaje**: La validación debe ser flexible y específica por contexto

### 3. Arquitectura Modular
- **Beneficio**: Fácil agregar nuevos exportadores
- **Implementación**: Patrón Strategy con interfaz IExporter
- **Aprendizaje**: La modularidad facilita la extensibilidad

### 4. Manejo de Errores
- **Estrategia**: Try-catch exhaustivo con mensajes descriptivos
- **UI**: Mostrar errores al usuario de forma amigable
- **Aprendizaje**: Los errores descriptivos ahorran tiempo de depuración

## 🚀 Posibles Mejoras Futuras

### 1. Funcionalidades Adicionales
- Soporte para bases de datos (SQL, NoSQL)
- Editor visual de drag-and-drop
- Plantillas personalizables
- Exportación a más plataformas (Qlik, Plotly)

### 2. Optimizaciones de Rendimiento
- Lazy loading para ejemplos grandes
- Cache de visualizaciones
- Procesamiento asíncrono para archivos grandes

### 3. Experiencia de Usuario
- Tours guiados para nuevos usuarios
- Shortcuts de teclado
- Tema oscuro
- Soporte multi-idioma

## 🔧 Comandos Útiles para Desarrollo

### Ejecutar el Programa
```bash
cd chart_maker
$env:PYTHONPATH = "$env:PYTHONPATH;."
python app/main.py
```

### Agregar Nuevo Tipo de Gráfico
1. Editar `core/chart_types.py`
2. Agregar ejemplo en `core/examples.py`
3. Actualizar mapeos en exportadores si es necesario

### Agregar Nuevo Exportador
1. Crear clase en `exporters/nueva_plataforma/`
2. Implementar interfaz `IExporter`
3. Registrar en `exporters/__init__.py`
4. Agregar botón en `main_window.py`

### Depuración
```bash
# Verificar importaciones
python -c "from chart_maker.core.examples import EXAMPLES; print('OK')"

# Probar exportador
python -c "from chart_maker.exporters import get_exporter; print(get_exporter('powerbi_python'))"
```

## 🎉 Conclusión

Este proyecto demuestra cómo crear una aplicación completa de visualización de datos con:
- Arquitectura modular y extensible
- Interfaz gráfica moderna
- Soporte multi-plataforma
- Manejo robusto de errores
- Documentación completa

**Tiempo total de desarrollo**: ~6 horas
**Líneas de código**: ~2000+ líneas
**Archivos creados**: 20+ archivos
**Funcionalidades**: 43 tipos de gráficos, 4 exportadores, soporte CSV/JSON

El resultado es una herramienta profesional lista para usar en entornos empresariales de análisis de datos.

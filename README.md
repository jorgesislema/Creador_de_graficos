# Creador de Gráficos - Chart Maker

Un programa completo para crear visualizaciones de datos y exportarlas a diferentes plataformas de análisis empresarial.

## 🎯 Características Principales

- **Interfaz Gráfica Intuitiva**: GUI moderna desarrollada con PySide6
- **43 Tipos de Gráficos**: Desde básicos (barras, líneas) hasta avanzados (sankey, radar, treemap)
- **Soporte Multi-formato**: Importa datos desde JSON y CSV
- **Exportación Multi-plataforma**: 
  - Power BI (script Python)
  - Tableau (archivo TWB)
  - Looker (LookML)
  - Looker Studio (configuración JSON)
- **Vista Previa en Tiempo Real**: Visualización instantánea con Vega-Lite
- **Validación de Datos**: Sistema robusto con Pydantic

## 📋 Requisitos del Sistema

- **Python**: 3.12 o superior
- **Sistema Operativo**: Windows, macOS, Linux
- **Memoria RAM**: 4GB mínimo, 8GB recomendado
- **Espacio en Disco**: 500MB para instalación completa

## 🚀 Instalación

### Opción 1: Instalación con Conda (Recomendado)

```bash
# Crear entorno virtual
conda create -n chartmaker python=3.12 -y

# Activar entorno
conda activate chartmaker

# Instalar dependencias
pip install pyside6 pydantic jinja2 pandas
```

### Opción 2: Instalación con pip

```bash
# Crear entorno virtual
python -m venv chartmaker_env

# Activar entorno (Windows)
chartmaker_env\Scripts\activate

# Activar entorno (macOS/Linux)
source chartmaker_env/bin/activate

# Instalar dependencias
pip install -r chart_maker/requirements.txt
```

## 🎮 Uso del Programa

### Ejecutar la Aplicación

```bash
# Navegar al directorio del proyecto
cd chart_maker

# Configurar PYTHONPATH (Windows PowerShell)
$env:PYTHONPATH = "$env:PYTHONPATH;."

# Ejecutar el programa
python app/main.py
```

### Interfaz Principal

La aplicación se divide en tres áreas principales:

1. **Panel de Controles** (Izquierda)
   - **Básico**: Selección de tipo de gráfico y configuración de encoding
   - **Datos**: Editor JSON y importador CSV
   - **Estilo**: Temas, colores y opciones de visualización

2. **Vista Previa** (Centro)
   - Visualización en tiempo real del gráfico
   - Información detallada del gráfico actual

3. **Exportación** (Derecha)
   - Botones para exportar a diferentes formatos y plataformas

## 📊 Tipos de Gráficos Disponibles

### Básicos
- **bar**: Gráfico de barras vertical
- **stacked_bar**: Barras apiladas
- **line**: Gráfico de líneas
- **area**: Gráfico de área
- **scatter**: Diagrama de dispersión
- **pie**: Gráfico circular
- **donut**: Gráfico de dona

### Estadísticos
- **histogram**: Histograma
- **boxplot**: Diagrama de caja
- **violin**: Gráfico violín
- **heatmap**: Mapa de calor

### Especializados
- **treemap**: Mapa de árbol
- **sankey**: Diagrama de Sankey
- **waterfall**: Gráfico cascada
- **funnel**: Gráfico embudo
- **radar**: Gráfico radar
- **sunburst**: Gráfico sunburst

### Empresariales
- **kpi**: Indicadores clave
- **gauge**: Medidores
- **candlestick**: Gráfico de velas
- **gantt**: Diagrama de Gantt

## 💾 Formatos de Datos

### Importar Datos JSON

```json
[
  {"categoria": "A", "valor": 100, "fecha": "2025-01-01"},
  {"categoria": "B", "valor": 150, "fecha": "2025-01-02"},
  {"categoria": "C", "valor": 200, "fecha": "2025-01-03"}
]
```

### Importar Datos CSV

```csv
categoria,valor,fecha
A,100,2025-01-01
B,150,2025-01-02
C,200,2025-01-03
```

El programa detecta automáticamente:
- Tipos de datos (numérico, texto, fecha)
- Delimitadores CSV
- Codificación de caracteres

## 🔄 Exportación a Plataformas

### Power BI
- **Formato**: Script Python (.py)
- **Usa**: matplotlib y pandas
- **Compatible**: Power BI Desktop y Service
- **Ejemplo de salida**:
```python
import matplotlib.pyplot as plt
import pandas as pd

data = [{"x": 1, "y": 2}, {"x": 2, "y": 3}]
dataset = pd.DataFrame(data)
dataset.plot(kind='bar', x='x', y='y')
plt.show()
```

### Tableau
- **Formato**: Workbook (.twb)
- **Estructura**: XML con datasources, worksheets y dashboards
- **Compatible**: Tableau Desktop 2018.1+
- **Incluye**: Configuración de campos, filtros y visualizaciones

### Looker
- **Formato**: LookML (.lkml)
- **Componentes**: Views, models y dashboards
- **Compatible**: Looker 7.0+
- **Ejemplo de salida**:
```lookml
view: chart_view {
  sql_table_name: public.chart_data ;;
  
  dimension: categoria {
    type: string
    sql: ${TABLE}.categoria ;;
  }
  
  measure: total_valor {
    type: sum
    sql: ${valor} ;;
  }
}
```

### Looker Studio
- **Formato**: Configuración JSON (.json)
- **Incluye**: Fuentes de datos, elementos de gráfico y estilos
- **Compatible**: Google Looker Studio
- **Estructura**: Páginas, elementos y mapeos de datos

## 🛠️ Arquitectura del Proyecto

```
chart_maker/
├── app/                    # Aplicación GUI
│   ├── main.py            # Punto de entrada
│   └── ui/                # Interfaz de usuario
│       ├── main_window.py # Ventana principal
│       └── preview_web_view.py # Vista previa
├── core/                  # Lógica central
│   ├── chart_types.py     # Tipos de gráficos
│   ├── examples.py        # Ejemplos predefinidos
│   └── spec.py           # Especificaciones con Pydantic
├── exporters/             # Exportadores
│   ├── base.py           # Interfaz base
│   ├── powerbi_python/   # Exportador Power BI
│   ├── tableau/          # Exportador Tableau
│   ├── looker/           # Exportador Looker
│   └── looker_studio/    # Exportador Looker Studio
├── packaging/             # Empaquetado
└── tests/                # Pruebas unitarias
```

## 🔧 Personalización

### Agregar Nuevos Tipos de Gráficos

1. Editar `core/chart_types.py`:
```python
CHART_TYPES = [
    # ... tipos existentes ...
    "mi_nuevo_grafico"
]
```

2. Agregar ejemplo en `core/examples.py`:
```python
EXAMPLES = {
    # ... ejemplos existentes ...
    "mi_nuevo_grafico": ChartSpec(
        type="mi_nuevo_grafico",
        data=[{"x": 1, "y": 2}],
        encoding={"x": {"field": "x", "type": "quantitative"}}
    )
}
```

### Agregar Nuevos Exportadores

1. Crear clase que herede de `IExporter`:
```python
from exporters.base import IExporter

class MiExportador(IExporter):
    def export(self, spec, output_path: str):
        # Implementar lógica de exportación
        pass
```

2. Registrar en `exporters/__init__.py`:
```python
EXPORTERS = {
    'mi_plataforma': MiExportador
}
```

## 🐛 Solución de Problemas

### Error: "No module named 'chart_maker'"
```bash
# Configurar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:." # Linux/macOS
$env:PYTHONPATH = "$env:PYTHONPATH;." # Windows PowerShell
```

### Error: "PySide6 not found"
```bash
# Reinstalar PySide6
pip uninstall pyside6
pip install pyside6
```

### Error de Validación en Ejemplos
- Verificar que los tipos en `examples.py` coincidan con `chart_types.py`
- Asegurar que el encoding no esté vacío para tipos que lo requieren

### Problemas con CSV
- Verificar codificación del archivo (UTF-8 recomendado)
- Comprobar que los delimitadores sean consistentes
- Asegurar que la primera fila contenga headers

## 🤝 Contribuir

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **PySide6**: Framework GUI moderno
- **Vega-Lite**: Gramática de visualización
- **Pydantic**: Validación de datos robusta
- **Pandas**: Manipulación de datos
- **Jinja2**: Motor de plantillas

## 📞 Soporte

- **Issues**: Reportar bugs en GitHub Issues
- **Documentación**: Wiki del repositorio
- **Ejemplos**: Carpeta `examples/` del proyecto

---

**Desarrollado con ❤️ para la comunidad de análisis de datos**

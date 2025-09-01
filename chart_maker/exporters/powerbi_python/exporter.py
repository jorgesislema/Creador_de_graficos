# exporter.py
# Exportador para script Python de Power BI
from ..base import IExporter
import json
from typing import Dict, Any

class PowerBIPythonExporter(IExporter):
    def export(self, spec, output_path: str):
        """
        Exporta un ChartSpec a script Python para Power BI
        """
        script = self._generate_python_script(spec)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(script)
        
        return True
    
    def _generate_python_script(self, spec) -> str:
        """
        Genera el script Python compatible con Power BI
        """
        chart_type = spec.type
        data = spec.data
        encoding = spec.encoding
        
        # Generar imports
        script = """# Script Python para Power BI
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# Configurar estilo para Power BI
plt.style.use('default')
mpl.rcParams['figure.figsize'] = (12, 8)
mpl.rcParams['font.size'] = 10

"""
        
        # Crear DataFrame con los datos
        script += f"# Datos del gráfico\n"
        script += f"data = {json.dumps(data, ensure_ascii=False, indent=2)}\n"
        script += f"dataset = pd.DataFrame(data)\n\n"
        
        # Generar código específico por tipo de gráfico
        if chart_type in ['bar', 'stacked_bar']:
            script += self._generate_bar_chart(encoding)
        elif chart_type == 'line':
            script += self._generate_line_chart(encoding)
        elif chart_type == 'scatter':
            script += self._generate_scatter_chart(encoding)
        elif chart_type in ['pie', 'donut']:
            script += self._generate_pie_chart(encoding, chart_type == 'donut')
        elif chart_type == 'histogram':
            script += self._generate_histogram(encoding)
        elif chart_type == 'boxplot':
            script += self._generate_boxplot(encoding)
        else:
            # Gráfico básico como fallback
            script += self._generate_basic_chart(encoding)
        
        script += """
# Mostrar el gráfico
plt.tight_layout()
plt.show()
"""
        
        return script
    
    def _generate_bar_chart(self, encoding: Dict) -> str:
        x_field = encoding.get('x', {}).get('field', 'x')
        y_field = encoding.get('y', {}).get('field', 'y')
        
        return f"""# Crear gráfico de barras
ax = dataset.plot(kind='bar', x='{x_field}', y='{y_field}', color='steelblue')
ax.set_title('Gráfico de Barras')
ax.set_xlabel('{x_field.title()}')
ax.set_ylabel('{y_field.title()}')
"""
    
    def _generate_line_chart(self, encoding: Dict) -> str:
        x_field = encoding.get('x', {}).get('field', 'x')
        y_field = encoding.get('y', {}).get('field', 'y')
        
        return f"""# Crear gráfico de líneas
ax = dataset.plot(kind='line', x='{x_field}', y='{y_field}', marker='o')
ax.set_title('Gráfico de Líneas')
ax.set_xlabel('{x_field.title()}')
ax.set_ylabel('{y_field.title()}')
"""
    
    def _generate_scatter_chart(self, encoding: Dict) -> str:
        x_field = encoding.get('x', {}).get('field', 'x')
        y_field = encoding.get('y', {}).get('field', 'y')
        
        return f"""# Crear gráfico de dispersión
ax = dataset.plot(kind='scatter', x='{x_field}', y='{y_field}', alpha=0.7)
ax.set_title('Gráfico de Dispersión')
ax.set_xlabel('{x_field.title()}')
ax.set_ylabel('{y_field.title()}')
"""
    
    def _generate_pie_chart(self, encoding: Dict, is_donut: bool = False) -> str:
        values_field = encoding.get('theta', {}).get('field', 'valor')
        labels_field = encoding.get('color', {}).get('field', 'categoria')
        
        wedgeprops = "wedgeprops={'width': 0.5}" if is_donut else ""
        
        return f"""# Crear gráfico circular
fig, ax = plt.subplots()
ax.pie(dataset['{values_field}'], labels=dataset['{labels_field}'], autopct='%1.1f%%', {wedgeprops})
ax.set_title('Gráfico {"Donut" if is_donut else "Circular"}')
"""
    
    def _generate_histogram(self, encoding: Dict) -> str:
        x_field = encoding.get('x', {}).get('field', 'valor')
        
        return f"""# Crear histograma
ax = dataset['{x_field}'].hist(bins=20, alpha=0.7, color='skyblue', edgecolor='black')
plt.title('Histograma')
plt.xlabel('{x_field.title()}')
plt.ylabel('Frecuencia')
"""
    
    def _generate_boxplot(self, encoding: Dict) -> str:
        y_field = encoding.get('y', {}).get('field', 'valor')
        x_field = encoding.get('x', {}).get('field', 'grupo')
        
        return f"""# Crear boxplot
if '{x_field}' in dataset.columns:
    dataset.boxplot(column='{y_field}', by='{x_field}')
else:
    dataset['{y_field}'].plot(kind='box')
plt.title('Diagrama de Caja')
plt.suptitle('')
"""
    
    def _generate_basic_chart(self, encoding: Dict) -> str:
        return """# Gráfico básico
if len(dataset.columns) >= 2:
    x_col = dataset.columns[0]
    y_col = dataset.columns[1]
    dataset.plot(x=x_col, y=y_col, kind='line', marker='o')
    plt.title('Gráfico de Datos')
else:
    dataset.plot()
    plt.title('Datos')
"""

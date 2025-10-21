# examples.py
# Ejemplos de especificaciones ChartSpec para cada tipo de gráfico en español e inglés
from .spec import ChartSpec

EXAMPLES = {
    # Gráficos Básicos Comunes / Common Basic Charts
    "barras_vertical": ChartSpec(
        type="barras_vertical",
        title="Gráfico de Barras Verticales",
        description="Comparación de categorías con barras verticales",
        data=[{"categoria": "Ventas", "valor": 150}, {"categoria": "Marketing", "valor": 80}, {"categoria": "IT", "valor": 120}],
        encoding={"x": {"field": "categoria", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    
    "bar_chart_vertical": ChartSpec(
        type="bar_chart_vertical", 
        title="Vertical Bar Chart",
        description="Category comparison with vertical bars",
        data=[{"category": "Sales", "value": 150}, {"category": "Marketing", "value": 80}, {"category": "IT", "value": 120}],
        encoding={"x": {"field": "category", "type": "nominal"}, "y": {"field": "value", "type": "quantitative"}},
    ),
    
    "barras_horizontal": ChartSpec(
        type="barras_horizontal",
        title="Gráfico de Barras Horizontales", 
        description="Comparación con barras extendidas horizontalmente",
        data=[{"categoria": "Producto A", "valor": 95}, {"categoria": "Producto B", "valor": 130}, {"categoria": "Producto C", "valor": 75}],
        encoding={"x": {"field": "valor", "type": "quantitative"}, "y": {"field": "categoria", "type": "nominal"}},
    ),
    
    "bar_chart_horizontal": ChartSpec(
        type="bar_chart_horizontal",
        title="Horizontal Bar Chart",
        description="Comparison with horizontally extended bars", 
        data=[{"category": "Product A", "value": 95}, {"category": "Product B", "value": 130}, {"category": "Product C", "value": 75}],
        encoding={"x": {"field": "value", "type": "quantitative"}, "y": {"field": "category", "type": "nominal"}},
    ),
    
    "barras_agrupadas": ChartSpec(
        type="barras_agrupadas",
        title="Gráfico de Barras Agrupadas",
        description="Comparación de múltiples series por categoría",
        data=[
            {"categoria": "Ene", "serie": "2022", "valor": 20}, {"categoria": "Ene", "serie": "2023", "valor": 25},
            {"categoria": "Feb", "serie": "2022", "valor": 18}, {"categoria": "Feb", "serie": "2023", "valor": 30}
        ],
        encoding={"x": {"field": "categoria", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}, "color": {"field": "serie", "type": "nominal"}},
    ),
    
    "grouped_bar_chart": ChartSpec(
        type="grouped_bar_chart",
        title="Grouped Bar Chart", 
        description="Multiple series comparison by category",
        data=[
            {"category": "Jan", "series": "2022", "value": 20}, {"category": "Jan", "series": "2023", "value": 25},
            {"category": "Feb", "series": "2022", "value": 18}, {"category": "Feb", "series": "2023", "value": 30}
        ],
        encoding={"x": {"field": "category", "type": "nominal"}, "y": {"field": "value", "type": "quantitative"}, "color": {"field": "series", "type": "nominal"}},
    ),
    
    # Gráficos de Tendencias / Trend Charts
    "lineas": ChartSpec(
        type="lineas",
        title="Gráfico de Líneas",
        description="Evolución temporal de una variable",
        data=[{"fecha": "2023-01", "valor": 45}, {"fecha": "2023-02", "valor": 52}, {"fecha": "2023-03", "valor": 48}, {"fecha": "2023-04", "valor": 61}],
        encoding={"x": {"field": "fecha", "type": "temporal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    
    "line_chart": ChartSpec(
        type="line_chart",
        title="Line Chart",
        description="Temporal evolution of a variable", 
        data=[{"date": "2023-01", "value": 45}, {"date": "2023-02", "value": 52}, {"date": "2023-03", "value": 48}, {"date": "2023-04", "value": 61}],
        encoding={"x": {"field": "date", "type": "temporal"}, "y": {"field": "value", "type": "quantitative"}},
    ),
    
    "area": ChartSpec(
        type="area",
        title="Gráfico de Área", 
        description="Magnitud de cambio a lo largo del tiempo",
        data=[{"fecha": "2023-01", "valor": 30}, {"fecha": "2023-02", "valor": 45}, {"fecha": "2023-03", "valor": 38}, {"fecha": "2023-04", "valor": 55}],
        encoding={"x": {"field": "fecha", "type": "temporal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    
    "area_chart": ChartSpec(
        type="area_chart",
        title="Area Chart",
        description="Magnitude of change over time",
        data=[{"date": "2023-01", "value": 30}, {"date": "2023-02", "value": 45}, {"date": "2023-03", "value": 38}, {"date": "2023-04", "value": 55}],
        encoding={"x": {"field": "date", "type": "temporal"}, "y": {"field": "value", "type": "quantitative"}},
    ),
    
    # Gráficos de Composición / Composition Charts
    "circular": ChartSpec(
        type="circular",
        title="Gráfico Circular",
        description="Proporciones del total en formato circular",
        data=[{"categoria": "Ventas", "valor": 45}, {"categoria": "Marketing", "valor": 25}, {"categoria": "Operaciones", "valor": 20}, {"categoria": "Otros", "valor": 10}],
        encoding={"theta": {"field": "valor", "type": "quantitative"}, "color": {"field": "categoria", "type": "nominal"}},
    ),
    
    "pie_chart": ChartSpec(
        type="pie_chart",
        title="Pie Chart", 
        description="Total proportions in circular format",
        data=[{"category": "Sales", "value": 45}, {"category": "Marketing", "value": 25}, {"category": "Operations", "value": 20}, {"category": "Other", "value": 10}],
        encoding={"theta": {"field": "value", "type": "quantitative"}, "color": {"field": "category", "type": "nominal"}},
    ),
    
    "dona": ChartSpec(
        type="dona",
        title="Gráfico de Dona",
        description="Variante del gráfico circular con centro hueco",
        data=[{"categoria": "Desktop", "valor": 60}, {"categoria": "Mobile", "valor": 35}, {"categoria": "Tablet", "valor": 5}],
        encoding={"theta": {"field": "valor", "type": "quantitative"}, "color": {"field": "categoria", "type": "nominal"}},
        options={"innerRadius": 50},
    ),
    
    "donut_chart": ChartSpec(
        type="donut_chart",
        title="Donut Chart",
        description="Variant of pie chart with hollow center",
        data=[{"category": "Desktop", "value": 60}, {"category": "Mobile", "value": 35}, {"category": "Tablet", "value": 5}],
        encoding={"theta": {"field": "value", "type": "quantitative"}, "color": {"field": "category", "type": "nominal"}},
        options={"innerRadius": 50},
    ),
    
    # Análisis de Distribución / Distribution Analysis
    "histograma": ChartSpec(
        type="histograma",
        title="Histograma",
        description="Distribución de frecuencias de una variable",
        data=[{"valor": 12}, {"valor": 15}, {"valor": 18}, {"valor": 14}, {"valor": 16}, {"valor": 13}, {"valor": 17}, {"valor": 19}],
        encoding={"x": {"field": "valor", "bin": True, "type": "quantitative"}},
    ),
    
    "histogram": ChartSpec(
        type="histogram",
        title="Histogram",
        description="Frequency distribution of a variable",
        data=[{"value": 12}, {"value": 15}, {"value": 18}, {"value": 14}, {"value": 16}, {"value": 13}, {"value": 17}, {"value": 19}],
        encoding={"x": {"field": "value", "bin": True, "type": "quantitative"}},
    ),
    
    # Análisis de Correlación / Correlation Analysis
    "dispersion": ChartSpec(
        type="dispersion",
        title="Gráfico de Dispersión",
        description="Relación entre dos variables continuas",
        data=[{"x": 10, "y": 15}, {"x": 15, "y": 22}, {"x": 20, "y": 18}, {"x": 25, "y": 30}, {"x": 30, "y": 25}],
        encoding={"x": {"field": "x", "type": "quantitative"}, "y": {"field": "y", "type": "quantitative"}},
    ),
    
    "scatter_plot": ChartSpec(
        type="scatter_plot",
        title="Scatter Plot",
        description="Relationship between two continuous variables",
        data=[{"x": 10, "y": 15}, {"x": 15, "y": 22}, {"x": 20, "y": 18}, {"x": 25, "y": 30}, {"x": 30, "y": 25}],
        encoding={"x": {"field": "x", "type": "quantitative"}, "y": {"field": "y", "type": "quantitative"}},
    ),
    
    "burbujas": ChartSpec(
        type="burbujas", 
        title="Gráfico de Burbujas",
        description="Tres dimensiones de datos con tamaño de burbuja",
        data=[{"x": 10, "y": 15, "tamaño": 20}, {"x": 20, "y": 25, "tamaño": 30}, {"x": 15, "y": 20, "tamaño": 25}],
        encoding={"x": {"field": "x", "type": "quantitative"}, "y": {"field": "y", "type": "quantitative"}, "size": {"field": "tamaño", "type": "quantitative"}},
    ),
    
    "bubble_chart": ChartSpec(
        type="bubble_chart",
        title="Bubble Chart", 
        description="Three data dimensions with bubble size",
        data=[{"x": 10, "y": 15, "size": 20}, {"x": 20, "y": 25, "size": 30}, {"x": 15, "y": 20, "size": 25}],
        encoding={"x": {"field": "x", "type": "quantitative"}, "y": {"field": "y", "type": "quantitative"}, "size": {"field": "size", "type": "quantitative"}},
    ),
    
    # Visualizaciones Avanzadas / Advanced Visualizations
    "mapa_calor": ChartSpec(
        type="mapa_calor",
        title="Mapa de Calor",
        description="Intensidad de valores en formato matriz",
        data=[{"x": "Lun", "y": "9:00", "valor": 3}, {"x": "Lun", "y": "10:00", "valor": 7}, {"x": "Mar", "y": "9:00", "valor": 5}],
        encoding={"x": {"field": "x", "type": "nominal"}, "y": {"field": "y", "type": "nominal"}, "color": {"field": "valor", "type": "quantitative"}},
    ),
    
    "heatmap": ChartSpec(
        type="heatmap",
        title="Heatmap",
        description="Value intensity in matrix format", 
        data=[{"x": "Mon", "y": "9:00", "value": 3}, {"x": "Mon", "y": "10:00", "value": 7}, {"x": "Tue", "y": "9:00", "value": 5}],
        encoding={"x": {"field": "x", "type": "nominal"}, "y": {"field": "y", "type": "nominal"}, "color": {"field": "value", "type": "quantitative"}},
    ),
    
    "radar": ChartSpec(
        type="radar",
        title="Gráfico Radar",
        description="Múltiples variables en disposición radial",
        data=[{"categoria": "Velocidad", "valor": 8}, {"categoria": "Potencia", "valor": 6}, {"categoria": "Eficiencia", "valor": 9}],
        encoding={"theta": {"field": "categoria", "type": "nominal"}, "radius": {"field": "valor", "type": "quantitative"}},
    ),
    
    "radar_chart": ChartSpec(
        type="radar_chart",
        title="Radar Chart",
        description="Multiple variables in radial layout",
        data=[{"category": "Speed", "value": 8}, {"category": "Power", "value": 6}, {"category": "Efficiency", "value": 9}],
        encoding={"theta": {"field": "category", "type": "nominal"}, "radius": {"field": "value", "type": "quantitative"}},
    ),

    # Espiral / Spiral (Escalera de caracol)
    "espiral": ChartSpec(
        type="espiral",
        title="Gráfico Espiral (Escalera de Caracol)",
        description="Visualización en forma de espiral con radio creciente",
        data=[
            {"angulo": 0, "radio": 10, "valor": 5},
            {"angulo": 30, "radio": 12, "valor": 8},
            {"angulo": 60, "radio": 15, "valor": 12},
            {"angulo": 90, "radio": 18, "valor": 16},
            {"angulo": 120, "radio": 21, "valor": 20},
            {"angulo": 150, "radio": 24, "valor": 24},
            {"angulo": 180, "radio": 27, "valor": 28},
            {"angulo": 210, "radio": 30, "valor": 32},
            {"angulo": 240, "radio": 33, "valor": 36},
            {"angulo": 270, "radio": 36, "valor": 40},
            {"angulo": 300, "radio": 39, "valor": 44},
            {"angulo": 330, "radio": 42, "valor": 48}
        ],
        encoding={
            "theta": {"field": "angulo", "type": "quantitative"},
            "radius": {"field": "radio", "type": "quantitative"},
            "color": {"field": "valor", "type": "quantitative"}
        },
    ),

    "spiral_chart": ChartSpec(
        type="spiral_chart",
        title="Spiral Chart (Staircase)",
        description="Spiral-shaped visualization with increasing radius",
        data=[
            {"angle": 0, "radius": 10, "value": 5},
            {"angle": 30, "radius": 12, "value": 8},
            {"angle": 60, "radius": 15, "value": 12},
            {"angle": 90, "radius": 18, "value": 16},
            {"angle": 120, "radius": 21, "value": 20},
            {"angle": 150, "radius": 24, "value": 24},
            {"angle": 180, "radius": 27, "value": 28},
            {"angle": 210, "radius": 30, "value": 32},
            {"angle": 240, "radius": 33, "value": 36},
            {"angle": 270, "radius": 36, "value": 40},
            {"angle": 300, "radius": 39, "value": 44},
            {"angle": 330, "radius": 42, "value": 48}
        ],
        encoding={
            "theta": {"field": "angle", "type": "quantitative"},
            "radius": {"field": "radius", "type": "quantitative"},
            "color": {"field": "value", "type": "quantitative"}
        },
    ),
    
    "kpi": ChartSpec(
        type="kpi",
        title="Tarjeta KPI",
        description="Indicador clave de rendimiento",
        data=[{"indicador": "Ventas Totales", "valor": 1250000, "meta": 1000000}],
        encoding={"value": {"field": "valor", "type": "quantitative"}, "target": {"field": "meta", "type": "quantitative"}},
    ),
    
    "kpi_card": ChartSpec(
        type="kpi_card",
        title="KPI Card",
        description="Key Performance Indicator card",
        data=[{"indicator": "Total Sales", "value": 1250000, "target": 1000000}],
        encoding={"value": {"field": "value", "type": "quantitative"}, "target": {"field": "target", "type": "quantitative"}},
    ),
    
    # Análisis de Flujo y Proceso / Flow and Process Analysis  
    "embudo": ChartSpec(
        type="embudo",
        title="Gráfico de Embudo",
        description="Procesos secuenciales con conversión",
        data=[{"etapa": "Visitantes", "valor": 1000}, {"etapa": "Interesados", "valor": 400}, {"etapa": "Clientes", "valor": 100}],
        encoding={"x": {"field": "etapa", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    
    "funnel_chart": ChartSpec(
        type="funnel_chart", 
        title="Funnel Chart",
        description="Sequential processes with conversion",
        data=[{"stage": "Visitors", "value": 1000}, {"stage": "Interested", "value": 400}, {"stage": "Customers", "value": 100}],
        encoding={"x": {"field": "stage", "type": "nominal"}, "y": {"field": "value", "type": "quantitative"}},
    ),
    
    "cascada": ChartSpec(
        type="cascada",
        title="Gráfico de Cascada",
        description="Cambios acumulativos paso a paso",
        data=[{"categoria": "Inicio", "valor": 100}, {"categoria": "Aumento", "valor": 20}, {"categoria": "Reducción", "valor": -15}],
        encoding={"x": {"field": "categoria", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    
    "waterfall_chart": ChartSpec(
        type="waterfall_chart",
        title="Waterfall Chart",
        description="Step-by-step cumulative changes", 
        data=[{"category": "Start", "value": 100}, {"category": "Increase", "value": 20}, {"category": "Decrease", "value": -15}],
        encoding={"x": {"field": "category", "type": "nominal"}, "y": {"field": "value", "type": "quantitative"}},
    ),
    
    # Ejemplos adicionales para completar compatibilidad
    "treemap": ChartSpec(
        type="treemap",
        title="Treemap", 
        description="Jerarquías y proporciones anidadas",
        data=[{"categoria": "Tecnología", "valor": 45}, {"categoria": "Salud", "valor": 30}, {"categoria": "Finanzas", "valor": 25}],
        encoding={"color": {"field": "categoria", "type": "nominal"}, "size": {"field": "valor", "type": "quantitative"}},
    ),
    
    "gantt": ChartSpec(
        type="gantt",
        title="Gráfico de Gantt",
        description="Cronograma de proyectos y tareas",
        data=[{"tarea": "Planificación", "inicio": "2023-01-01", "fin": "2023-01-15"}],
        encoding={"x": {"field": "inicio", "type": "temporal"}, "x2": {"field": "fin", "type": "temporal"}, "y": {"field": "tarea", "type": "nominal"}},
    ),
    
    # Gráficos de Lazo / Loop Charts
    "lazo": ChartSpec(
        type="lazo",
        title="Gráfico de Lazo",
        description="Visualización de procesos cíclicos o flujos circulares",
        data=[
            {"etapa": "Inicio", "siguiente": "Proceso", "valor": 100},
            {"etapa": "Proceso", "siguiente": "Evaluación", "valor": 85},
            {"etapa": "Evaluación", "siguiente": "Decisión", "valor": 70},
            {"etapa": "Decisión", "siguiente": "Inicio", "valor": 55}
        ],
        encoding={"x": {"field": "etapa", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}, "detail": {"field": "siguiente", "type": "nominal"}},
    ),
    
    "loop_chart": ChartSpec(
        type="loop_chart",
        title="Loop Chart", 
        description="Visualization of cyclical processes or circular flows",
        data=[
            {"stage": "Start", "next": "Process", "value": 100},
            {"stage": "Process", "next": "Evaluation", "value": 85},
            {"stage": "Evaluation", "next": "Decision", "value": 70},
            {"stage": "Decision", "next": "Start", "value": 55}
        ],
        encoding={"x": {"field": "stage", "type": "nominal"}, "y": {"field": "value", "type": "quantitative"}, "detail": {"field": "next", "type": "nominal"}},
    ),
    
    "lazo_circular": ChartSpec(
        type="lazo_circular",
        title="Gráfico de Lazo Circular",
        description="Proceso cíclico representado en forma circular",
        data=[
            {"paso": "Diseño", "angulo": 0, "radio": 80, "duracion": 5},
            {"paso": "Desarrollo", "angulo": 90, "radio": 85, "duracion": 10},
            {"paso": "Pruebas", "angulo": 180, "radio": 75, "duracion": 3},
            {"paso": "Despliegue", "angulo": 270, "radio": 90, "duracion": 2}
        ],
        encoding={"theta": {"field": "angulo", "type": "quantitative"}, "radius": {"field": "radio", "type": "quantitative"}, "color": {"field": "paso", "type": "nominal"}},
    ),
    
    "circular_loop_chart": ChartSpec(
        type="circular_loop_chart",
        title="Circular Loop Chart",
        description="Cyclical process represented in circular form", 
        data=[
            {"step": "Design", "angle": 0, "radius": 80, "duration": 5},
            {"step": "Development", "angle": 90, "radius": 85, "duration": 10},
            {"step": "Testing", "angle": 180, "radius": 75, "duration": 3},
            {"step": "Deploy", "angle": 270, "radius": 90, "duration": 2}
        ],
        encoding={"theta": {"field": "angle", "type": "quantitative"}, "radius": {"field": "radius", "type": "quantitative"}, "color": {"field": "step", "type": "nominal"}},
    ),
    
    "lazo_proceso": ChartSpec(
        type="lazo_proceso",
        title="Gráfico de Lazo de Proceso",
        description="Flujo de proceso con retroalimentación y ciclos",
        data=[
            {"actividad": "Entrada", "tipo": "input", "x": 0, "y": 0, "conexion": "Procesamiento"},
            {"actividad": "Procesamiento", "tipo": "process", "x": 1, "y": 0, "conexion": "Salida"},
            {"actividad": "Salida", "tipo": "output", "x": 2, "y": 0, "conexion": "Retroalimentación"},
            {"actividad": "Retroalimentación", "tipo": "feedback", "x": 1, "y": -1, "conexion": "Entrada"}
        ],
        encoding={"x": {"field": "x", "type": "quantitative"}, "y": {"field": "y", "type": "quantitative"}, "color": {"field": "tipo", "type": "nominal"}, "detail": {"field": "conexion", "type": "nominal"}},
    ),
    
    "process_loop_chart": ChartSpec(
        type="process_loop_chart", 
        title="Process Loop Chart",
        description="Process flow with feedback and cycles",
        data=[
            {"activity": "Input", "type": "input", "x": 0, "y": 0, "connection": "Processing"},
            {"activity": "Processing", "type": "process", "x": 1, "y": 0, "connection": "Output"},
            {"activity": "Output", "type": "output", "x": 2, "y": 0, "connection": "Feedback"},
            {"activity": "Feedback", "type": "feedback", "x": 1, "y": -1, "connection": "Input"}
        ],
        encoding={"x": {"field": "x", "type": "quantitative"}, "y": {"field": "y", "type": "quantitative"}, "color": {"field": "type", "type": "nominal"}, "detail": {"field": "connection", "type": "nominal"}},
    ),
    
    "lazo_flujo": ChartSpec(
        type="lazo_flujo",
        title="Gráfico de Lazo de Flujo", 
        description="Flujo continuo con recirculación y bucles",
        data=[
            {"nodo": "Origen", "flujo_salida": 120, "flujo_entrada": 0, "posicion": 1},
            {"nodo": "Proceso A", "flujo_salida": 100, "flujo_entrada": 120, "posicion": 2},
            {"nodo": "Proceso B", "flujo_salida": 80, "flujo_entrada": 100, "posicion": 3},
            {"nodo": "Recirculación", "flujo_salida": 20, "flujo_entrada": 80, "posicion": 4}
        ],
        encoding={"x": {"field": "posicion", "type": "ordinal"}, "y": {"field": "flujo_salida", "type": "quantitative"}, "y2": {"field": "flujo_entrada", "type": "quantitative"}},
    ),
    
    "flow_loop_chart": ChartSpec(
        type="flow_loop_chart",
        title="Flow Loop Chart",
        description="Continuous flow with recirculation and loops",
        data=[
            {"node": "Source", "outflow": 120, "inflow": 0, "position": 1},
            {"node": "Process A", "outflow": 100, "inflow": 120, "position": 2}, 
            {"node": "Process B", "outflow": 80, "inflow": 100, "position": 3},
            {"node": "Recirculation", "outflow": 20, "inflow": 80, "position": 4}
        ],
        encoding={"x": {"field": "position", "type": "ordinal"}, "y": {"field": "outflow", "type": "quantitative"}, "y2": {"field": "inflow", "type": "quantitative"}},
    )
}

"""
Catálogo de tipos de gráficos soportados - Español e Inglés.
Lista completa para generación de objetos visuales locales para Power BI y Tableau.
"""

CHART_TYPES = [
    # Gráficos Básicos Comunes / Common Basic Charts
    'barras_vertical', 'bar_chart_vertical',
    'barras_horizontal', 'bar_chart_horizontal', 
    'columnas', 'column_chart',
    'barras_agrupadas', 'grouped_bar_chart',
    'barras_apiladas', 'stacked_bar_chart',
    
    # Gráficos de Tendencias / Trend Charts
    'lineas', 'line_chart',
    'area', 'area_chart', 
    'area_apilada', 'stacked_area_chart',
    
    # Gráficos de Composición / Composition Charts
    'circular', 'pie_chart',
    'dona', 'donut_chart',
    'treemap', 'treemap_chart',
    'waffle', 'waffle_chart',
    
    # Análisis de Distribución / Distribution Analysis
    'histograma', 'histogram',
    'caja', 'box_plot',
    'violin', 'violin_plot',
    'densidad', 'density_plot',
    
    # Análisis de Correlación / Correlation Analysis  
    'dispersion', 'scatter_plot',
    'burbujas', 'bubble_chart',
    'matriz_correlacion', 'correlation_matrix',
    
    # Mapas y Geoespaciales / Maps and Geospatial
    'mapa_coropletico', 'choropleth_map',
    'mapa_puntos', 'point_map', 
    'mapa_calor_geografico', 'geographic_heatmap',
    
    # Análisis de Flujo y Proceso / Flow and Process Analysis
    'embudo', 'funnel_chart',
    'sankey', 'sankey_diagram',
    'cascada', 'waterfall_chart',
    'lazo', 'loop_chart',
    'lazo_circular', 'circular_loop_chart',
    'lazo_proceso', 'process_loop_chart',
    'lazo_flujo', 'flow_loop_chart',
    
    # Visualizaciones Avanzadas / Advanced Visualizations
    'mapa_calor', 'heatmap',
    'radar', 'radar_chart',
    'gantt', 'gantt_chart',
    'kpi', 'kpi_card',
    'espiral', 'spiral_chart',
    
    # Gráficos Específicos R/ggplot2 / R/ggplot2 Specific
    'puntos', 'geom_point',
    'linea_tendencia', 'geom_smooth',
    'poligono', 'geom_polygon',
    
    # Categorías de Visualización / Visualization Categories
    'correlacion', 'correlation',
    'desviacion', 'deviation', 
    'ranking', 'ranking',
    'distribucion', 'distribution',
    'composicion', 'composition',
    'cambio', 'change',
    'grupos', 'groups',
    'espacial', 'spatial'
]

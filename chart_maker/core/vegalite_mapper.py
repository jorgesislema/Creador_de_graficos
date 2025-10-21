"""
Mapper de ChartSpec canónico → Vega-Lite (v6) para vista previa.

Nota: Este mapper cubre los casos más comunes (bar, line, area, scatter/bubble,
pie/donut, heatmap, table básica) y usa degradaciones simples para otros tipos.
"""

from typing import Dict, Any


def chartspec_to_vegalite(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Convierte una especificación ChartSpec canónica a una Vega-Lite v6 básica."""
    chart_type = spec.get('type', 'bar')
    data = spec.get('data')
    encoding = spec.get('encoding', {})
    options = spec.get('options', {})

    vl: Dict[str, Any] = {
        "$schema": "https://vega.github.io/schema/vega-lite/v6.json",
        "mark": _map_mark(chart_type, options),
        "width": spec.get('width', 400),
        "height": spec.get('height', 300),
    }

    # Título / descripción
    if spec.get('title'):
        vl['title'] = spec['title']
    if spec.get('description'):
        vl['description'] = spec['description']

    # Datos: soporta lista de dicts o dict con values/url
    if isinstance(data, list):
        vl['data'] = {"values": data}
    elif isinstance(data, dict):
        # si ya viene como {values: [...] } ó {url: '...'}
        vl['data'] = data
    else:
        vl['data'] = {"values": []}

    # Encoding
    vl['encoding'] = _map_encoding(chart_type, encoding)

    # Stacking y otras opciones básicas
    stacking = options.get('stacking')
    if stacking in ('stack', 'normalize', 'none'):
        # aplicar stacking a mark si procede (para bar/area)
        if isinstance(vl['mark'], dict) and chart_type in ('bar', 'area'):
            if stacking == 'none':
                vl['mark']['stack'] = None
            else:
                vl['mark']['stack'] = stacking

    # Líneas de referencia
    ref_lines = options.get('referenceLines') or []
    if ref_lines:
        vl['layer'] = [
            {k: v for k, v in vl.items() if k not in ('layer',)}
        ]
        for rl in ref_lines:
            channel = rl.get('channel')
            value = rl.get('value')
            label = rl.get('label')
            if channel in ('y', 'x') and value is not None:
                # Regla simple
                rule = {
                    "mark": {"type": "rule", "color": "#d32f2f"},
                    "encoding": {
                        channel: {"datum": value}
                    }
                }
                if label and channel == 'y':
                    rule['encoding']['tooltip'] = {"value": label}
                vl['layer'].append(rule)

    return vl


def _map_mark(chart_type: str, options: Dict[str, Any]) -> Any:
    # mapeo básico de tipo - español e inglés
    mark_map = {
        # Barras / Bars
        'barras_vertical': 'bar',
        'bar_chart_vertical': 'bar',
        'barras_horizontal': 'bar',
        'bar_chart_horizontal': 'bar',
        'columnas': 'bar',
        'column_chart': 'bar',
        'barras_agrupadas': 'bar',
        'grouped_bar_chart': 'bar',
        'barras_apiladas': 'bar',
        'stacked_bar_chart': 'bar',
        # Líneas y áreas / Lines and areas
        'lineas': 'line',
        'line_chart': 'line',
        'area': 'area',
        'area_chart': 'area',
        'area_apilada': 'area',
        'stacked_area_chart': 'area',
        # Composición / Composition
        'circular': 'arc',
        'pie_chart': 'arc',
        'dona': {'type': 'arc', 'innerRadius': options.get('innerRadius', 50)},
        'donut_chart': {'type': 'arc', 'innerRadius': options.get('innerRadius', 50)},
        'treemap': 'rect',
        'treemap_chart': 'rect',
        # Distribución / Distribution
        'histograma': 'bar',
        'histogram': 'bar',
        'caja': 'boxplot',
        'box_plot': 'boxplot',
        'violin': 'area',
        'violin_plot': 'area',
        'densidad': 'area',
        'density_plot': 'area',
        # Correlación / Correlation
        'dispersion': 'point',
        'scatter_plot': 'point',
        'burbujas': {'type': 'point'},
        'bubble_chart': {'type': 'point'},
        'matriz_correlacion': 'rect',
        'correlation_matrix': 'rect',
        # Mapas / Maps
        'mapa_coropletico': 'geoshape',
        'choropleth_map': 'geoshape',
        'mapa_puntos': 'point',
        'point_map': 'point',
        'mapa_calor_geografico': 'rect',
        'geographic_heatmap': 'rect',
        # Flujo / Flow
        'embudo': 'bar',
        'funnel_chart': 'bar',
        'sankey': 'rect',
        'sankey_diagram': 'rect',
        'cascada': 'bar',
        'waterfall_chart': 'bar',
        'lazo': 'line',
        'loop_chart': 'line',
        'lazo_circular': 'arc',
        'circular_loop_chart': 'arc',
        'lazo_proceso': 'point',
        'process_loop_chart': 'point',
        'lazo_flujo': 'area',
        'flow_loop_chart': 'area',
        # Avanzados / Advanced
        'mapa_calor': 'rect',
        'heatmap': 'rect',
        'radar': 'line',
        'radar_chart': 'line',
        'gantt': 'bar',
        'gantt_chart': 'bar',
        'kpi': 'text',
        'kpi_card': 'text',
        # R/ggplot2
        'puntos': 'point',
        'geom_point': 'point',
        'linea_tendencia': 'line',
        'geom_smooth': 'line',
        'poligono': 'area',
        'geom_polygon': 'area',
        # Categorías
        'correlacion': 'point',
        'correlation': 'point',
        'desviacion': 'bar',
        'deviation': 'bar',
        'ranking': 'bar',
        'distribucion': 'bar',
        'distribution': 'bar',
        'composicion': 'arc',
        'composition': 'arc',
        'cambio': 'line',
        'change': 'line',
        'grupos': 'bar',
        'groups': 'bar',
        'espacial': 'point',
        'spatial': 'point'
    }
    return mark_map.get(chart_type, 'point')


def _map_encoding(chart_type: str, enc: Dict[str, Any]) -> Dict[str, Any]:
    # Decodificación directa de canales canónicos → Vega-Lite
    vl_enc: Dict[str, Any] = {}

    def _field(channel: str, fallback_field: str = None, fallback_type: str = None):
        fd = enc.get(channel)
        if isinstance(fd, dict) and 'field' in fd:
            m = {'field': fd['field']}
            if 'type' in fd:
                m['type'] = _map_type(fd['type'])
            if 'aggregate' in fd:
                m['aggregate'] = fd['aggregate']
            if 'bin' in fd:
                m['bin'] = fd['bin']
            return m
        if fallback_field:
            m = {'field': fallback_field}
            if fallback_type:
                m['type'] = _map_type(fallback_type)
            return m
        return None

    # comunes
    x = _field('x')
    y = _field('y')
    x2 = _field('x2')
    y2 = _field('y2')
    color = _field('color')
    size = _field('size')
    shape = _field('shape')

    if x:
        vl_enc['x'] = x
    if y:
        vl_enc['y'] = y
    if x2:
        vl_enc['x2'] = x2
    if y2:
        vl_enc['y2'] = y2
    if color:
        vl_enc['color'] = color
    if size:
        # si es bubble, usar size
        vl_enc['size'] = size
    if shape:
        vl_enc['shape'] = shape

    # canales especiales
    if chart_type in ('pie', 'donut'):
        theta = _field('theta', fallback_field='value', fallback_type='quantitative')
        if theta:
            vl_enc['theta'] = theta
        if not color:
            # color por categoría si existe
            cat = _field('color', fallback_field='category', fallback_type='nominal')
            if cat:
                vl_enc['color'] = cat

    if chart_type == 'heatmap':
        if 'color' not in vl_enc:
            vl_enc['color'] = {'field': 'value', 'type': 'quantitative'}

    return vl_enc


def _map_type(t: str) -> str:
    # normaliza tipos a vega-lite
    mapping = {
        'quantitative': 'quantitative',
        'temporal': 'temporal',
        'ordinal': 'ordinal',
        'nominal': 'nominal',
        # alias
        'number': 'quantitative',
        'string': 'nominal',
        'date': 'temporal',
    }
    return mapping.get(t, t)

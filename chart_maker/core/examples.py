# examples.py
# Ejemplos de especificaciones ChartSpec para cada tipo de gráfico
from .spec import ChartSpec

EXAMPLES = {
    "bar": ChartSpec(
        type="bar",
        data=[{"categoria": "A", "valor": 10}, {"categoria": "B", "valor": 20}],
        encoding={"x": {"field": "categoria", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    "stacked_bar": ChartSpec(
        type="bar",
        data=[{"categoria": "A", "grupo": "X", "valor": 10}, {"categoria": "A", "grupo": "Y", "valor": 5}],
        encoding={"x": {"field": "categoria", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}, "color": {"field": "grupo", "type": "nominal"}},
    ),
    "line": ChartSpec(
        type="line",
        data=[{"fecha": "2023-01", "valor": 5}, {"fecha": "2023-02", "valor": 15}],
        encoding={"x": {"field": "fecha", "type": "temporal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    "area": ChartSpec(
        type="area",
        data=[{"fecha": "2023-01", "valor": 5}, {"fecha": "2023-02", "valor": 15}],
        encoding={"x": {"field": "fecha", "type": "temporal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    "stacked_area": ChartSpec(
        type="area",
        data=[{"fecha": "2023-01", "grupo": "A", "valor": 5}, {"fecha": "2023-01", "grupo": "B", "valor": 3}],
        encoding={"x": {"field": "fecha", "type": "temporal"}, "y": {"field": "valor", "type": "quantitative"}, "color": {"field": "grupo", "type": "nominal"}},
    ),
    "combo": ChartSpec(
        type="bar",
        data=[{"categoria": "A", "valor": 10, "valor2": 5}],
        encoding={"x": {"field": "categoria", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}, "y2": {"field": "valor2", "type": "quantitative"}},
    ),
    "scatter": ChartSpec(
        type="scatter",
        data=[{"x": 1, "y": 2}, {"x": 2, "y": 3}],
        encoding={"x": {"field": "x", "type": "quantitative"}, "y": {"field": "y", "type": "quantitative"}},
    ),
    "bubble": ChartSpec(
        type="bubble",
        data=[{"x": 1, "y": 2, "size": 10}, {"x": 2, "y": 3, "size": 20}],
        encoding={"x": {"field": "x", "type": "quantitative"}, "y": {"field": "y", "type": "quantitative"}, "size": {"field": "size", "type": "quantitative"}},
    ),
    "table": ChartSpec(
        type="table",
        data=[{"col1": "A", "col2": 1}, {"col1": "B", "col2": 2}],
        encoding={},
    ),
    "matrix": ChartSpec(
        type="matrix",
        data=[{"row": "A", "col": "X", "valor": 5}],
        encoding={"row": {"field": "row", "type": "nominal"}, "column": {"field": "col", "type": "nominal"}, "value": {"field": "valor", "type": "quantitative"}},
    ),
    "kpi": ChartSpec(
        type="kpi",
        data=[{"valor": 100}],
        encoding={"value": {"field": "valor", "type": "quantitative"}},
    ),
    "gauge": ChartSpec(
        type="gauge",
        data=[{"valor": 70}],
        encoding={"value": {"field": "valor", "type": "quantitative"}},
    ),
    "treemap": ChartSpec(
        type="treemap",
        data=[{"categoria": "A", "valor": 10}, {"categoria": "B", "valor": 20}],
        encoding={"color": {"field": "categoria", "type": "nominal"}, "size": {"field": "valor", "type": "quantitative"}},
    ),
    "pie": ChartSpec(
        type="pie",
        data=[{"categoria": "A", "valor": 30}, {"categoria": "B", "valor": 70}],
        encoding={"theta": {"field": "valor", "type": "quantitative"}, "color": {"field": "categoria", "type": "nominal"}},
    ),
    "donut": ChartSpec(
        type="donut",
        data=[{"categoria": "A", "valor": 30}, {"categoria": "B", "valor": 70}],
        encoding={"theta": {"field": "valor", "type": "quantitative"}, "color": {"field": "categoria", "type": "nominal"}},
        options={"innerRadius": 50},
    ),
    "histogram": ChartSpec(
        type="bar",
        data=[{"valor": 1}, {"valor": 2}, {"valor": 2}, {"valor": 3}],
        encoding={"x": {"field": "valor", "bin": True, "type": "quantitative"}},
    ),
    "boxplot": ChartSpec(
        type="boxplot",
        data=[{"grupo": "A", "valor": 10}, {"grupo": "A", "valor": 20}],
        encoding={"x": {"field": "grupo", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    "violin": ChartSpec(
        type="violin",
        data=[{"grupo": "A", "valor": 10}, {"grupo": "A", "valor": 20}],
        encoding={"x": {"field": "grupo", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    "heatmap": ChartSpec(
        type="heatmap",
        data=[{"x": "A", "y": "B", "valor": 5}],
        encoding={"x": {"field": "x", "type": "nominal"}, "y": {"field": "y", "type": "nominal"}, "color": {"field": "valor", "type": "quantitative"}},
    ),
    "hexbin": ChartSpec(
        type="hexbin",
        data=[{"x": 1, "y": 2}],
        encoding={"x": {"field": "x", "type": "quantitative"}, "y": {"field": "y", "type": "quantitative"}},
    ),
    "waterfall": ChartSpec(
        type="waterfall",
        data=[{"categoria": "A", "valor": 10}, {"categoria": "B", "valor": -5}],
        encoding={"x": {"field": "categoria", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    "funnel": ChartSpec(
        type="funnel",
        data=[{"etapa": "A", "valor": 100}, {"etapa": "B", "valor": 60}],
        encoding={"x": {"field": "etapa", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    "bullet": ChartSpec(
        type="bullet",
        data=[{"valor": 70, "meta": 100}],
        encoding={"value": {"field": "valor", "type": "quantitative"}, "target": {"field": "meta", "type": "quantitative"}},
    ),
    "candlestick": ChartSpec(
        type="candlestick",
        data=[{"fecha": "2023-01", "open": 10, "close": 15, "high": 18, "low": 8}],
        encoding={"x": {"field": "fecha", "type": "temporal"}, "open": {"field": "open", "type": "quantitative"}, "close": {"field": "close", "type": "quantitative"}, "high": {"field": "high", "type": "quantitative"}, "low": {"field": "low", "type": "quantitative"}},
    ),
    "range_bar": ChartSpec(
        type="bar",
        data=[{"categoria": "A", "min": 5, "max": 10}],
        encoding={"x": {"field": "categoria", "type": "nominal"}, "y": {"field": "min", "type": "quantitative"}, "y2": {"field": "max", "type": "quantitative"}},
    ),
    "timeline": ChartSpec(
        type="timeline",
        data=[{"evento": "A", "inicio": "2023-01", "fin": "2023-02"}],
        encoding={"x": {"field": "inicio", "type": "temporal"}, "x2": {"field": "fin", "type": "temporal"}, "y": {"field": "evento", "type": "nominal"}},
    ),
    "gantt": ChartSpec(
        type="gantt",
        data=[{"tarea": "A", "inicio": "2023-01", "fin": "2023-02"}],
        encoding={"x": {"field": "inicio", "type": "temporal"}, "x2": {"field": "fin", "type": "temporal"}, "y": {"field": "tarea", "type": "nominal"}},
    ),
    "sankey": ChartSpec(
        type="sankey",
        data=[{"origen": "A", "destino": "B", "valor": 10}],
        encoding={"source": {"field": "origen", "type": "nominal"}, "target": {"field": "destino", "type": "nominal"}, "value": {"field": "valor", "type": "quantitative"}},
    ),
    "chord": ChartSpec(
        type="chord",
        data=[{"origen": "A", "destino": "B", "valor": 10}],
        encoding={"source": {"field": "origen", "type": "nominal"}, "target": {"field": "destino", "type": "nominal"}, "value": {"field": "valor", "type": "quantitative"}},
    ),
    "network": ChartSpec(
        type="network",
        data=[{"source": "A", "target": "B"}],
        encoding={"source": {"field": "source", "type": "nominal"}, "target": {"field": "target", "type": "nominal"}},
    ),
    "parallel": ChartSpec(
        type="parallel",
        data=[{"var1": 1, "var2": 2, "var3": 3}],
        encoding={"var1": {"field": "var1", "type": "quantitative"}, "var2": {"field": "var2", "type": "quantitative"}, "var3": {"field": "var3", "type": "quantitative"}},
    ),
    "sunburst": ChartSpec(
        type="sunburst",
        data=[{"categoria": "A", "sub": "X", "valor": 10}],
        encoding={"color": {"field": "categoria", "type": "nominal"}, "sub": {"field": "sub", "type": "nominal"}, "size": {"field": "valor", "type": "quantitative"}},
    ),
    "icicle": ChartSpec(
        type="icicle",
        data=[{"categoria": "A", "sub": "X", "valor": 10}],
        encoding={"color": {"field": "categoria", "type": "nominal"}, "sub": {"field": "sub", "type": "nominal"}, "size": {"field": "valor", "type": "quantitative"}},
    ),
    "marimekko": ChartSpec(
        type="marimekko",
        data=[{"cat1": "A", "cat2": "X", "valor": 10}],
        encoding={"x": {"field": "cat1", "type": "nominal"}, "y": {"field": "cat2", "type": "nominal"}, "size": {"field": "valor", "type": "quantitative"}},
    ),
    "radar": ChartSpec(
        type="radar",
        data=[{"categoria": "A", "valor": 10}, {"categoria": "B", "valor": 20}],
        encoding={"theta": {"field": "categoria", "type": "nominal"}, "radius": {"field": "valor", "type": "quantitative"}},
    ),
    "dumbbell": ChartSpec(
        type="dumbbell",
        data=[{"categoria": "A", "valor1": 10, "valor2": 20}],
        encoding={"x": {"field": "categoria", "type": "nominal"}, "y": {"field": "valor1", "type": "quantitative"}, "y2": {"field": "valor2", "type": "quantitative"}},
    ),
    "lollipop": ChartSpec(
        type="lollipop",
        data=[{"categoria": "A", "valor": 10}],
        encoding={"x": {"field": "categoria", "type": "nominal"}, "y": {"field": "valor", "type": "quantitative"}},
    ),
    "bump": ChartSpec(
        type="bump",
        data=[{"categoria": "A", "periodo": "2023-01", "ranking": 1}],
        encoding={"x": {"field": "periodo", "type": "temporal"}, "y": {"field": "ranking", "type": "quantitative"}, "color": {"field": "categoria", "type": "nominal"}},
    ),
    "wordcloud": ChartSpec(
        type="wordcloud",
        data=[{"text": "python", "size": 10}, {"text": "data", "size": 20}],
        encoding={"text": {"field": "text", "type": "nominal"}, "size": {"field": "size", "type": "quantitative"}},
    ),
    "map_points": ChartSpec(
        type="map_points",
        data=[{"lat": 10, "lon": 20}],
        encoding={"latitude": {"field": "lat", "type": "quantitative"}, "longitude": {"field": "lon", "type": "quantitative"}},
    ),
    "choropleth": ChartSpec(
        type="choropleth",
        data=[{"region": "A", "valor": 10}],
        encoding={"color": {"field": "valor", "type": "quantitative"}, "region": {"field": "region", "type": "nominal"}},
    ),
    "map_lines": ChartSpec(
        type="map_lines",
        data=[{"lat1": 10, "lon1": 20, "lat2": 15, "lon2": 25}],
        encoding={"latitude": {"field": "lat1", "type": "quantitative"}, "longitude": {"field": "lon1", "type": "quantitative"}, "latitude2": {"field": "lat2", "type": "quantitative"}, "longitude2": {"field": "lon2", "type": "quantitative"}},
    ),
    "decomposition_tree": ChartSpec(
        type="decomposition_tree",
        data=[{"causa": "A", "valor": 10}],
        encoding={"cause": {"field": "causa", "type": "nominal"}, "value": {"field": "valor", "type": "quantitative"}},
    ),
    "key_influencers": ChartSpec(
        type="key_influencers",
        data=[{"factor": "A", "impacto": 0.8}],
        encoding={"factor": {"field": "factor", "type": "nominal"}, "impact": {"field": "impacto", "type": "quantitative"}},
    ),
    "narrative": ChartSpec(
        type="narrative",
        data=[{"texto": "El valor aumentó"}],
        encoding={"text": {"field": "texto", "type": "nominal"}},
    ),
}

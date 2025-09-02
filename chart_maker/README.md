# Chart Maker

Creador de gráficos para análisis y ciencia de datos, con exportación a Power BI, Tableau, Looker y Looker Studio.

## Estructura

- `app/` - Interfaz gráfica y componentes
- `core/` - Especificación, transformación y validación de gráficos
- `exporters/` - Exportadores por plataforma
- `packaging/` - Utilidades para empaquetado y CLI
- `tests/` - Pruebas

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python -m chart_maker.app.main
```

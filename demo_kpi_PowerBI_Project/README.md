# Proyecto Power BI Visual - Tarjeta KPI

Este es un proyecto de desarrollo de visual personalizado para Power BI generado automáticamente por **Creador de Gráficos**.

## 📊 Información del Visual

- **Tipo de gráfico**: kpi
- **Título**: Tarjeta KPI
- **Descripción**: Indicador clave de rendimiento
- **Fecha de creación**: 2025-09-28 20:54

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
demo_kpi_PowerBI_Project/
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

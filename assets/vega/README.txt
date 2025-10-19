Coloca aquí las librerías para ejecución 100% local (sin CDN):

- vega.min.js (o vega.js)
- vega-lite.min.js (o vega-lite.js)
- vega-embed.min.js (o vega-embed.js)

Cómo obtenerlas:
1) Desde CDN y guardarlas localmente:
   - https://cdn.jsdelivr.net/npm/vega@6/build/vega.min.js
   - https://cdn.jsdelivr.net/npm/vega-lite@6/build/vega-lite.min.js
   - https://cdn.jsdelivr.net/npm/vega-embed@7/build/vega-embed.min.js

2) O instalando con npm en otra máquina y copiando los archivos build a esta carpeta.

Nota:
- La vista previa en el navegador y la exportación HTML buscarán primero estos archivos.
- Si no se encuentran, se mostrará un aviso y no se intentará renderizar para evitar llamadas a Internet.

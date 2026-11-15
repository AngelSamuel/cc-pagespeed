# Changelog

Todos los cambios relevantes de la skill. El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y las versiones siguen [SemVer](https://semver.org/lang/es/).

## [2.0.1] - 2026-11-15

### Añadido
- Licencia MIT.

## [2.0.0] - 2026-11-15

### Cambiado
- La medición usa solo **Lighthouse 13.6.0 en local**. Es gratis, no necesita API key y también mide `localhost`.
- Informe rediseñado (`references/report-template.md`): veredicto, puntuaciones y Core Web Vitals con iconos, peso de la página con barras, plan de acción con prioridad, dificultad, tiempo y responsable, fichas por arreglo, sección "Lo que no haríamos" y glosario.
- La prioridad se decide por impacto real y esfuerzo, con criterios explícitos, y no por el orden de Lighthouse. Los arreglos se numeran por prioridad, incluidos los de servidor.
- Las unidades de `summary.json` pasan a ser KiB (`totalKiB`, `kibByType`, `kib`).

### Añadido
- En `summary.json`: valores exactos de las métricas, peso por tipo de recurso, peticiones más pesadas (con su prioridad y protocolo), auditorías que pasan, detalle de contraste, elemento LCP y sus fases, texto de los errores de consola y tamaño mostrado de las imágenes.
- Enlace al análisis oficial de PageSpeed Insights para consultar los datos de usuarios reales.
- Modo "solo URL": cuando no hay código, la skill cita las líneas del HTML publicado y da instrucciones para el servidor detectado.
- Informe de ejemplo en `examples/`.

### Eliminado
- La integración con la API de PageSpeed Insights y la variable `PAGESPEED_API_KEY`.

## [1.0.0] - 2026-11-15

### Añadido
- Primera versión: medición con la API de PageSpeed Insights (con Lighthouse local como alternativa), informe priorizado y aplicación de los arreglos que se elijan.

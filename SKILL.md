---
name: pagespeed-audit
description: Analiza el rendimiento de una web con Lighthouse, el motor de Google PageSpeed Insights (rendimiento, accesibilidad, buenas prácticas y SEO, en móvil y escritorio), genera un informe visual y priorizado (iconos, prioridad, dificultad, tiempo estimado) y, cuando la persona elige qué arreglos quiere, los aplica en el código del proyecto local y vuelve a medir. Úsala siempre que alguien pida analizar u optimizar la velocidad de una URL, mencione PageSpeed, Lighthouse, Core Web Vitals, LCP, INP, CLS o la nota de rendimiento, o diga que su web "va lenta" o "carga mal en móvil", aunque no nombre la herramienta.
---

# PageSpeed Audit

Convierte una URL en un informe de PageSpeed entendible y en cambios reales en el código. Tiene tres fases, y entre la segunda y la tercera la persona decide:

1. **Medir**: el script ejecuta Lighthouse en local y deja un resumen.
2. **Informar**: escribes un informe priorizado y relacionas cada problema con los archivos del proyecto.
3. **Aplicar**: solo los arreglos que la persona elija. Después se vuelve a medir.

La persona puede querer solo el informe, o solo algunos arreglos. Las dos cosas son resultados válidos: nunca apliques cambios que no se han elegido.

## 1. Medir

Ejecuta el script incluido (está en la carpeta de esta skill):

```bash
python3 <carpeta-de-la-skill>/scripts/run_pagespeed.py <URL> --out ./pagespeed-report
```

Por defecto analiza móvil y escritorio. Puede tardar 1-2 minutos: lánzalo y espera.

**Motor.** El script usa **Lighthouse**, el mismo motor que Google PageSpeed Insights, ejecutado en este equipo con `npx`. Es gratis, no necesita API key ni cuenta, y también puede medir `localhost`. Necesita Node.js y Google Chrome. Si faltan, explica cómo instalarlos (https://nodejs.org y Chrome) y, mientras tanto, ofrece analizar la web a mano en https://pagespeed.web.dev.

Lighthouse local da datos de laboratorio, no de usuarios reales. Los datos de usuarios reales (CrUX, los que Google usa para posicionar) se consultan gratis en la web oficial de PageSpeed Insights: el resumen trae el enlace directo en `pagespeedWebUrl`, y el informe lo incluye para que la persona pueda contrastarlo.

## 2. Informar

Lee `pagespeed-report/summary.json`. Para cada estrategia contiene:

- `scores`: nota de 0 a 100 por categoría.
- `lab`: métricas de laboratorio.
- `page`: peso total en KB, número de peticiones, KB por tipo de recurso y las peticiones más pesadas, con su prioridad y protocolo (para la sección "Peso de la página").
- `passed`: auditorías que ya están bien. Sirven para descartar causas y para decir qué funciona.
- `lab`: incluye `numericValue` (valor exacto). Clasifica con él, no con el texto redondeado.
- `lcp`: qué elemento es el LCP (selector, fragmento de HTML y tamaño mostrado) y el reparto de su tiempo por fases (TTFB, retraso de carga, descarga, renderizado). Las fases vienen de la carga sin limitar, así que úsalas como proporción: dicen si el problema está en el servidor, en el descubrimiento o en el peso.
- `issues`: auditorías por mejorar en cada categoría, con el ahorro estimado (`metricSavings`, `overallSavingsMs/Bytes`) y los elementos afectados (`items`). Cada elemento puede incluir la URL del recurso, el selector, el fragmento de HTML, `displayed` (tamaño en pantalla, útil para elegir a qué tamaño exportar las imágenes), `reasons`, el texto del error y `sourceLocation` (archivo y línea).
- `runWarnings`: avisos de Lighthouse. Si hay alguno, menciónalo, porque puede invalidar la medición.

Si necesitas más detalle de una auditoría, búscalo en `raw-<estrategia>.json`. No leas ese archivo entero: es muy grande.

**Relaciona los problemas con el código.** Este paso es el que hace útil el informe. Comprueba si el directorio de trabajo es el proyecto de esa web: busca `package.json`, el framework y los nombres de recursos que aparecen en `items`. Para cada problema busca dónde se origina (el `<link>` que bloquea el renderizado, el componente que carga la imagen del LCP, el script de terceros) y anota el archivo y la línea. Si no encuentras el proyecto, pregunta dónde está (si nadie puede responder, sigue como si no hubiera código).

**Si no hay código local** (la persona solo da la URL), el informe queda como tareas para otra persona. Aun así, hazlo concreto:
- Descarga el HTML público (`curl -s <URL> -o fuente/index.html`) y cita sus líneas. Avisa en el informe de que son líneas del HTML servido y que pueden no coincidir con las plantillas.
- Mira las cabeceras con `curl -sI` (la página y un CSS o una imagen) para ver `Cache-Control`, la compresión y el servidor (nginx, Apache, Plesk, Cloudflare…). Así los arreglos de servidor pueden llevar instrucciones para esa plataforma concreta.

Clasifica cada arreglo según dónde se aplica:

- **Código**: puedes aplicarlo tú en el proyecto.
- **Servidor/hosting/CDN**: caché HTTP, compresión, TTFB, redirecciones, HTTP/2. Normalmente no está en el repositorio: da instrucciones concretas. Si el proyecto tiene la configuración (por ejemplo `vercel.json`, `netlify.toml`, `nginx.conf`, `.htaccess` o cabeceras de Next), entonces cuenta como código.
- **Terceros/contenido**: scripts de marketing, chats, imágenes subidas a un CMS. Explica qué decisión hay que tomar y quién la toma.

Para encontrar la causa y la solución de cada auditoría habitual, consulta `references/audit-fixes.md`.

**Prioriza** por impacto real y por lo que cuesta arreglarlo, no por el orden de Lighthouse: ahorro estimado, si la métrica afectada está en rojo o ámbar, si pasa en móvil y en escritorio, y la dificultad. Para cada arreglo decide prioridad (🔥 hacer ya / 📌 planificar / 💤 no prioritario), dificultad, tiempo estimado y quién lo hace. Decir "esto no merece la pena ahora" es tan útil como decir qué hacer. Agrupa las auditorías que tienen la misma causa en un solo arreglo (por ejemplo, un LCP lento por una imagen hero pesada y sin precarga).

**Escribe el informe** en `pagespeed-informe-<dominio>-<AAAA-MM-DD>.md`, en la raíz del proyecto (o en el directorio de trabajo si no hay proyecto). Escríbelo en el idioma de la persona y con lenguaje claro: lo puede leer alguien que no es técnico.

**Sigue la plantilla de `references/report-template.md`**: léela antes de escribir. Tiene la estructura (veredicto, puntuaciones, Core Web Vitals, peso de la página, plan de acción, fichas de cada arreglo, lo que no haríamos, notas y glosario), las leyendas de iconos y los criterios para decidir la prioridad. Los iconos tienen que significar siempre lo mismo para que el informe se lea de un vistazo.

Numera los arreglos: así la persona puede elegir diciendo "el 1, el 3 y el 4".

## 3. Elegir y aplicar

En el chat, haz un resumen de 3-5 líneas, indica la ruta del informe y pregunta qué arreglos quiere aplicar. Si no hay código local, en lugar de eso pregunta si quiere aplicarlos sobre el proyecto (y dónde está) o solo entregar el informe. Si tienes `AskUserQuestion`, ofrece los arreglos de tipo código como opciones de selección múltiple (como máximo 4 por pregunta; agrupa o usa varias preguntas). Si no, pide los números. Ofrece también "solo el informe". Espera la respuesta: no empieces a cambiar el código antes.

Al aplicar:

- Aplica solo los arreglos elegidos, uno a uno. Antes de tocar nada, lee el código afectado.
- Respeta las convenciones del proyecto y usa las herramientas del framework (por ejemplo `next/image` y `next/font` en Next, `<Image>` en Astro). No metas dependencias nuevas sin decirlo.
- No cambies cómo se ve la web sin avisar. Algunos arreglos se notan visualmente (cambiar `font-display`, recortar CSS, cargar una imagen de forma diferida). Avisa de cada uno.
- Después de los cambios, ejecuta el build, el lint y los tests que tenga el proyecto, y arregla lo que hayas roto.
- No hagas commit, push ni despliegues sin que la persona lo pida.

## 4. Volver a medir

Compara siempre con la misma estrategia (móvil con móvil), porque las notas de laboratorio varían de una ejecución a otra (±5 puntos es normal).

- Si el proyecto se puede servir en local, haz el build de producción, arráncalo y mide `http://localhost:<puerto>` **antes y después** de los cambios. Mide primero la versión sin cambios (con `git stash` o en un build previo) o, si no es posible, avisa de que la comparación con la URL pública no es directa.
- Si no se puede servir en local, explica que la mejora se verá al desplegar y da el comando para volver a medir la URL pública.

Añade al informe una sección `## 🔁 Resultados tras los cambios` con una tabla antes/después (con los mismos iconos de puntuación) y los arreglos aplicados, y resúmela en el chat. Si una métrica empeora, dilo y explica la causa probable.

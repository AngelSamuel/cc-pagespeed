---
name: pagespeed-audit
description: Analiza el rendimiento de una web con Google PageSpeed Insights / Lighthouse (rendimiento, accesibilidad, buenas prácticas y SEO, en móvil y escritorio), genera un informe priorizado y, cuando la persona elige qué arreglos quiere, los aplica en el código del proyecto local y vuelve a medir. Úsala siempre que alguien pida analizar u optimizar la velocidad de una URL, mencione PageSpeed, Lighthouse, Core Web Vitals, LCP, INP, CLS o la nota de rendimiento, o diga que su web "va lenta" o "carga mal en móvil", aunque no nombre la herramienta.
---

# PageSpeed Audit

Convierte una URL en un informe de PageSpeed entendible y en cambios reales en el código. Tiene tres fases, y entre la segunda y la tercera la persona decide:

1. **Medir**: el script consulta PageSpeed (o Lighthouse en local) y deja un resumen.
2. **Informar**: escribes un informe priorizado y relacionas cada problema con los archivos del proyecto.
3. **Aplicar**: solo los arreglos que la persona elija. Después se vuelve a medir.

La persona puede querer solo el informe, o solo algunos arreglos. Las dos cosas son resultados válidos: nunca apliques cambios que no se han elegido.

## 1. Medir

Ejecuta el script incluido (está en la carpeta de esta skill):

```bash
python3 <carpeta-de-la-skill>/scripts/run_pagespeed.py <URL> --out ./pagespeed-report
```

Por defecto analiza móvil y escritorio. Puede tardar 1-2 minutos: lánzalo y espera.

**Motor.** La skill se instala en muchos equipos y tiene que funcionar gratis, por eso el script elige el motor solo (`--engine auto`):

- Si existe la variable de entorno `PAGESPEED_API_KEY`, usa la **API de PageSpeed**. Es la única opción que trae **datos de campo** (usuarios reales de Chrome, CrUX), los que Google tiene en cuenta para el posicionamiento.
- Si no hay key, o la API devuelve error de cuota, usa **Lighthouse en local** con `npx`. Es el mismo motor que PageSpeed, gratis y sin key, pero solo da datos de laboratorio. Necesita Node.js y Google Chrome.

Google no da cuota a las peticiones sin key, así que no intentes usar la API sin ella. Si el script falla porque faltan Node o Chrome, explica las dos salidas: instalar Node y Chrome, o crear una API key gratuita (en https://developers.google.com/speed/docs/insights/v5/get-started) y hacer `export PAGESPEED_API_KEY=...`. Nunca escribas la key en archivos del proyecto ni en la skill.

Para URLs de `localhost` o dominios locales el script usa siempre Lighthouse local, porque los servidores de Google no pueden acceder a ellas.

## 2. Informar

Lee `pagespeed-report/summary.json`. Para cada estrategia contiene:

- `scores`: nota de 0 a 100 por categoría.
- `field`: datos de usuarios reales con el p75 y la categoría FAST, AVERAGE o SLOW. Es `null` si no hay datos o si el motor es local. `scope: origen` significa que son de todo el dominio, no de esa página.
- `lab`: métricas de laboratorio.
- `lcp`: qué elemento es el LCP (selector, fragmento de HTML y tamaño mostrado) y cuánto tarda cada fase (TTFB, retraso de carga, descarga, renderizado). Con esto sabes si el problema está en el servidor, en el descubrimiento o en el peso.
- `issues`: auditorías por mejorar en cada categoría, con el ahorro estimado (`metricSavings`, `overallSavingsMs/Bytes`) y los elementos afectados (`items`). Cada elemento puede incluir la URL del recurso, el selector, el fragmento de HTML, `displayed` (tamaño en pantalla, útil para elegir a qué tamaño exportar las imágenes), `reasons`, el texto del error y `sourceLocation` (archivo y línea).
- `runWarnings`: avisos de Lighthouse. Si hay alguno, menciónalo, porque puede invalidar la medición.

Si necesitas más detalle de una auditoría, búscalo en `raw-<estrategia>.json`. No leas ese archivo entero: es muy grande.

**Relaciona los problemas con el código.** Este paso es el que hace útil el informe. Comprueba si el directorio de trabajo es el proyecto de esa web: busca `package.json`, el framework y los nombres de recursos que aparecen en `items`. Para cada problema busca dónde se origina (el `<link>` que bloquea el renderizado, el componente que carga la imagen del LCP, el script de terceros) y anota el archivo y la línea. Si no encuentras el proyecto, pregunta dónde está.

**Si no hay código local** (la persona solo da la URL), el informe queda como tareas para otra persona. Aun así, hazlo concreto:
- Descarga el HTML público (`curl -s <URL> -o fuente/index.html`) y cita sus líneas. Avisa en el informe de que son líneas del HTML servido y que pueden no coincidir con las plantillas.
- Mira las cabeceras con `curl -sI` (la página y un CSS o una imagen) para ver `Cache-Control`, la compresión y el servidor (nginx, Apache, Plesk, Cloudflare…). Así los arreglos de servidor pueden llevar instrucciones para esa plataforma concreta.

Clasifica cada arreglo según dónde se aplica:

- **Código**: puedes aplicarlo tú en el proyecto.
- **Servidor/hosting/CDN**: caché HTTP, compresión, TTFB, redirecciones, HTTP/2. Normalmente no está en el repositorio: da instrucciones concretas. Si el proyecto tiene la configuración (por ejemplo `vercel.json`, `netlify.toml`, `nginx.conf`, `.htaccess` o cabeceras de Next), entonces cuenta como código.
- **Terceros/contenido**: scripts de marketing, chats, imágenes subidas a un CMS. Explica qué decisión hay que tomar y quién la toma.

Para encontrar la causa y la solución de cada auditoría habitual, consulta `references/audit-fixes.md`.

**Prioriza** por impacto real: ahorro estimado en las métricas, peso de la auditoría y si el problema aparece en móvil y en escritorio. Los arreglos rápidos y de gran impacto van primero. Agrupa las auditorías que tienen la misma causa en un solo arreglo (por ejemplo, un LCP lento por una imagen hero pesada y sin precarga).

**Escribe el informe** en `pagespeed-informe-<dominio>-<AAAA-MM-DD>.md`, en la raíz del proyecto (o en el directorio de trabajo si no hay proyecto). Escríbelo en el idioma de la persona y con lenguaje claro: lo puede leer alguien que no es técnico. Usa esta estructura:

```markdown
# Informe PageSpeed: <dominio>
<URL> · <fecha> · Motor: API de PageSpeed / Lighthouse local <versión>

## Resumen
2-4 frases: cómo está la web, el problema principal y qué se gana arreglándolo.

## Notas
| Categoría | Móvil | Escritorio |
(rendimiento, accesibilidad, buenas prácticas, SEO)

## Core Web Vitals
Datos de campo (si los hay) y de laboratorio: LCP, INP/TBT, CLS, FCP, TTFB, con su valoración
(bueno / mejorable / malo). Indica si los datos de campo son de la página o de todo el dominio.

## Arreglos propuestos
### 1. <Título orientado a la acción> — Impacto: alto · Esfuerzo: bajo · Tipo: código
- Problema: qué pasa y en qué métrica se nota (con el ahorro estimado).
- Causa: dónde está, con la ruta del archivo y la línea.
- Solución: qué se cambiaría exactamente.
- Auditorías relacionadas: ids de Lighthouse.
### 2. …

## Fuera del código
Lo que depende del servidor, del hosting, del CMS o de terceros, con instrucciones.

## Notas de medición
Variabilidad, avisos de Lighthouse, limitaciones del motor usado.
```

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

Compara siempre con el mismo motor y la misma estrategia, porque las notas de laboratorio varían de una ejecución a otra (±5 puntos es normal).

- Si el proyecto se puede servir en local, haz el build de producción, arráncalo y mide `http://localhost:<puerto>` con `--engine local` **antes y después** de los cambios. Mide primero la versión sin cambios (con `git stash` o en un build previo) o, si no es posible, avisa de que la comparación con la URL pública no es directa.
- Si no se puede servir en local, explica que la mejora se verá al desplegar y da el comando para volver a medir la URL pública.

Añade al informe una sección `## Resultados tras los cambios` con una tabla antes/después y los arreglos aplicados, y resúmela en el chat. Si una métrica empeora, dilo y explica la causa probable.

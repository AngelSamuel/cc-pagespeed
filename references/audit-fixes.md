# Guía de arreglos por auditoría

Para cada auditoría habitual de Lighthouse 12-13: la causa típica, dónde buscarla en el código y la solución. Los ids pueden cambiar entre versiones de Lighthouse; si no encuentras uno, busca por el título o por el tema.

Contenido: [LCP y carga](#lcp-y-carga) · [Recursos que bloquean el renderizado](#recursos-que-bloquean-el-renderizado) · [Imágenes](#imágenes) · [Fuentes](#fuentes) · [JavaScript](#javascript) · [CLS](#cls) · [INP / TBT](#inp--tbt) · [Servidor y red](#servidor-y-red) · [Accesibilidad](#accesibilidad) · [Buenas prácticas](#buenas-prácticas) · [SEO](#seo)

## LCP y carga

**`lcp-discovery-insight`, `lcp-breakdown-insight` / `lcp-phases-insight`, `largest-contentful-paint-element`**
- Causa: el elemento del LCP (casi siempre la imagen hero o un titular) se descubre tarde, se carga de forma diferida o pesa mucho. Las fases indican dónde se va el tiempo: TTFB (servidor), retraso de carga (descubrimiento), duración de la carga (peso) o retraso de renderizado (JS/CSS).
- Dónde buscar: el selector o fragmento que aparece en `items`. Busca ese componente en el código.
- Solución: quita `loading="lazy"` de la imagen del LCP; añade `fetchpriority="high"`; si viene de un CSS `background-image` o la inserta el JS, pásala a un `<img>` en el HTML o precárgala con `<link rel="preload" as="image" fetchpriority="high">`. Next: `<Image priority>`. Astro: `<Image loading="eager" fetchpriority="high">`. Si el retraso de renderizado es alto, el problema es el JS o el CSS que bloquea (ver abajo).

**`network-dependency-tree-insight`** (antes `critical-request-chains`)
- Causa: cadenas de peticiones encadenadas (un CSS que importa otro CSS que carga una fuente).
- Solución: aplana la cadena. Usa `preconnect` hacia los orígenes críticos (máximo 2-4), `preload` para los recursos que se descubren tarde y elimina los `@import` dentro del CSS.

## Recursos que bloquean el renderizado

**`render-blocking-insight`** (antes `render-blocking-resources`)
- Causa: hojas de estilo y scripts síncronos en el `<head>`.
- Solución: añade `defer` (o `type="module"`) a los scripts; mete el CSS crítico en línea y carga el resto de forma diferida; mueve los CSS de terceros (fuentes, widgets) o cárgalos con `media="print" onload="this.media='all'"`. En frameworks con bundler suele bastar con no importar el CSS global de librerías que no se usan en esa página.

**`unused-css-rules`, `unminified-css`, `unused-javascript`, `unminified-javascript`**
- Solución: comprueba que el build de producción minifica (normalmente sí; si no, la URL medida puede ser un build de desarrollo). Elimina las librerías que se cargan enteras para usar una parte; usa la división de código por ruta y `import()` dinámico para los componentes que no se ven al cargar la página. Si Tailwind genera un CSS enorme, revisa `content`/`@source`.

## Imágenes

**`image-delivery-insight`** (reúne `uses-optimized-images`, `modern-image-formats`, `uses-responsive-images`, `efficient-animated-content`)
- Solución: usa AVIF/WebP; dimensiones ajustadas al tamaño mostrado, con `srcset` y `sizes`; comprime al 75-85 %; cambia los GIF animados por `<video autoplay muted loop playsinline>`. Usa el componente de imagen del framework si lo hay. En imágenes estáticas del repositorio puedes convertirlas tú si hay herramienta disponible (`sharp`, `cwebp`, `squoosh-cli`); si vienen de un CMS, es una tarea de contenido.

**Imágenes fuera de pantalla** (`offscreen-images` hasta Lighthouse 12; en la 13 ya no existe como auditoría): pon `loading="lazy"` en las imágenes que están debajo del primer pantallazo, nunca en la del LCP. En Lighthouse 13 se detecta mirando el HTML: busca los `<img>` que no tienen `loading` o que tienen `loading="eager"` lejos del hero.

**`unsized-images`**: añade `width` y `height`, o `aspect-ratio` en CSS (también ayuda al CLS).

## Fuentes

**`font-display-insight`** (antes `font-display`)
- Solución: `font-display: swap` (o `optional` para evitar el salto de texto). Google Fonts: añade `&display=swap`. Lo mejor es autoalojar con `next/font`, `@fontsource` o archivos `woff2` locales, precargar solo 1-2 pesos críticos y usar subconjuntos de caracteres.
- Efecto visual: con `swap` hay un cambio breve de fuente al cargar. Avísalo.

## JavaScript

**`bootup-time`, `mainthread-work-breakdown`, `third-parties-insight`** (antes `third-party-summary`)
- Causa habitual: terceros (analítica, chats, tests A/B, píxeles), hidratación pesada.
- Solución: carga los terceros después de la interacción o en `requestIdleCallback`; usa fachadas para chats y vídeos incrustados (por ejemplo `lite-youtube`); con Next `<Script strategy="lazyOnload">`; con Partytown para la analítica. Quitar un tercero lo decide la persona: proponlo, no lo quites tú.

**`legacy-javascript-insight`** (antes `legacy-javascript`): ajusta el `browserslist` o el `target` del bundler a navegadores modernos y quita los polyfills que no hacen falta.

**`duplicated-javascript-insight`**: busca varias versiones de la misma librería (`npm ls <pkg>`) y unifícalas.

**`dom-size-insight`** (antes `dom-size`): demasiados nodos. Usa virtualización en listas largas y renderiza bajo demanda los menús y modales ocultos.

## CLS

**`cls-culprits-insight`** (antes `layout-shifts`, `layout-shift-elements`)
- Causas: imágenes o iframes sin tamaño, anuncios o banners que se insertan arriba, fuentes que cambian de métricas, contenido inyectado por JS.
- Solución: reserva el espacio (`width`/`height`, `aspect-ratio`, `min-height` en los contenedores de anuncios y embebidos); muestra los banners de cookies superpuestos, sin empujar el contenido; usa `size-adjust` o el ajuste de fuentes de `next/font`; anima con `transform`, no con `top`/`height`.

## INP / TBT

**`inp-breakdown-insight`, `forced-reflow-insight`, `long-tasks`, `total-blocking-time`**
- Solución: divide las tareas largas (`await scheduler.yield()` o `setTimeout`); quita trabajo de los manejadores de eventos; evita leer el layout justo después de escribirlo (reflow forzado); usa debounce en los manejadores de `scroll`/`resize`; reduce la hidratación (islas, server components).

## Servidor y red

Estos arreglos suelen ser de tipo "servidor/hosting" salvo que la configuración esté en el repositorio.

- **`server-response-time`, `document-latency-insight`**: TTFB alto. Usa caché de página o CDN, generación estática o ISR en lugar de SSR por petición y revisa las consultas lentas. `document-latency-insight` también marca la falta de compresión y las redirecciones.
- **`redirects`**: enlaza directamente a la URL final (con o sin `www`, con o sin barra final, siempre `https`) y quita los saltos encadenados. Si la redirección la hace el propio código (middleware, i18n), puede ser de tipo código.
- **`cache-insight`** (antes `uses-long-cache-ttl`): `Cache-Control: public, max-age=31536000, immutable` para los recursos con hash en el nombre. Se configura en `vercel.json`, `netlify.toml`, `_headers`, `headers()` de Next, nginx o `.htaccess`.
- **`uses-text-compression`**: activa Brotli o gzip en el servidor o la CDN.
- **`modern-http-insight`** (antes `uses-http2`): activa HTTP/2 o HTTP/3 en el hosting o la CDN.
- **`total-byte-weight`**: resultado de todo lo anterior. Ataca primero las imágenes y el JS.

## Accesibilidad

- **`color-contrast`**: sube el contraste a ≥4,5:1 (≥3:1 en texto grande). Cambia el color visual: propón los valores concretos y avisa.
- **`image-alt`**: añade un `alt` descriptivo (o `alt=""` si la imagen es decorativa). Si no sabes qué muestra la imagen, pide el texto.
- **`link-name`, `button-name`**: los enlaces y botones con solo un icono necesitan `aria-label` o texto oculto visualmente.
- **`label`, `select-name`**: asocia `<label for>` a los campos de formulario.
- **`html-has-lang`, `html-lang-valid`**: `<html lang="es">`.
- **`heading-order`**: no te saltes niveles de encabezado. Si para corregirlo cambias la etiqueta, mantén el estilo con clases.
- **`frame-title`**: añade `title` a los `<iframe>`.
- **`aria-*`**: corrige los roles o atributos ARIA no válidos; si un elemento nativo sirve, mejor que ARIA.
- **`target-size`**: las zonas táctiles deben medir al menos 24×24 px.

## Buenas prácticas

- **`errors-in-console`**: busca el origen de cada error (los `items` traen la URL o la fuente) y corrígelo, o márcalo como de terceros.
- **`third-party-cookies`**: cookies de terceros. Suelen ser de embebidos o píxeles: es una decisión sobre terceros.
- **`inspector-issues`**: problemas del panel Issues de Chrome (cookies SameSite, contenido mixto, CSP). Mira el detalle en `items`.
- **`image-aspect-ratio`, `image-size-responsive`**: imágenes deformadas o de poca resolución. Corrige las dimensiones o el `srcset`.
- **`is-on-https`, contenido mixto**: cambia los recursos `http://` a `https://`.
- **`csp-xss`, `has-hsts`, `clickjacking-mitigation`, `origin-isolation`**: cabeceras de seguridad (a menudo de tipo servidor). Ojo: una CSP mal hecha rompe la web. Propón una política de solo informe primero (`Content-Security-Policy-Report-Only`).
- **`deprecations`**: API obsoletas. Si vienen de una librería, puede bastar con actualizarla.

## SEO

- **`document-title`, `meta-description`**: título y descripción únicos por página. Escribe una propuesta y pide confirmación del texto.
- **`link-text`**: cambia los "haz clic aquí" o "más información" por textos descriptivos.
- **`crawlable-anchors`**: los enlaces necesitan un `href` real, no solo `onclick`.
- **`is-crawlable`**: `noindex` o `robots.txt` bloquean la página. Pregunta antes de tocarlo: a veces es intencionado (staging).
- **`robots-txt`, `canonical`, `hreflang`, `http-status-code`**: valida la sintaxis y que las URL sean absolutas y coherentes.
- **`structured-data`** (manual): no sale como fallo, pero si la persona quiere SEO avanzado, sugiere revisar el schema.

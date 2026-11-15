# 🚀 Informe de rendimiento web: theguardian.com

> 🌐 https://www.theguardian.com/international · 📅 15 de noviembre de 2026 · 🔬 Lighthouse 13.6.0 (móvil y escritorio)
> 🔎 [Ver el análisis oficial de Google con datos de usuarios reales](https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fwww.theguardian.com%2Finternational)

## 🧭 Resumen

**Veredicto: 🟠 Mejorable**

La portada internacional va bien en escritorio (rendimiento 96) y es mejorable en móvil (87). En la conexión móvil lenta que simula Google, la foto principal tarda 3,6 s en verse, por encima de los 2,5 s que Google considera buenos. La página no se mueve mientras carga, responde enseguida al tacto y el servidor contesta en 19 ms. El tiempo se va sobre todo en lo que el móvil tiene que descargar antes de pintar: el código de la página (HTML), de 155 KB comprimido, y, en la primera visita, una segunda copia de las fuentes, que muy probablemente pide el aviso de cookies. Además hay varios fallos de accesibilidad y SEO que se corrigen en menos de una hora cada uno.

> 💡 **Lo más importante:** comprimir el HTML con Brotli en la CDN (#1). Es el primer archivo que necesita el móvil y, según nuestra prueba, pasaría de unos 152 KB a unos 93 KB.

## 📊 Puntuaciones

| | 📱 Móvil | 🖥️ Escritorio |
|---|:---:|:---:|
| ⚡ Rendimiento | 🟠 87 | 🟢 96 |
| ♿ Accesibilidad | 🟠 89 | 🟢 92 |
| ✅ Buenas prácticas | 🟢 100 | 🟢 100 |
| 🔍 SEO | 🟠 85 | 🟠 85 |

## ⏱️ Core Web Vitals

| Métrica | Qué significa | 📱 Móvil | 🖥️ Escritorio | Objetivo |
|---|---|:---:|:---:|:---:|
| **LCP** | Cuánto tarda en verse el contenido principal | ⚠️ 3,6 s | ✅ 1,4 s | ≤ 2,5 s |
| **TBT** | Cuánto tiempo la página no responde mientras carga | ✅ 60 ms | ✅ 0 ms | ≤ 200 ms |
| **CLS** | Si el contenido "salta" mientras carga | ✅ 0,009 | ✅ 0,001 | ≤ 0,1 |
| **FCP** | Cuándo aparece lo primero en pantalla | ⚠️ 2,5 s | ✅ 0,7 s | ≤ 1,8 s |

El elemento del LCP es la foto de una de las noticias destacadas (`picture.dcr-1b8y165 > img.dcr-11wzo8p`, 392×314 px en móvil y 620×496 px en escritorio). Ya está en el HTML inicial y no usa carga diferida, pero Chrome la pide con prioridad baja. En la carga sin limitar, la mayor parte del tiempo se va en el retraso de renderizado (41 % en móvil, 43 % en escritorio) y en la respuesta del servidor (33 % y 37 %). La descarga de la propia imagen pesa poco (11 % y 10 %). Es decir: la foto llega pronto, pero el navegador tarda en poder pintarla.

## 📦 Peso de la página

**1.347 KB en 110 peticiones (móvil; 1.394 KB en escritorio).** Reparto en móvil:

```
JavaScript ████████░░░░░░░░░░░░  550 KB  41 %
Imágenes   █████░░░░░░░░░░░░░░░  361 KB  27 %
Fuentes    ████░░░░░░░░░░░░░░░░  245 KB  18 %
HTML       ██░░░░░░░░░░░░░░░░░░  157 KB  12 %
Otros      █░░░░░░░░░░░░░░░░░░░   33 KB   2 %
```

El peso total está dentro de lo razonable para una portada (< 1-1,5 MB). Lo llamativo es el reparto: hay 10 archivos de fuentes (245 KB), y la mitad son una segunda versión de familias que ya se habían descargado (ver #3).

## 🎯 Plan de acción

| # | Arreglo | Prioridad | Dificultad | Tiempo | Quién | Mejora esperada |
|:-:|---|:-:|:-:|:-:|:-:|---|
| 1 | Comprimir el HTML con Brotli en Fastly | 🔥 Hacer ya | 🟡 Media | ½ día | 🖥️ | −60 KB de HTML (nuestra medición) · FCP y LCP móvil |
| 2 | Dar prioridad alta a la imagen del LCP | 🔥 Hacer ya | 🟡 Media | ½ día | 👩‍💻 | LCP móvil (Lighthouse no lo cuantifica) |
| 3 | Evitar que el aviso de consentimiento descargue otra copia de las fuentes | 🔥 Hacer ya | 🟡 Media | 2-4 h | 👩‍💻 🤝 | −162 KB de fuentes y −28 KB de logos en la primera visita |
| 4 | Corregir la cabecera `Link` y recortar los `preconnect` | 🔥 Hacer ya | 🟢 Fácil | ~30 min | 👩‍💻 | Quita el aviso de Lighthouse · 6 conexiones anticipadas sin usar menos |
| 5 | Poner nombre a los botones de reproducir vídeo | 🔥 Hacer ya | 🟢 Fácil | ~30 min | 👩‍💻 | Con #6: accesibilidad escritorio 92 → 100, móvil 89 → 96 |
| 6 | Corregir la lista del carrusel de destacados | 🔥 Hacer ya | 🟢 Fácil | ~30 min | 👩‍💻 | Ver #5 |
| 7 | Quitar `role="menubar"` del menú de navegación | 🔥 Hacer ya | 🟢 Fácil | ~1 h | 👩‍💻 | Con #5 y #6: accesibilidad móvil → 100 |
| 8 | Dar texto descriptivo al enlace "Learn more" | 🔥 Hacer ya | 🟢 Fácil | ~15 min | 👩‍💻 ✍️ | SEO 85 → 92 |
| 9 | Ajustar las imágenes a la densidad real de la pantalla | 📌 Planificar | 🟡 Media | 1-2 días | 👩‍💻 | −92 KB en móvil (estimación de Lighthouse) |
| 10 | Reducir el JavaScript propio sin usar y duplicado | 📌 Planificar | 🔴 Difícil | varias semanas | 👩‍💻 | −175 KB de JS sin usar y −19 KB duplicados · LCP móvil −150 ms (estimaciones de Lighthouse) |
| 11 | Decidir si el `canonical` debe apuntar a la portada | 📌 Planificar | 🟢 Fácil | ~1 h + decisión | 🤝 | SEO +8 puntos en Lighthouse, si se cambia |

> ⚡ **Quick wins** (menos de 30 min cada uno): #4, #5, #6, #8. Juntos llevarían la accesibilidad de escritorio a 100, la de móvil a 96 y el SEO a 92 (cálculo con los pesos de Lighthouse), sin cambios visibles.

## 🛠️ Detalle de los arreglos

> Las líneas citadas son del HTML servido el 15/11/2026 (descargado un minuto después de la medición), no de las plantillas del proyecto. El HTML está minificado en líneas muy largas (la 559 tiene unos 248.000 caracteres) y la portada cambia con cada actualización editorial, así que conviene localizar cada elemento por el selector. Las rutas de los mapas de origen indican que el front-end es `@guardian/dotcom-rendering`.

### 1. 🔥 Comprimir el HTML con Brotli en Fastly

| Prioridad | Dificultad | Tiempo | Quién | Tipo |
|:-:|:-:|:-:|:-:|:-:|
| 🔥 Hacer ya | 🟡 Media | ½ día | 🖥️ Hosting / servidor | Servidor/CDN |

**🖥️ Infraestructura**: la CDN es **Fastly**: lo indican las cabeceras `x-served-by: cache-mad…`, `x-timer` y `via: 1.1 varnish`, y en las imágenes `fastly-io-*`. El HTML se sirve por HTTP/2 (con HTTP/3 anunciado), con `cache-control: max-age=60, …, private` y compresión **gzip**, aunque el navegador acepte Brotli.

**❓ Qué pasa**: el HTML de la portada ocupa 1,4 MB sin comprimir. Casi la mitad (unos 687 KB) es CSS en línea, en un único bloque `<style>` (`index.html:234`). Se sirve con gzip: 152 KB en nuestra descarga (155 KB según Lighthouse, que cuenta también las cabeceras). En una prueba sobre el mismo HTML, Brotli lo deja en **93 KB** con un nivel apto para contenido dinámico (nivel 5) y en 79 KB con el máximo (nivel 11). Es el primer archivo que necesita el navegador para pintar nada, y en móvil el FCP (2,5 s) y el LCP (3,6 s) están en ⚠️. Lighthouse no lo marca porque da por buena cualquier compresión: esta recomendación sale de nuestra medición del HTML descargado, no de una auditoría.

**📍 Dónde**: configuración del servicio de Fastly que sirve `www.theguardian.com` (respuestas `text/html`).

**✅ Cómo arreglarlo**:
1. En Fastly, activa la compresión dinámica con Brotli para `text/html`. En VCL se hace en `vcl_fetch` con `set beresp.brotli = true;` cuando la petición acepta `br` (consulta la documentación de Fastly y si el plan contratado lo incluye). La alternativa es comprimir con Brotli en el servidor de origen.
2. Mantén `Vary: Accept-Encoding` (ya está) y gzip como respaldo.
3. Comprueba con `curl -sI -H 'Accept-Encoding: br' https://www.theguardian.com/international` que la respuesta trae `content-encoding: br`.

**📈 Qué se gana**: unos 60 KB menos en el archivo crítico, un 39 % (estimación sobre el HTML del 15/11/2026). Con la conexión que simula Lighthouse (unos 1,5 Mbit/s), eso supone del orden de 0,3 s menos de descarga antes de que se pueda pintar. Es una estimación: el efecto real en FCP y LCP hay que medirlo después del cambio.

**⚠️ Ojo**: Brotli a niveles altos consume más CPU por respuesta. Con HTML que cambia cada pocos minutos conviene un nivel intermedio (4-6). Vigila la carga de la CDN o del origen los primeros días.

<details><summary>🔬 Auditorías de Lighthouse</summary>

Ninguna lo marca (`document-latency-insight` da la compresión por buena). Relacionadas: `first-contentful-paint`, `largest-contentful-paint`, `total-byte-weight`.

</details>

### 2. 🔥 Dar prioridad alta a la imagen del LCP

| Prioridad | Dificultad | Tiempo | Quién | Tipo |
|:-:|:-:|:-:|:-:|:-:|
| 🔥 Hacer ya | 🟡 Media | ½ día | 👩‍💻 Desarrollo | Código |

**❓ Qué pasa**: la foto que Google toma como contenido principal ya está en el HTML y no usa carga diferida, pero Chrome la pide con prioridad **baja** (Low). Al mismo tiempo pide 10 fuentes con prioridad muy alta, y en una conexión lenta todo eso compite con la foto. Lighthouse marca que le falta `fetchpriority="high"`, que es el único punto pendiente de su comprobación de descubrimiento del LCP.

**📍 Dónde**: `picture.dcr-1b8y165 > img.dcr-11wzo8p` (en el HTML servido, `index.html:559`). Es el componente de imagen de las tarjetas de portada. En la versión descargada hay 13 `<img loading="eager">`.

**✅ Cómo arreglarlo**: en el componente de tarjeta, marca con `fetchpriority="high"` solo la imagen de la primera tarjeta grande del primer contenedor visible. Como el contenido de la portada cambia, la regla tiene que depender de la posición, no de la noticia. Revisa también qué imágenes llevan `loading="eager"`: las que quedan por debajo del primer pantallazo pueden pasar a `lazy`.

```html
<!-- Antes -->
<img alt="…" src="https://i.guim.co.uk/img/media/…?width=465&dpr=1…" loading="eager" class="dcr-11wzo8p"/>
<!-- Después -->
<img alt="…" src="https://i.guim.co.uk/img/media/…?width=465&dpr=1…" loading="eager" fetchpriority="high" class="dcr-11wzo8p"/>
```

**📈 Qué se gana**: Lighthouse no da una cifra para este cambio. Lo esperable es que la foto se descargue antes en móvil, donde el LCP está en ⚠️ (3,6 s).

**⚠️ Ojo**: dar prioridad alta a varias imágenes anula el efecto. Hay que limitarlo a una, como mucho a dos.

<details><summary>🔬 Auditorías de Lighthouse</summary>

`lcp-discovery-insight`, `largest-contentful-paint-element`, `lcp-breakdown-insight`

</details>

### 3. 🔥 Evitar que el aviso de consentimiento descargue otra copia de las fuentes

| Prioridad | Dificultad | Tiempo | Quién | Tipo |
|:-:|:-:|:-:|:-:|:-:|
| 🔥 Hacer ya | 🟡 Media | 2-4 h | 👩‍💻 Desarrollo · 🤝 Decisión del cliente | Terceros/contenido |

**❓ Qué pasa**: la página carga 10 archivos de fuentes (245 KB). Cinco son las versiones del propio sitio en `assets.guim.co.uk`, declaradas en el HTML con `font-display: swap`. Los otros cinco son **otra versión de las mismas familias** en `interactive.guim.co.uk/fonts/guss-webfonts/`: GuardianTextSansWeb Regular y Bold, GuardianTextEgyptianWeb Regular y Bold y GHGuardianHeadline Bold. Suman 162 KB, se piden con prioridad muy alta, no aparecen en el HTML servido y son las que Lighthouse marca sin `font-display`. Forman además la cadena de peticiones más larga de la carga (494 ms). En la carga observada se piden justo después de la configuración y los logos del aviso de consentimiento (Sourcepoint). Por eso es muy probable que los inyecte ese aviso, aunque Lighthouse no registra el iniciador y hay que confirmarlo. Los dos logos del aviso (512×512 y 140×140 px, mostrados a 42×42) suman otros 28 KB de sobra.

**📍 Dónde**: el mensaje de consentimiento que se configura en Sourcepoint (`sourcepoint.theguardian.com`), en su CSS o en las fuentes personalizadas del mensaje. Logos: `media.guim.co.uk/8c1c22e1…/0_0_512_512/512.png` y `media.guim.co.uk/843ea077…/0_0_512_512/140.jpg`.

**✅ Cómo arreglarlo**:
1. Confirma el origen: en DevTools, pestaña Red, filtra por `guss-webfonts` y mira la columna "Iniciador".
2. En la configuración del mensaje, apunta las fuentes a los mismos archivos que usa la página (`assets.guim.co.uk/static/frontend/fonts/…`, que ya están descargados o en caché), o usa las familias ya declaradas por su nombre en lugar de cargar otras.
3. Sustituye los logos por versiones a 84×84 px (2× de 42 px) o por SVG.

**📈 Qué se gana**: en la primera visita, 162 KB menos de fuentes (un 12 % del peso de la página) y 28 KB menos de imágenes. También desaparecen 5 peticiones de prioridad muy alta que compiten con la foto del LCP, y con ellas los avisos de `font-display` y buena parte de los de caché (las fuentes de `interactive.guim.co.uk` se cachean solo 3,5 días).

**⚠️ Ojo**: solo afecta a quien ve el aviso (primera visita o sin consentimiento guardado). Si las fuentes nuevas no son exactamente iguales, el aviso puede verse algo distinto: compáralo antes de publicar.

<details><summary>🔬 Auditorías de Lighthouse</summary>

`font-display-insight`, `network-dependency-tree-insight`, `cache-insight`, `image-delivery-insight` (logos del aviso)

</details>

### 4. 🔥 Corregir la cabecera `Link` y recortar los `preconnect`

| Prioridad | Dificultad | Tiempo | Quién | Tipo |
|:-:|:-:|:-:|:-:|:-:|
| 🔥 Hacer ya | 🟢 Fácil | ~30 min | 👩‍💻 Desarrollo | Código |

**❓ Qué pasa**: la cabecera HTTP `Link` del documento tiene un elemento vacío, una coma doble justo antes de `<https://assets.guim.co.uk/>` (carácter 688). Por eso Lighthouse avisa de que no puede leerla. Además, entre esa cabecera y el HTML la página pide conexión anticipada (`preconnect`) con 11 orígenes distintos. Durante la carga medida, 6 no se usaron: `j.ophan.co.uk`, `api.nextgen.guardianapps.co.uk`, `hits-secure.theguardian.com`, `phar.gu-web.net`, `static.theguardian.com` y `support.theguardian.com`. Lighthouse recomienda 4 como máximo.

**📍 Dónde**: cabecera `Link` de la respuesta de `https://www.theguardian.com/international` (`…graun.standalone.commercial.js>; rel=prefetch,,<https://assets.guim.co.uk/>…`) y `index.html:22-26` (los `<link rel="preconnect">`).

**✅ Cómo arreglarlo**:
1. Donde se monta la cabecera, filtra los valores vacíos antes de unirlos con comas.
2. Deja `preconnect` solo para los orígenes que se usan en la carga inicial (por ejemplo `assets.guim.co.uk` e `i.guim.co.uk`). Para el resto basta el `dns-prefetch` que ya hay en las líneas 27-35.

```text
Antes:   …commercial.js>; rel=prefetch,,<https://assets.guim.co.uk/>; rel=preconnect,…
Después: …commercial.js>; rel=prefetch,<https://assets.guim.co.uk/>; rel=preconnect,…
```

**📈 Qué se gana**: una cabecera válida y menos conexiones abiertas en vano al principio de la carga. Lighthouse no cuantifica la ganancia.

**⚠️ Ojo**: que un origen no se usara en esta carga no significa que nunca se use (por ejemplo, después de aceptar las cookies). Compruébalo antes de quitarlo.

<details><summary>🔬 Auditorías de Lighthouse</summary>

`network-dependency-tree-insight` (orígenes preconectados), aviso de ejecución sobre la cabecera `link`

</details>

### 5. 🔥 Poner nombre a los botones de reproducir vídeo

| Prioridad | Dificultad | Tiempo | Quién | Tipo |
|:-:|:-:|:-:|:-:|:-:|
| 🔥 Hacer ya | 🟢 Fácil | ~30 min | 👩‍💻 Desarrollo | Código |

**❓ Qué pasa**: los botones de reproducir y pausar de los vídeos en bucle solo tienen un icono. Un lector de pantalla los anuncia como "botón", sin decir para qué sirven. Hay 2 en la portada, y fallan en móvil y en escritorio.

**📍 Dónde**: `div.controls-container > button.play-pause-icon` (`index.html:559` y `:580`).

**✅ Cómo arreglarlo**: añade un `aria-label` que cambie con el estado.

```html
<!-- Antes -->
<button type="button" class="play-pause-icon dcr-19641bk" data-testid="play-icon">
<!-- Después -->
<button type="button" class="play-pause-icon dcr-19641bk" data-testid="play-icon" aria-label="Play video">
```

**📈 Qué se gana**: junto con #6, la accesibilidad pasa de 92 a 100 en escritorio y de 89 a 96 en móvil (cálculo con los pesos de Lighthouse).

<details><summary>🔬 Auditorías de Lighthouse</summary>

`button-name`

</details>

### 6. 🔥 Corregir la lista del carrusel de destacados

| Prioridad | Dificultad | Tiempo | Quién | Tipo |
|:-:|:-:|:-:|:-:|:-:|
| 🔥 Hacer ya | 🟢 Fácil | ~30 min | 👩‍💻 Desarrollo | Código |

**❓ Qué pasa**: el carrusel de destacados es una lista (`<ul>`), pero sus elementos llevan `role="group"`, que anula su papel de elemento de lista. Los lectores de pantalla ya no pueden anunciar "lista, N elementos" ni dejar navegar por ella como tal.

**📍 Dónde**: `gu-island > div.dcr-1c6gnzc > ul.dcr-4c0jzx` (`index.html:380`).

**✅ Cómo arreglarlo**: mueve el rol de diapositiva a un contenedor interior y deja el `<li>` como elemento de lista.

```html
<!-- Antes -->
<li role="group" aria-roledescription="slide" class="dcr-1i6ti96"><div …>…</div></li>
<!-- Después -->
<li class="dcr-1i6ti96"><div role="group" aria-roledescription="slide" …>…</div></li>
```

**📈 Qué se gana**: ver #5.

<details><summary>🔬 Auditorías de Lighthouse</summary>

`list`

</details>

### 7. 🔥 Quitar `role="menubar"` del menú de navegación

| Prioridad | Dificultad | Tiempo | Quién | Tipo |
|:-:|:-:|:-:|:-:|:-:|
| 🔥 Hacer ya | 🟢 Fácil | ~1 h | 👩‍💻 Desarrollo | Código |

**❓ Qué pasa**: el menú desplegable se declara como `menubar`, un rol pensado para menús de aplicación que solo puede contener elementos de menú. Dentro hay un buscador (campo de texto y botón). Con ese rol, el lector de pantalla espera un comportamiento de teclado que el menú no tiene. Solo falla en móvil.

**📍 Dónde**: `div#header-expanded-menu ul.dcr-k9l4gc` (`index.html:499`).

**✅ Cómo arreglarlo**: para una navegación de sitio basta con una lista normal dentro de `<nav>`. Quita el rol.

```html
<!-- Antes -->
<ul role="menubar" data-testid="nav-menu-columns" class="dcr-k9l4gc">
<!-- Después -->
<ul data-testid="nav-menu-columns" class="dcr-k9l4gc">
```

**📈 Qué se gana**: junto con #5 y #6, la accesibilidad en móvil llega a 100.

**⚠️ Ojo**: si hay elementos hijos con `role="menuitem"` o una navegación por teclado escrita para ese rol, hay que revisarlos a la vez. Por eso la estimación es de 1 h y no de 15 min.

<details><summary>🔬 Auditorías de Lighthouse</summary>

`aria-required-children`

</details>

### 8. 🔥 Dar texto descriptivo al enlace "Learn more"

| Prioridad | Dificultad | Tiempo | Quién | Tipo |
|:-:|:-:|:-:|:-:|:-:|
| 🔥 Hacer ya | 🟢 Fácil | ~15 min | 👩‍💻 Desarrollo · ✍️ Contenido | Código |

**❓ Qué pasa**: el enlace que explica la lista "Deeply read" dice solo "Learn more". Fuera de contexto no dice adónde lleva, ni a Google ni a quien navega por la lista de enlaces con un lector de pantalla.

**📍 Dónde**: `<a href="https://www.theguardian.com/info/2024/feb/28/what-is-the-deeply-read-list">` (`index.html:580`).

**✅ Cómo arreglarlo**: (texto propuesto, a confirmar por contenido)

```html
<!-- Antes -->
<a href="…/what-is-the-deeply-read-list" class="dcr-1hmjp3l">Learn more</a>
<!-- Después -->
<a href="…/what-is-the-deeply-read-list" class="dcr-1hmjp3l">Learn more about the Deeply read list</a>
```

**📈 Qué se gana**: SEO de 85 a 92 en Lighthouse (cálculo con los pesos de Lighthouse).

**⚠️ Ojo**: el texto es más largo; comprueba que cabe en el diseño del módulo.

<details><summary>🔬 Auditorías de Lighthouse</summary>

`link-text`

</details>

### 9. 📌 Ajustar las imágenes a la densidad real de la pantalla

| Prioridad | Dificultad | Tiempo | Quién | Tipo |
|:-:|:-:|:-:|:-:|:-:|
| 📌 Planificar | 🟡 Media | 1-2 días | 👩‍💻 Desarrollo | Código |

**❓ Qué pasa**: cada `<picture>` ofrece solo dos versiones por tamaño de pantalla, a densidad 1× o 2×, y cualquier pantalla de 1,25× o más recibe la de 2×. En el móvil que simula Lighthouse (densidad 1,75×), una foto que se muestra a 686×549 píxeles reales se descarga a 930×744. Lighthouse estima que en móvil sobran 92 KB solo en las fotos editoriales (121 KB contando los logos del aviso de consentimiento, que van en #3). En escritorio señala además margen de compresión en algunas fotos (117 KB en total).

**📍 Dónde**: componente de imagen de las tarjetas (`picture.dcr-1b8y165`, `picture.dcr-1fmn09d`). Por ejemplo, la imagen del LCP en `index.html:559`, con `<source srcSet="…?width=465&dpr=2…" media="(min-width: 320px) and (-webkit-min-device-pixel-ratio: 1.25)…">`.

**✅ Cómo arreglarlo**: el servicio de imágenes (`i.guim.co.uk`) ya acepta cualquier `width`. Sustituye la pareja 1×/2× por un `srcset` con anchos (`w`) y un `sizes`, para que el navegador elija la versión más próxima a lo que necesita.

```html
<!-- Antes -->
<source srcSet="…?width=465&dpr=2…" media="(min-width: 320px) and (-webkit-min-device-pixel-ratio: 1.25), …"/>
<source srcSet="…?width=465&dpr=1…" media="(min-width: 320px)"/>
<!-- Después -->
<source srcset="…?width=465&dpr=1… 465w, …?width=700&dpr=1… 700w, …?width=930&dpr=1… 930w"
        sizes="(min-width: 480px) 480px, 100vw" media="(min-width: 320px)"/>
```

(Los anchos y `sizes` del ejemplo son ilustrativos: hay que sacarlos del diseño real de cada tipo de tarjeta.)

**📈 Qué se gana**: −92 KB en la portada móvil según Lighthouse; en la imagen del LCP, 19 KB de 42 KB.

**⚠️ Ojo**: más tamaños posibles significan más variantes en la caché del servicio de imágenes. Conviene un conjunto cerrado de anchos. Revisa también la nitidez en pantallas de alta densidad.

<details><summary>🔬 Auditorías de Lighthouse</summary>

`image-delivery-insight`

</details>

### 10. 📌 Reducir el JavaScript propio sin usar y duplicado

| Prioridad | Dificultad | Tiempo | Quién | Tipo |
|:-:|:-:|:-:|:-:|:-:|
| 📌 Planificar | 🔴 Difícil | varias semanas | 👩‍💻 Desarrollo | Código |

**❓ Qué pasa**: Lighthouse estima 239 KB de JavaScript descargado que no se ejecuta durante la carga. De ellos, unos 175 KB son de los paquetes propios del sitio y 64 KB del aviso de consentimiento (ese tercero se trata en "Lo que no haríamos"). Además detecta 19 KB de módulos repetidos en varios paquetes, sobre todo `@guardian/source`, `@guardian/consent-manager` y `@guardian/libs`. El bloqueo de la página está en verde (TBT de 60 ms), así que esto afecta más a la descarga que a la respuesta al tacto.

**📍 Dónde** (sin usar, estimación de Lighthouse):
- `assets.guim.co.uk/assets/index.client.web.103b5bf4b6b86edec94f.js`: 57 KB
- `assets.guim.co.uk/assets/8252.client.web.c5051a4227e53dd30949.js`: 36 KB
- `assets.guim.co.uk/assets/2667.client.web.1621764e85a2ca8fd0bb.js`: 35 KB
- `assets.guim.co.uk/assets/9711.client.web.d5928bc409cce6b934dd.js`: 23 KB
- `assets.guim.co.uk/commercial/…/graun.standalone.commercial.js`: 23 KB

**✅ Cómo arreglarlo**: revisa con un analizador de paquetes (por ejemplo `webpack-bundle-analyzer`) qué entra en esos fragmentos. Carga con `import()` dinámico lo que no se ve al abrir la portada y unifica las versiones de `@guardian/source` y del resto de librerías repetidas para que vayan en un único fragmento compartido.

**📈 Qué se gana**: Lighthouse estima −150 ms de LCP en móvil (−100 ms en escritorio) por todo el JavaScript sin usar, y −19 KB por los duplicados.

**⚠️ Ojo**: dividir paquetes en un sitio de este tamaño puede retrasar componentes interactivos si se cargan demasiado tarde. Hay que medir con datos reales antes y después.

<details><summary>🔬 Auditorías de Lighthouse</summary>

`unused-javascript`, `duplicated-javascript-insight`

</details>

### 11. 📌 Decidir si el `canonical` debe apuntar a la portada

| Prioridad | Dificultad | Tiempo | Quién | Tipo |
|:-:|:-:|:-:|:-:|:-:|
| 📌 Planificar | 🟢 Fácil | ~1 h + decisión | 🤝 Decisión del cliente | Código |

**❓ Qué pasa**: la página `/international` declara como URL canónica `https://www.theguardian.com`, la portada raíz. Lighthouse lo marca como fallo porque, con esa etiqueta, Google entiende que esta página es una copia de la portada y que es la portada la que debe aparecer en los resultados.

**📍 Dónde**: `<link rel="canonical" href="https://www.theguardian.com" />` (`index.html:11`).

**✅ Cómo arreglarlo**: primero, decidir. Si la intención es que las ediciones (internacional, Reino Unido, EE. UU.…) se agrupen bajo la portada raíz, lo que se ve es coherente con esa decisión y no hay que tocarlo, aunque Lighthouse lo marque. Si se quiere que `/international` aparezca en Google por sí misma, el canonical debe apuntar a ella:

```html
<!-- Antes -->
<link rel="canonical" href="https://www.theguardian.com" />
<!-- Después -->
<link rel="canonical" href="https://www.theguardian.com/international" />
```

**📈 Qué se gana**: en Lighthouse, +8 puntos de SEO (de 85 a 92 por sí solo; a 100 junto con #8). El efecto real en Google depende de la estrategia de ediciones.

**⚠️ Ojo**: cambiar el canonical de una página con mucho tráfico puede redistribuir el posicionamiento entre la portada y las ediciones. Es una decisión de SEO, no un arreglo técnico.

<details><summary>🔬 Auditorías de Lighthouse</summary>

`canonical`

</details>

## 🚫 Lo que no haríamos (por ahora)

- **Alargar la caché de los archivos de Sourcepoint** (`cache-insight`, 151 KB en total): solo beneficia a visitas repetidas, y los archivos son de un tercero que decide sus versiones. La parte de fuentes desaparece con #3. Si se quiere abordar, que sea con el proveedor.
- **JavaScript antiguo y sin usar del aviso de consentimiento** (29 KB de `legacy-javascript-insight` y 64 KB de `unused-javascript`): es código de Sourcepoint, un servicio necesario para el consentimiento. Solo se puede pedir al proveedor.
- **`font-display` (20 ms)**: el ahorro es mínimo y se resuelve con #3. Las 28 `@font-face` del propio sitio ya usan `font-display: swap`.
- **Reducir los ~687 KB de CSS en línea**: forman parte de cómo el sitio genera los estilos (emotion). Lighthouse da por buena la auditoría de CSS sin usar, y su efecto en la descarga se reduce mucho con #1. Rehacerlo sería un proyecto de arquitectura.
- **Tiempo hasta interactivo en móvil (7,9 s)**: no forma parte de la nota de rendimiento, y el bloqueo real de la página (TBT) es de 60 ms, en verde.
- **Servidor y caché de página**: el servidor respondió en 19 ms y no hay redirecciones. No hay nada que mejorar ahí.

## 📝 Notas de medición

- 🔬 Medido con Lighthouse 13.6.0 en local, con la conexión móvil lenta que simula Google (150 ms de latencia, unos 1,6 Mbit/s y CPU 4 veces más lenta). Las notas varían ±5 puntos entre ejecuciones y pueden diferir algo de las de pagespeed.web.dev.
- 👥 Lighthouse mide en laboratorio. Los datos de **usuarios reales** (los que Google usa para posicionar) están en el [análisis oficial de PageSpeed Insights](https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fwww.theguardian.com%2Finternational), en el apartado "Descubre lo que experimentan tus usuarios reales". Si la web tiene poco tráfico, Google puede no tener datos.
- ⚠️ Lighthouse avisó de que no podía leer la cabecera `link` ("Unexpected character "," at offset 688"). Es un problema de la propia cabecera (ver #4), no de la ejecución: Lighthouse completó la medición.
- 📰 Es una portada de noticias: el contenido, la foto del LCP y los anuncios cambian a lo largo del día, y hay pruebas A/B activas (la cabecera `x-gu-server-ab-tests` cambió entre dos peticiones seguidas). La edición servida depende del país (`x-gu-edition: eur` en nuestra descarga). Otra medición puede dar resultados algo distintos.
- 🍪 La medición es de una primera visita sin consentimiento guardado, así que incluye el aviso de cookies. Las visitas repetidas descargan menos.
- 📏 KB = 1.024 bytes, como en Lighthouse. Los ahorros en KB y ms son estimaciones de Lighthouse salvo los de #1, que salen de comprimir nosotros el HTML descargado. Las notas previstas de accesibilidad y SEO están calculadas con los pesos de Lighthouse sobre esta medición.
- Solo se ha analizado `https://www.theguardian.com/international`. Las páginas de artículo pueden comportarse de otra forma.

## 🔁 Cómo volver a medir

```bash
python3 ~/.claude/skills/pagespeed-audit/scripts/run_pagespeed.py https://www.theguardian.com/international
```

<details><summary>📖 Glosario</summary>

- **LCP** (*Largest Contentful Paint*): tiempo hasta que se ve el elemento más grande (normalmente la imagen principal o el titular).
- **INP / TBT**: lo rápido que responde la página al tocar o hacer clic. TBT es su equivalente en laboratorio.
- **CLS** (*Cumulative Layout Shift*): cuánto se mueve el contenido mientras carga.
- **FCP** (*First Contentful Paint*): cuándo aparece lo primero en pantalla.
- **TTFB** (*Time To First Byte*): lo que tarda el servidor en empezar a responder.
- **Core Web Vitals**: las tres métricas (LCP, INP, CLS) que Google usa como señal de posicionamiento.

</details>

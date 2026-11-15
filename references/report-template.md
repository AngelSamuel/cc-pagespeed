# Plantilla del informe

El informe lo leen personas no técnicas (clientes, cuentas, dirección) y también desarrolladores. Por eso se organiza en capas: arriba, el veredicto y el plan de acción, que se entienden de un vistazo; abajo, el detalle técnico para quien vaya a hacer los cambios. Los iconos sirven para leer rápido, así que úsalos siempre con el mismo significado (las leyendas de abajo). No los añadas como adorno.

Se escribe en Markdown, que GitHub, VS Code y la mayoría de editores muestran con formato (incluidos los emojis y los bloques `<details>`).

## Leyendas: úsalas siempre igual

**Puntuación** (los mismos umbrales que Google): 🟢 90-100 · 🟠 50-89 · 🔴 0-49

**Veredicto general:** 🟢 Muy bien (todas las notas ≥ 90 y todos los Core Web Vitals en ✅) · 🟠 Mejorable (alguna nota entre 50 y 89 o algún vital en ⚠️) · 🔴 Necesita trabajo (alguna nota < 50 o algún vital en ❌). Evalúa con el peor de móvil y escritorio.

**Core Web Vitals:** ✅ bueno · ⚠️ mejorable · ❌ malo. Clasifica con el valor exacto (`numericValue` en `lab`), no con el redondeado: 2526 ms se muestra como "2,5 s" pero es ⚠️. En ese caso escribe el valor con más precisión ("2,53 s").

| Métrica | ✅ Bueno | ⚠️ Mejorable | ❌ Malo |
|---|---|---|---|
| LCP | ≤ 2,5 s | ≤ 4 s | > 4 s |
| INP (o TBT en laboratorio) | ≤ 200 ms (TBT ≤ 200 ms) | ≤ 500 ms (TBT ≤ 600 ms) | más |
| CLS | ≤ 0,1 | ≤ 0,25 | > 0,25 |
| FCP | ≤ 1,8 s | ≤ 3 s | > 3 s |
| TTFB | ≤ 800 ms | ≤ 1,8 s | más |

**Prioridad**: es una recomendación, no una repetición del orden de Lighthouse:
- 🔥 **Hacer ya**: impacto alto o medio con poco esfuerzo, o algo que hoy perjudica a los usuarios o al SEO.
- 📌 **Planificar**: merece la pena, pero cuesta más (rediseño, cambio de hosting, decisión de negocio). Va a la hoja de ruta.
- 💤 **No prioritario**: Lighthouse lo marca, pero la ganancia es pequeña para lo que cuesta. Explica siempre por qué (por ejemplo: "ahorra 40 ms y la nota ya es 100").

**Dificultad:** 🟢 Fácil (cambio puntual, sin riesgo) · 🟡 Media (varios archivos o requiere probar) · 🔴 Difícil (cambios de arquitectura, terceros, riesgo de romper algo)

**Quién:** 👩‍💻 Desarrollo · 🖥️ Hosting / servidor · ✍️ Contenido / marketing · 🤝 Decisión del cliente

**Tiempo**: estimación aproximada para alguien que conoce el proyecto: `~15 min`, `~1 h`, `½ día`, `1-2 días`. Si es incierto, da un rango.

---

## Estructura

Copia esta estructura y rellénala. Puedes quitar una sección que se quede vacía (por ejemplo, "Fuera del código" si no hay nada), pero mantén el orden.

````markdown
# 🚀 Informe de rendimiento web: <dominio>

> 🌐 <URL> · 📅 <fecha> · 🔬 Lighthouse <versión> (móvil y escritorio)
> 🔎 [Ver el análisis oficial de Google con datos de usuarios reales](<pagespeedWebUrl>)

## 🧭 Resumen

**Veredicto: 🟢 Muy bien / 🟠 Mejorable / 🔴 Necesita trabajo**

2-4 frases en lenguaje llano: cómo está la web, qué es lo que más pesa y qué se gana arreglándolo. Sin jerga; si usas una sigla, explícala.

> 💡 **Lo más importante:** una sola frase con la acción que más impacto tiene.

## 📊 Puntuaciones

| | 📱 Móvil | 🖥️ Escritorio |
|---|:---:|:---:|
| ⚡ Rendimiento | 🟢 97 | 🟢 100 |
| ♿ Accesibilidad | 🟢 97 | 🟢 94 |
| ✅ Buenas prácticas | 🟢 96 | 🟢 96 |
| 🔍 SEO | 🟢 91 | 🟢 91 |

## ⏱️ Core Web Vitals

| Métrica | Qué significa | 📱 Móvil | 🖥️ Escritorio | Objetivo |
|---|---|:---:|:---:|:---:|
| **LCP** | Cuánto tarda en verse el contenido principal | ⚠️ 2,6 s | ✅ 0,5 s | ≤ 2,5 s |
| **TBT** | Cuánto tiempo la página no responde mientras carga | ✅ 0 ms | ✅ 0 ms | ≤ 200 ms |
| **CLS** | Si el contenido "salta" mientras carga | ✅ 0 | ✅ 0 | ≤ 0,1 |
| **FCP** | Cuándo aparece lo primero en pantalla | ✅ 1,3 s | ✅ 0,4 s | ≤ 1,8 s |

Una línea sobre el elemento LCP (qué es: imagen del hero, titular…) y en qué fase se pierde el tiempo (servidor, descubrimiento, descarga, renderizado).

## 📦 Peso de la página

**<total> en <n> peticiones.** Reparto:

```
Imágenes   ████████████████░░░░  2,6 MB  75 %
CSS        █░░░░░░░░░░░░░░░░░░░   26 KB   1 %
HTML       █░░░░░░░░░░░░░░░░░░░   19 KB   1 %
…
```

(Escala: 20 bloques = 100 %, redondeando y con un mínimo de 1 bloque si hay algo, aunque entonces la suma pase de 20. Agrupa los tipos pequeños en "Otros". Referencia: una portada ligera pesa < 1-1,5 MB.)

## 🎯 Plan de acción

| # | Arreglo | Prioridad | Dificultad | Tiempo | Quién | Mejora esperada |
|:-:|---|:-:|:-:|:-:|:-:|---|
| 1 | Redimensionar y comprimir imágenes | 🔥 Hacer ya | 🟢 Fácil | ~1 h | 👩‍💻 | −2,5 MB · LCP móvil −1 s |
| 2 | … | 📌 Planificar | 🟡 Media | ½ día | 🖥️ | … |
| 3 | … | 💤 No prioritario | 🟡 Media | ~2 h | 👩‍💻 | −40 ms |

Numera todos los arreglos seguidos, incluidos los de "Fuera del código", para que se puedan elegir por número.

> ⚡ **Quick wins** (menos de 30 min cada uno, de cualquier tipo): #2, #4, #5. Juntos suben <lo que sea> sin riesgo.

## 🛠️ Detalle de los arreglos

### 1. 🔥 <Título orientado a la acción>

| Prioridad | Dificultad | Tiempo | Quién | Tipo |
|:-:|:-:|:-:|:-:|:-:|
| 🔥 Hacer ya | 🟢 Fácil | ~1 h | 👩‍💻 Desarrollo | Código |

**❓ Qué pasa**: el problema explicado para alguien no técnico, con la cifra que lo demuestra.

**📍 Dónde**: `ruta/archivo.ext:línea` (o el selector, o el recurso).

**✅ Cómo arreglarlo**: pasos concretos. Si es código, un antes/después corto:

```html
<!-- Antes -->
<img src="hero.webp">
<!-- Después -->
<img src="hero.webp" fetchpriority="high">
```

**📈 Qué se gana**: métrica y ahorro estimado.

**⚠️ Ojo**: solo si hay riesgo o cambio visual (colores, fuentes, imágenes que cargan después). Si no hay, omite la línea.

<details><summary>🔬 Auditorías de Lighthouse</summary>

`image-delivery-insight`, `total-byte-weight`

</details>

### 2. …

## 🖥️ Fuera del código

Arreglos de servidor, hosting, CMS o terceros, con instrucciones para la plataforma concreta (detectada en las cabeceras: nginx, Apache, Plesk, Cloudflare…), con el mismo formato de ficha que arriba.

## 🚫 Lo que no haríamos (por ahora)

Cosas que Lighthouse marca y que **no** recomendamos priorizar, con una línea de por qué cada una: poca ganancia, alto riesgo, la métrica ya está en verde, depende de un tercero imprescindible… Esto evita que alguien pierda días persiguiendo un punto de nota.

## 📝 Notas de medición

- 🔬 Medido con Lighthouse <versión> en local, con la conexión móvil lenta que simula Google. Las notas varían ±5 puntos entre ejecuciones y pueden diferir algo de las de pagespeed.web.dev.
- 👥 Lighthouse mide en laboratorio. Los datos de **usuarios reales** (los que Google usa para posicionar) están en el [análisis oficial de PageSpeed Insights](<pagespeedWebUrl>), en el apartado "Descubre lo que experimentan tus usuarios reales". Si la web tiene poco tráfico, Google puede no tener datos.
- Avisos de Lighthouse, páginas no analizadas, otras limitaciones.

## 🔁 Cómo volver a medir

```bash
python3 <ruta real de la skill>/scripts/run_pagespeed.py <URL>
```

<details><summary>📖 Glosario</summary>

- **LCP** (*Largest Contentful Paint*): tiempo hasta que se ve el elemento más grande (normalmente la imagen principal o el titular).
- **INP / TBT**: lo rápido que responde la página al tocar o hacer clic. TBT es su equivalente en laboratorio.
- **CLS** (*Cumulative Layout Shift*): cuánto se mueve el contenido mientras carga.
- **FCP** (*First Contentful Paint*): cuándo aparece lo primero en pantalla.
- **TTFB** (*Time To First Byte*): lo que tarda el servidor en empezar a responder.
- **Core Web Vitals**: las tres métricas (LCP, INP, CLS) que Google usa como señal de posicionamiento.

</details>
````

## Cómo decidir la prioridad

No copies el orden de Lighthouse. Piensa en lo que nota el usuario y en lo que cuesta arreglarlo:

1. ¿Afecta a una métrica que está en ⚠️/❌, sobre todo en móvil? Entonces el impacto es alto.
2. ¿El ahorro es grande (cientos de ms o cientos de KB)? Impacto alto. ¿Son decenas de ms con la métrica ya en ✅? Impacto bajo.
3. Cruza el impacto con la dificultad: alto y fácil → 🔥; alto y difícil → 📌; bajo → 💤, salvo que sea trivial (por ejemplo, una meta descripción que falta: 5 minutos y mejora el SEO, así que 🔥).
4. Accesibilidad y SEO: los fallos que impiden o dificultan usar la web a personas reales (contraste, botones sin nombre, zonas táctiles diminutas, imágenes sin `alt`) o que afectan a cómo aparece en Google (título, descripción, indexación) suelen ser 🔥 porque son baratos. Los fallos más técnicos que no restan nota (`weight: 0`, por ejemplo `label-content-name-mismatch`) van a 📌 o 💤.
5. Las fases del LCP (`lcp.phasesMsObserved`) salen de la carga real sin limitar y suman menos que el LCP simulado. Úsalas para ver en qué proporción se reparte el tiempo, no como valores absolutos.

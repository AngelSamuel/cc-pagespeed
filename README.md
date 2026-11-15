# pagespeed-audit

Skill para Claude que analiza una web con Google PageSpeed Insights / Lighthouse (rendimiento, accesibilidad, buenas prácticas y SEO, en móvil y escritorio), escribe un informe con los arreglos priorizados y, si se lo pides, aplica en tu proyecto los que elijas y vuelve a medir.

## Instalación

**Claude Code** (clonar en la carpeta de skills):

```bash
git clone https://github.com/AngelSamuel/pagespeed.git ~/.claude/skills/pagespeed-audit
```

Para que solo la use un proyecto, clónala en `.claude/skills/pagespeed-audit` dentro de ese proyecto.

**Claude.ai / Claude Desktop**: comprime esta carpeta en un `.zip` y súbelo desde *Ajustes → Capacidades → Skills*.

## Requisitos

- Python 3.8 o superior (solo usa la biblioteca estándar).
- Node.js y Google Chrome: la skill ejecuta **Lighthouse** (el motor de Google PageSpeed Insights) en tu equipo.

No necesita API key ni cuenta: es gratis. Además puede medir `localhost`. Los datos de usuarios reales de Google (CrUX) no salen en Lighthouse local, así que el informe incluye un enlace directo al análisis oficial en [pagespeed.web.dev](https://pagespeed.web.dev) para consultarlos.

## Uso

Abre Claude en la carpeta del proyecto web y pídelo con tus palabras:

> Analiza https://miweb.com con PageSpeed

Claude mide la web, escribe `pagespeed-informe-<dominio>-<fecha>.md` y te pregunta qué arreglos aplicar. No toca el código hasta que elijas, y no hace commit ni despliega sin que se lo pidas.

El informe empieza con un veredicto y un **plan de acción** en tabla: cada arreglo con su prioridad (🔥 hacer ya · 📌 planificar · 💤 no prioritario), dificultad (🟢 🟡 🔴), tiempo estimado, quién lo hace y qué se gana. Después vienen las fichas detalladas de cada arreglo, lo que *no* merece la pena hacer, las notas de medición y un glosario.

Si quieres ejecutar solo la medición:

```bash
python3 scripts/run_pagespeed.py https://miweb.com --out ./pagespeed-report
python3 scripts/run_pagespeed.py http://localhost:3000 --strategy mobile
```

## Contenido

- `SKILL.md`: instrucciones para Claude (flujo y plantilla del informe).
- `scripts/run_pagespeed.py`: medición con Lighthouse (móvil y escritorio); genera `summary.json`.
- `references/report-template.md`: plantilla del informe, leyendas de iconos y criterios de prioridad.
- `references/audit-fixes.md`: causa y solución de las auditorías habituales de Lighthouse.

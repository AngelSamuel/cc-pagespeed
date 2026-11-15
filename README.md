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
- Uno de estos dos:
  - **Node.js y Google Chrome**: se usa Lighthouse en local. Es gratis, no necesita key y también mide `localhost`.
  - **Una API key de PageSpeed** (gratuita): da además datos de usuarios reales (CrUX). Créala en https://developers.google.com/speed/docs/insights/v5/get-started y añádela a tu shell:
    ```bash
    export PAGESPEED_API_KEY=tu_key
    ```

Sin key, Google da cuota 0 a la API. Por eso, si no hay key, la skill usa Lighthouse local automáticamente.

## Uso

Abre Claude en la carpeta del proyecto web y pídelo con tus palabras:

> Analiza https://miweb.com con PageSpeed

Claude mide la web, escribe `pagespeed-informe-<dominio>-<fecha>.md` y te pregunta qué arreglos aplicar. No toca el código hasta que elijas, y no hace commit ni despliega sin que se lo pidas.

Si quieres ejecutar solo la medición:

```bash
python3 scripts/run_pagespeed.py https://miweb.com --out ./pagespeed-report
python3 scripts/run_pagespeed.py http://localhost:3000 --engine local --strategy mobile
```

## Contenido

- `SKILL.md`: instrucciones para Claude (flujo y plantilla del informe).
- `scripts/run_pagespeed.py`: medición con la API de PageSpeed v5 o con Lighthouse local; genera `summary.json`.
- `references/audit-fixes.md`: causa y solución de las auditorías habituales de Lighthouse.

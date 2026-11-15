#!/usr/bin/env python3
"""Auditoría de rendimiento con PageSpeed Insights (API v5) o Lighthouse local.

Solo usa la biblioteca estándar de Python, así funciona en cualquier equipo.

Motores (--engine):
    api    API de Google PageSpeed Insights. Necesita PAGESPEED_API_KEY
           (gratuita): sin key Google da cuota 0. Incluye datos de campo
           (usuarios reales, CrUX). No puede analizar localhost.
    local  Lighthouse en este equipo vía npx (gratis, sin key). Necesita Node
           y Chrome. Mismo motor que PageSpeed, sin datos de campo. Sí puede
           analizar localhost.
    auto   (por defecto) api si hay key; si no hay key, o la API falla por
           cuota, cae a local.

Uso:
    python3 run_pagespeed.py https://ejemplo.com --out ./pagespeed-report
    python3 run_pagespeed.py http://localhost:3000 --engine local

Salida en --out:
    raw-<strategy>.json   respuesta completa de la API (por si hace falta un detalle)
    summary.json          resumen de ambas estrategias, pensado para leerlo Claude
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
CATEGORIES = ["PERFORMANCE", "ACCESSIBILITY", "BEST_PRACTICES", "SEO"]
LIGHTHOUSE_PKG = "lighthouse@13.6.0"  # versión fijada: lo que se ejecuta es predecible
MAX_ITEMS = 8  # elementos por auditoría en el resumen
SKIP_MODES = {"notApplicable", "manual"}

FIELD_METRICS = {
    "LARGEST_CONTENTFUL_PAINT_MS": "LCP (ms)",
    "INTERACTION_TO_NEXT_PAINT": "INP (ms)",
    "CUMULATIVE_LAYOUT_SHIFT_SCORE": "CLS (x100)",
    "FIRST_CONTENTFUL_PAINT_MS": "FCP (ms)",
    "EXPERIMENTAL_TIME_TO_FIRST_BYTE": "TTFB (ms)",
}
LAB_METRICS = [
    "first-contentful-paint",
    "largest-contentful-paint",
    "total-blocking-time",
    "cumulative-layout-shift",
    "speed-index",
    "interactive",
]


class QuotaError(Exception):
    pass


def is_local_host(url):
    host = urllib.parse.urlparse(url).hostname or ""
    return host in ("localhost", "127.0.0.1", "::1") or host.endswith((".localhost", ".test", ".local"))


def run_local(url, strategy, locale):
    """Ejecuta Lighthouse en local y devuelve la respuesta con forma de la API."""
    npx = shutil.which("npx")
    if not npx:
        raise SystemExit(
            "ERROR: no hay API key de PageSpeed y tampoco Node.js para usar Lighthouse en local.\n"
            "Opciones: 1) instala Node.js (https://nodejs.org) y Google Chrome, o\n"
            "2) crea una API key gratuita en https://developers.google.com/speed/docs/insights/v5/get-started "
            "y expórtala como PAGESPEED_API_KEY."
        )
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "lhr.json")
        cmd = [npx, "--yes", LIGHTHOUSE_PKG, url,
               "--output=json", f"--output-path={out}", "--quiet",
               "--only-categories=performance,accessibility,best-practices,seo",
               f"--locale={locale}", "--chrome-flags=--headless=new --no-first-run"]
        if strategy == "desktop":
            cmd.append("--preset=desktop")
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode != 0 or not os.path.exists(out):
            err = (r.stderr or r.stdout or "").strip()[-1200:]
            hint = ""
            if "chrome" in err.lower() and ("not found" in err.lower() or "no chrome" in err.lower()):
                hint = "\nParece que falta Google Chrome: instálalo o exporta CHROME_PATH con su ruta."
            raise SystemExit(f"ERROR ejecutando Lighthouse local ({strategy}):\n{err}{hint}")
        with open(out, encoding="utf-8") as f:
            lhr = json.load(f)
    return {"id": url, "lighthouseResult": lhr}


def fetch(url, strategy, key, locale, retries=2):
    params = [("url", url), ("strategy", strategy.upper()), ("locale", locale)]
    params += [("category", c) for c in CATEGORIES]
    if key:
        params.append(("key", key))
    full = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(full, headers={"User-Agent": "pagespeed-audit-skill"})

    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            try:
                msg = json.loads(body)["error"]["message"]
            except Exception:
                msg = body[:500]
            if e.code == 429:
                if attempt < retries:
                    time.sleep(15 * (attempt + 1))
                    continue
                raise QuotaError(msg)
            if e.code >= 500 and attempt < retries:
                time.sleep(5)
                continue
            raise SystemExit(f"ERROR {e.code} ({strategy}): {msg}")
        except urllib.error.URLError as e:
            if attempt < retries:
                time.sleep(5)
                continue
            raise SystemExit(f"ERROR de red ({strategy}): {e.reason}")


def trim_item(item):
    """Se queda con los campos útiles para localizar el problema en el código."""
    out = {}
    for k in ("url", "wastedBytes", "wastedMs", "totalBytes", "transferSize",
              "cacheLifetimeMs", "label", "source", "duration", "groupLabel"):
        v = item.get(k)
        if v not in (None, ""):
            if isinstance(v, dict):  # p. ej. source-location
                v = {kk: v.get(kk) for kk in ("url", "line", "column") if v.get(kk) is not None}
            out[k] = round(v) if isinstance(v, float) else v
    if item.get("description"):  # p. ej. el texto de errors-in-console
        out["description"] = str(item["description"])[:240]
    loc = item.get("sourceLocation")
    if isinstance(loc, dict) and loc.get("url"):
        out["sourceLocation"] = {k: loc.get(k) for k in ("url", "line", "column") if loc.get(k) is not None}
    node = item if item.get("type") == "node" else item.get("node")
    if isinstance(node, dict):
        n = {k: node.get(k) for k in ("selector", "snippet", "nodeLabel") if node.get(k)}
        rect = node.get("boundingRect") or {}
        if rect.get("width"):
            n["displayed"] = f"{round(rect['width'])}x{round(rect.get('height', 0))}"
        if n:
            out["node"] = n
    sub = (item.get("subItems") or {}).get("items") or []
    reasons = [x.get("reason") for x in sub if isinstance(x, dict) and x.get("reason")]
    if reasons:
        out["reasons"] = [r[:200] for r in reasons[:3]]
    return out


def flatten_items(details):
    """Lighthouse 13 anida detalles: 'list' contiene tablas, 'checklist' usa un dict."""
    items = details.get("items")
    if isinstance(items, dict):  # checklist: {clave: {label, value}}
        return [{"label": v.get("label"), "source": "ok" if v.get("value") else "FALTA"}
                for v in items.values() if isinstance(v, dict)]
    out = []
    for it in items or []:
        if isinstance(it, dict) and it.get("type") in ("table", "opportunity", "list", "checklist"):
            out.extend(flatten_items(it))
        elif isinstance(it, dict) and it.get("type") == "list-section":
            v = it.get("value") or {}
            if v.get("type") == "network-tree":
                out.extend(longest_chain(v.get("chains") or {}))
        elif isinstance(it, dict):
            out.append(it)
    return out


def longest_chain(chains):
    """Devuelve la cadena crítica más larga como lista de pasos."""
    steps = []
    level = chains
    while level:
        key = next((k for k, c in level.items() if c.get("isLongest")), next(iter(level)))
        c = level[key]
        steps.append({"url": c.get("url"), "duration": round(c.get("navStartToEndTime", 0)),
                      "transferSize": c.get("transferSize")})
        level = c.get("children") or {}
    return steps


def summarize_audit(audit):
    details = audit.get("details") or {}
    items = flatten_items(details)
    s = {
        "id": audit["id"],
        "title": audit.get("title"),
        "score": audit.get("score"),
        "displayValue": audit.get("displayValue"),
        "description": (audit.get("description") or "")[:400],
    }
    savings = audit.get("metricSavings") or {}
    savings = {k: v for k, v in savings.items() if v}
    if savings:
        s["metricSavings"] = savings
    if details.get("overallSavingsMs"):
        s["overallSavingsMs"] = round(details["overallSavingsMs"])
    if details.get("overallSavingsBytes"):
        s["overallSavingsBytes"] = round(details["overallSavingsBytes"])
    if items:
        s["items"] = [t for t in (trim_item(i) for i in items[:MAX_ITEMS] if isinstance(i, dict)) if t]
        if len(items) > MAX_ITEMS:
            s["moreItems"] = len(items) - MAX_ITEMS
    return s


def summarize(data):
    lh = data.get("lighthouseResult", {})
    audits = lh.get("audits", {})
    res = {
        "finalUrl": lh.get("finalDisplayedUrl") or lh.get("finalUrl"),
        "lighthouseVersion": lh.get("lighthouseVersion"),
        "fetchTime": lh.get("fetchTime"),
        "runWarnings": lh.get("runWarnings") or [],
        "scores": {},
        "field": None,
        "lab": {},
        "issues": {},
    }

    le = data.get("loadingExperience") or {}
    if le.get("metrics"):
        res["field"] = {
            "scope": "página" if le.get("id") == data.get("id") and not le.get("origin_fallback") else "origen",
            "overall": le.get("overall_category"),
            "metrics": {
                label: {"p75": m.get("percentile"), "category": m.get("category")}
                for key, label in FIELD_METRICS.items()
                if (m := le["metrics"].get(key))
            },
        }

    lcp = audits.get("lcp-breakdown-insight") or audits.get("lcp-phases-insight") or {}
    lcp_items = flatten_items(lcp.get("details") or {})
    nodes = [i for i in lcp_items if i.get("type") == "node"]
    phases = {i.get("label"): round(i["duration"]) for i in lcp_items if i.get("duration") is not None}
    if nodes or phases:
        res["lcp"] = {"element": trim_item(nodes[0]).get("node") if nodes else None, "phasesMs": phases}

    for mid in LAB_METRICS:
        a = audits.get(mid)
        if a:
            res["lab"][a.get("title", mid)] = {"value": a.get("displayValue"), "score": a.get("score")}

    for cid, cat in (lh.get("categories") or {}).items():
        score = cat.get("score")
        res["scores"][cid] = None if score is None else round(score * 100)
        failing = []
        seen = set()
        for ref in cat.get("auditRefs", []):
            if ref.get("group") == "metrics" or ref["id"] in LAB_METRICS:
                continue
            a = audits.get(ref["id"])
            if not a or a.get("scoreDisplayMode") in SKIP_MODES or a["id"] in seen:
                continue
            sc = a.get("score")
            has_savings = any((a.get("metricSavings") or {}).values())
            if (sc is not None and sc < 0.9) or (sc is None and has_savings):
                seen.add(a["id"])
                entry = summarize_audit(a)
                entry["weight"] = ref.get("weight", 0)
                failing.append(entry)
        failing.sort(key=lambda x: (-(x.get("weight") or 0),
                                    -(x.get("overallSavingsMs") or 0),
                                    x.get("score") if x.get("score") is not None else 1))
        res["issues"][cid] = failing
    return res


def main():
    p = argparse.ArgumentParser(description="Auditoría PageSpeed Insights (v5)")
    p.add_argument("url")
    p.add_argument("--engine", choices=["auto", "api", "local"], default="auto")
    p.add_argument("--strategy", choices=["mobile", "desktop", "both"], default="both")
    p.add_argument("--key", default=os.environ.get("PAGESPEED_API_KEY"))
    p.add_argument("--locale", default="es")
    p.add_argument("--out", default="./pagespeed-report")
    a = p.parse_args()

    url = a.url if a.url.startswith(("http://", "https://")) else "https://" + a.url
    engine = a.engine
    if engine == "auto":
        engine = "api" if a.key and not is_local_host(url) else "local"
    if engine == "api" and is_local_host(url):
        raise SystemExit(
            "ERROR: la API de PageSpeed se ejecuta en servidores de Google y no puede acceder a "
            "localhost ni a dominios locales. Usa --engine local o una URL pública."
        )
    if engine == "api" and not a.key:
        print("Aviso: sin PAGESPEED_API_KEY Google suele dar cuota 0; probablemente fallará.", file=sys.stderr)

    os.makedirs(a.out, exist_ok=True)
    strategies = ["mobile", "desktop"] if a.strategy == "both" else [a.strategy]
    summary = {"url": url, "engine": engine, "strategies": {}}

    for st in strategies:
        print(f"Analizando {url} ({st}, motor {engine})… puede tardar hasta un minuto.", file=sys.stderr)
        if engine == "api":
            try:
                data = fetch(url, st, a.key, a.locale)
            except QuotaError as e:
                if a.engine == "api":
                    raise SystemExit(
                        f"ERROR 429 ({st}): cuota de la API agotada ({e}).\n"
                        "Prueba --engine local, o espera / revisa la cuota de tu API key."
                    )
                print("La API no tiene cuota; continúo con Lighthouse local.", file=sys.stderr)
                engine = summary["engine"] = "local"
        if engine == "local":
            data = run_local(url, st, a.locale)
        with open(os.path.join(a.out, f"raw-{st}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        summary["strategies"][st] = summarize(data)

    path = os.path.join(a.out, "summary.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)

    for st, s in summary["strategies"].items():
        sc = ", ".join(f"{k}={v}" for k, v in s["scores"].items())
        n = sum(len(v) for v in s["issues"].values())
        print(f"{st}: {sc} | {n} auditorías por mejorar", file=sys.stderr)
    print(path)


if __name__ == "__main__":
    main()

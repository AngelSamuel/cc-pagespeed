#!/usr/bin/env python3
"""Auditoría web con Lighthouse (el motor de Google PageSpeed Insights) en local.

Gratis y sin API key: ejecuta Lighthouse con npx y Chrome en headless.
Requisitos: Python 3.8+, Node.js y Google Chrome. Puede medir URLs públicas
y también localhost.

Uso:
    python3 run_pagespeed.py https://ejemplo.com --out ./pagespeed-report
    python3 run_pagespeed.py http://localhost:3000 --strategy mobile

Salida en --out:
    raw-<strategy>.json   informe completo de Lighthouse (por si hace falta un detalle)
    summary.json          resumen de ambas estrategias, pensado para leerlo Claude
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

LIGHTHOUSE_PKG = "lighthouse@13.6.0"  # versión fijada: lo que se ejecuta es predecible
MAX_ITEMS = 15  # elementos por auditoría en el resumen
SKIP_MODES = {"notApplicable", "manual"}

LAB_METRICS = [
    "first-contentful-paint",
    "largest-contentful-paint",
    "total-blocking-time",
    "cumulative-layout-shift",
    "speed-index",
    "interactive",
]


def run_local(url, strategy, locale):
    """Ejecuta Lighthouse en local y devuelve el informe (LHR)."""
    npx = shutil.which("npx")
    if not npx:
        raise SystemExit(
            "ERROR: no se encuentra Node.js (npx), necesario para ejecutar Lighthouse.\n"
            "Instala Node.js (https://nodejs.org) y Google Chrome y vuelve a intentarlo.\n"
            "Mientras tanto puedes analizar la web a mano en https://pagespeed.web.dev"
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
    return lhr


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
        if node.get("explanation"):  # p. ej. colores y ratio en color-contrast
            n["explanation"] = str(node["explanation"])[:300]
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


def summarize(lh):
    audits = lh.get("audits", {})
    res = {
        "finalUrl": lh.get("finalDisplayedUrl") or lh.get("finalUrl"),
        "lighthouseVersion": lh.get("lighthouseVersion"),
        "fetchTime": lh.get("fetchTime"),
        "runWarnings": lh.get("runWarnings") or [],
        "throttling": (lh.get("configSettings") or {}).get("throttlingMethod"),
        "scores": {},
        "lab": {},
        "page": {},
        "issues": {},
    }

    lcp = audits.get("lcp-breakdown-insight") or audits.get("lcp-phases-insight") or {}
    lcp_items = flatten_items(lcp.get("details") or {})
    nodes = [i for i in lcp_items if i.get("type") == "node"]
    phases = {i.get("label"): round(i["duration"]) for i in lcp_items if i.get("duration") is not None}
    if nodes or phases:
        # Ojo: las fases salen de la traza observada (sin la limitación simulada), así que
        # suman menos que el LCP simulado. Sirven para ver la proporción, no el valor absoluto.
        res["lcp"] = {"element": trim_item(nodes[0]).get("node") if nodes else None,
                      "phasesMsObserved": phases}

    weight = audits.get("total-byte-weight") or {}
    if weight.get("numericValue"):
        res["page"]["totalKB"] = round(weight["numericValue"] / 1024)
    reqs = ((audits.get("network-requests") or {}).get("details") or {}).get("items") or []
    if reqs:
        res["page"]["requests"] = len(reqs)
        by_type = {}
        for r in reqs:
            t = r.get("resourceType") or "Other"
            by_type[t] = by_type.get(t, 0) + (r.get("transferSize") or 0)
        top = sorted(reqs, key=lambda r: -(r.get("transferSize") or 0))[:15]
        res["page"]["largestRequests"] = [
            {"url": (r.get("url") or "")[:200], "type": r.get("resourceType"),
             "kb": round((r.get("transferSize") or 0) / 1024), "priority": r.get("priority"),
             "protocol": r.get("protocol")} for r in top]
        res["page"]["kbByType"] = {k: round(v / 1024) for k, v in sorted(by_type.items(), key=lambda x: -x[1]) if v}

    for mid in LAB_METRICS:
        a = audits.get(mid)
        if a:
            res["lab"][a.get("title", mid)] = {"id": mid, "value": a.get("displayValue"),
                                               "numericValue": a.get("numericValue"), "score": a.get("score")}

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
        # Lo que está bien también sirve: descarta causas y da contexto al informe.
        res.setdefault("passed", {})[cid] = [
            audits[r["id"]].get("title") for r in cat.get("auditRefs", [])
            if r["id"] in audits and audits[r["id"]].get("score") == 1
            and audits[r["id"]].get("scoreDisplayMode") not in SKIP_MODES | {"informative"}
            and r.get("group") != "metrics" and r["id"] not in LAB_METRICS][:25]
    return res


def main():
    p = argparse.ArgumentParser(description="Auditoría web con Lighthouse")
    p.add_argument("url")
    p.add_argument("--strategy", choices=["mobile", "desktop", "both"], default="both")
    p.add_argument("--locale", default="es")
    p.add_argument("--out", default="./pagespeed-report")
    a = p.parse_args()

    url = a.url if a.url.startswith(("http://", "https://")) else "https://" + a.url
    host = urllib.parse.urlparse(url).hostname or ""
    is_local = host in ("localhost", "127.0.0.1", "::1") or host.endswith((".localhost", ".test", ".local"))

    os.makedirs(a.out, exist_ok=True)
    strategies = ["mobile", "desktop"] if a.strategy == "both" else [a.strategy]
    summary = {
        "url": url,
        "engine": f"Lighthouse {LIGHTHOUSE_PKG.split('@')[1]} (local)",
        # Enlace al análisis oficial de Google: muestra los datos de usuarios reales (CrUX),
        # que Lighthouse local no puede obtener.
        "pagespeedWebUrl": None if is_local else
            "https://pagespeed.web.dev/analysis?url=" + urllib.parse.quote(url, safe=""),
        "strategies": {},
    }

    for st in strategies:
        print(f"Analizando {url} ({st})… puede tardar hasta un minuto.", file=sys.stderr)
        lhr = run_local(url, st, a.locale)
        with open(os.path.join(a.out, f"raw-{st}.json"), "w", encoding="utf-8") as f:
            json.dump(lhr, f, ensure_ascii=False)
        summary["strategies"][st] = summarize(lhr)

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

"""Genera los diagramas del repositorio a partir de una especificacion declarativa.

La fuente de verdad es diagrams/architecture.json: describe grupos, nodos y
aristas con coordenadas explicitas. De ahi salen tres formatos por vista:

  diagrams/rendered/<vista>.svg   vectorial, es el que se referencia en el README
  diagrams/rendered/<vista>.png   exportado con Chrome headless, para previsualizar
  diagrams/rendered/<vista>.mmd   mermaid, por si se quiere embeber en linea

Uso:
    python scripts/render_diagrams.py              solo SVG y mermaid
    python scripts/render_diagrams.py --render-png ademas exporta PNG
    python scripts/render_diagrams.py --check      falla si algo esta desactualizado
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
import struct
import subprocess
import sys
import tempfile
import textwrap
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "diagrams" / "architecture.json"
OUT = ROOT / "diagrams" / "rendered"

WIDTH = 1920
HEIGHT = 1080
NODE_WIDTH = 216
NODE_HEIGHT = 150

ICON_COLORS = {
    "actor": "#334155",
    "api": "#2563eb",
    "queue": "#7c3aed",
    "event_bus": "#7c3aed",
    "database": "#ca8a04",
    "object_store": "#ca8a04",
    "failure": "#dc2626",
    "review": "#dc2626",
    "monitor": "#0891b2",
    "security": "#059669",
    "branch": "#2563eb",
    "release": "#059669",
    "hotfix": "#dc2626",
    "merge": "#7c3aed",
    "check": "#0891b2",
}

ICON_SYMBOLS = {
    "actor": "USER",
    "api": "API",
    "queue": "QUEUE",
    "event_bus": "EVENT",
    "database": "DB",
    "object_store": "DATA",
    "failure": "ERR",
    "review": "QA",
    "monitor": "OBS",
    "security": "SEC",
    "branch": "GIT",
    "release": "TAG",
    "hotfix": "FIX",
    "merge": "MERGE",
    "check": "CHECK",
}

BADGE_COLORS = {
    "IMPLEMENTED": ("#dcfce7", "#166534"),
    "PLANNED": ("#fef3c7", "#92400e"),
    "EXTERNAL": ("#e2e8f0", "#334155"),
    "LOCAL": ("#dbeafe", "#1e40af"),
    "MAIN": ("#dcfce7", "#166534"),
    "DEVELOP": ("#dbeafe", "#1e40af"),
    "FEATURE": ("#ede9fe", "#5b21b6"),
    "FIX": ("#fee2e2", "#991b1b"),
    "DOCS": ("#e2e8f0", "#334155"),
}


def _lines(value) -> list[str]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _wrapped(value, width: int, maximum: int) -> list[str]:
    result: list[str] = []
    for original in _lines(value):
        result.extend(textwrap.wrap(str(original), width=width, break_long_words=False) or [""])
    return result[:maximum]


# --- mermaid -----------------------------------------------------------------


def _node_mermaid(node: dict) -> str:
    text = "<br/>".join([*_lines(node["label"]), *_lines(node.get("detail"))])
    shape = node.get("kind", "service")
    if shape == "actor":
        return f'    {node["id"]}(["{text}"])'
    if shape in {"database", "object_store"}:
        return f'    {node["id"]}[("{text}")]'
    if shape in {"queue", "event_bus"}:
        return f'    {node["id"]}{{{{"{text}"}}}}'
    if shape in {"failure", "review"}:
        return f'    {node["id"]}>"{text}"]'
    return f'    {node["id"]}["{text}"]'


def mermaid(view: dict) -> str:
    rows = ["flowchart LR"]
    assigned: set[str] = set()
    for group in view.get("groups", []):
        rows.append(f'  subgraph {group["id"]}["{group["title"]}"]')
        rows.append("    direction TB")
        for node in view["nodes"]:
            if node.get("group") == group["id"]:
                rows.append(_node_mermaid(node))
                assigned.add(str(node["id"]))
        rows.append("  end")
    for node in view["nodes"]:
        if str(node["id"]) not in assigned:
            rows.append(_node_mermaid(node))
    for edge in view["edges"]:
        connector = "-.->" if edge.get("style") == "dashed" else "-->"
        rows.append(f'  {edge["from"]} {connector}|"{edge["label"]}"| {edge["to"]}')
    return "\n".join(rows) + "\n"


# --- svg ---------------------------------------------------------------------


def _icon(node: dict, x: float, y: float) -> str:
    kind = str(node.get("kind", "service"))
    color = ICON_COLORS.get(kind, "#2563eb")
    symbol = ICON_SYMBOLS.get(kind, "APP")
    size = 11 if len(symbol) <= 5 else 9
    return (
        f'<circle cx="{x + 34}" cy="{y + 34}" r="30" fill="{color}" opacity="0.12"/>'
        f'<circle cx="{x + 34}" cy="{y + 34}" r="23" fill="none" stroke="{color}" stroke-width="3"/>'
        f'<text x="{x + 34}" y="{y + 38}" text-anchor="middle" font-size="{size}"'
        f' font-weight="700" fill="{color}">{symbol}</text>'
    )


def _badge(status: str, x: float, y: float) -> str:
    fill, foreground = BADGE_COLORS.get(status, BADGE_COLORS["DOCS"])
    width = max(62, len(status) * 6.2 + 15)
    return (
        f'<rect x="{x - width}" y="{y}" width="{width}" height="21" rx="10" fill="{fill}"/>'
        f'<text x="{x - width / 2}" y="{y + 14}" text-anchor="middle" font-size="9"'
        f' font-weight="700" fill="{foreground}">{html.escape(status)}</text>'
    )


def _node_svg(node: dict) -> str:
    x, y = float(node["x"]), float(node["y"])
    status = str(node.get("status", "DOCS"))
    border = "#ef4444" if node.get("kind") in {"failure", "hotfix"} else "#94a3b8"
    parts = [
        f'<g id="node-{html.escape(str(node["id"]))}">',
        f'<rect x="{x}" y="{y}" width="{NODE_WIDTH}" height="{NODE_HEIGHT}" rx="14"'
        f' fill="#ffffff" stroke="{border}" stroke-width="2" filter="url(#shadow)"/>',
        _badge(status, x + NODE_WIDTH - 8, y + 7),
        _icon(node, x + 12, y + 35),
    ]
    label_lines = _wrapped(node["label"], 19, 3)
    detail_lines = _wrapped(node.get("detail"), 34, 3)
    label_y = y + 49
    for index, line in enumerate(label_lines):
        parts.append(
            f'<text x="{x + 75}" y="{label_y + index * 15}" font-size="12"'
            f' font-weight="700" fill="#0f172a">{html.escape(line)}</text>'
        )
    detail_y = max(y + 108, label_y + len(label_lines) * 15 + 7)
    for index, line in enumerate(detail_lines):
        parts.append(
            f'<text x="{x + 12}" y="{detail_y + index * 13}" font-size="9.5"'
            f' fill="#475569">{html.escape(line)}</text>'
        )
    parts.append("</g>")
    return "".join(parts)


def _edge_points(source: dict, target: dict) -> tuple[float, float, float, float]:
    sx, sy = float(source["x"]), float(source["y"])
    tx, ty = float(target["x"]), float(target["y"])
    if tx >= sx + NODE_WIDTH:
        return sx + NODE_WIDTH, sy + NODE_HEIGHT / 2, tx, ty + NODE_HEIGHT / 2
    if tx + NODE_WIDTH <= sx:
        return sx, sy + NODE_HEIGHT / 2, tx + NODE_WIDTH, ty + NODE_HEIGHT / 2
    if ty >= sy:
        return sx + NODE_WIDTH / 2, sy + NODE_HEIGHT, tx + NODE_WIDTH / 2, ty
    return sx + NODE_WIDTH / 2, sy, tx + NODE_WIDTH / 2, ty + NODE_HEIGHT


def _edge_svg(edge: dict, nodes: dict) -> tuple[str, str]:
    source, target = nodes[str(edge["from"])], nodes[str(edge["to"])]
    sx, sy, tx, ty = _edge_points(source, target)
    if abs(tx - sx) > abs(ty - sy):
        middle = (sx + tx) / 2
        path = f"M {sx} {sy} H {middle} V {ty} H {tx}"
        label_x, label_y = middle, min(sy, ty) + abs(ty - sy) / 2 - 8
    else:
        middle = (sy + ty) / 2
        path = f"M {sx} {sy} V {middle} H {tx} V {ty}"
        label_x, label_y = min(sx, tx) + abs(tx - sx) / 2, middle - 8
    dashed = ' stroke-dasharray="8 7"' if edge.get("style") == "dashed" else ""
    color = "#64748b" if edge.get("style") == "dashed" else "#334155"
    label = html.escape(str(edge["label"]))
    return (
        f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2"{dashed}'
        f' marker-end="url(#arrow)"/>',
        f'<text x="{label_x}" y="{label_y}" text-anchor="middle" font-size="11"'
        f' font-weight="600" fill="#334155" stroke="#ffffff" stroke-width="5"'
        f' paint-order="stroke">{label}</text>',
    )


def _legend(view: dict) -> str:
    entries = view.get("legend", [])
    if not entries:
        return ""
    parts = ['<g font-family="Arial, sans-serif" font-size="11">']
    x = 1920 - 60 - sum(len(str(e["label"])) * 6.6 + 34 for e in entries)
    for entry in entries:
        fill = BADGE_COLORS.get(str(entry["status"]), BADGE_COLORS["DOCS"])[0]
        parts.append(f'<rect x="{x}" y="1016" width="14" height="14" rx="4" fill="{fill}"/>')
        parts.append(f'<text x="{x + 20}" y="1028">{html.escape(str(entry["label"]))}</text>')
        x += len(str(entry["label"])) * 6.6 + 34
    parts.append("</g>")
    return "".join(parts)


def svg(view: dict, project: str) -> str:
    nodes = {str(node["id"]): node for node in view["nodes"]}
    groups = "".join(
        f'<rect x="{g["x"]}" y="{g["y"]}" width="{g["width"]}" height="{g["height"]}"'
        f' rx="18" fill="{g["color"]}" fill-opacity="0.52" stroke="#94a3b8" stroke-width="1.5"/>'
        f'<text x="{float(g["x"]) + 15}" y="{float(g["y"]) + 27}" font-size="15"'
        f' font-weight="700" fill="#334155">{html.escape(str(g["title"]))}</text>'
        for g in view.get("groups", [])
    )
    edges = [_edge_svg(edge, nodes) for edge in view["edges"]]
    paths = "".join(part[0] for part in edges)
    labels = "".join(part[1] for part in edges)
    cards = "".join(_node_svg(node) for node in view["nodes"])
    title = f'{project} · {view["name"]}'
    subtitle = html.escape(str(view.get("subtitle", "")))
    footer = html.escape(str(view.get("footer", "")))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title>
<desc id="desc">{subtitle}</desc>
<defs>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.14"/></filter>
  <marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L0,9 L8,4.5 z" fill="#334155"/></marker>
</defs>
<rect width="100%" height="100%" fill="#f8fafc"/>
<text x="48" y="48" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="#0f172a">{html.escape(title)}</text>
<text x="48" y="78" font-family="Arial, sans-serif" font-size="15" fill="#475569">{subtitle}</text>
<g font-family="Arial, sans-serif">{groups}{paths}{cards}{labels}</g>
<rect x="48" y="1003" width="1824" height="48" rx="12" fill="#e2e8f0"/>
<text x="68" y="1033" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#0f172a">{footer}</text>
{_legend(view)}
</svg>
"""


# --- png ---------------------------------------------------------------------


def _chrome() -> str | None:
    for candidate in (
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chrome"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ):
        if candidate and Path(candidate).exists():
            return str(candidate)
    return None


def _render_png(svg_path: Path, png_path: Path) -> None:
    browser = _chrome()
    if not browser:
        raise RuntimeError("no se encontro Chrome para exportar PNG")
    png_path.parent.mkdir(parents=True, exist_ok=True)
    if png_path.exists():
        png_path.unlink()
    # ignore_cleanup_errors: en Windows Chrome mantiene el lockfile del perfil
    # un instante despues de terminar, y el borrado fallaria sin motivo.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
        command = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--user-data-dir={profile}",
            f"--window-size={WIDTH},{HEIGHT}",
            f"--screenshot={png_path.resolve()}",
            svg_path.resolve().as_uri(),
        ]
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        exportado = False
        deadline = time.time() + 120
        while time.time() < deadline:
            if png_path.exists() and png_path.stat().st_size > 1_000:
                exportado = True
                break
            time.sleep(0.4)
        process.terminate()
        try:
            process.wait(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
    if exportado:
        return
    raise RuntimeError(f"el navegador no exporto el PNG: {png_path}")


def _png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[16:24]
    return struct.unpack(">II", data)


# --- cli ---------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render-png", action="store_true", help="exportar tambien PNG")
    parser.add_argument("--check", action="store_true", help="fallar si hay salidas desactualizadas")
    args = parser.parse_args()

    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    project = spec["project"]
    OUT.mkdir(parents=True, exist_ok=True)
    stale: list[str] = []

    for name, view in spec["views"].items():
        view = {**view, "name": view.get("name", name)}
        svg_path = OUT / f"{name}.svg"
        mmd_path = OUT / f"{name}.mmd"
        png_path = OUT / f"{name}.png"

        svg_text = svg(view, project)
        mmd_text = mermaid(view)

        if args.check:
            for path, expected in ((svg_path, svg_text), (mmd_path, mmd_text)):
                if not path.exists() or path.read_text(encoding="utf-8") != expected:
                    stale.append(str(path.relative_to(ROOT)))
            if not png_path.exists() or _png_size(png_path) != (WIDTH, HEIGHT):
                stale.append(str(png_path.relative_to(ROOT)))
            continue

        svg_path.write_text(svg_text, encoding="utf-8")
        mmd_path.write_text(mmd_text, encoding="utf-8")
        print(f"escrito {svg_path.relative_to(ROOT)}")
        if args.render_png:
            _render_png(svg_path, png_path)
            print(f"escrito {png_path.relative_to(ROOT)}")

    if args.check:
        if stale:
            print("diagramas desactualizados:")
            for item in stale:
                print(f"  {item}")
            sys.exit(1)
        print("los diagramas estan al dia")


if __name__ == "__main__":
    main()

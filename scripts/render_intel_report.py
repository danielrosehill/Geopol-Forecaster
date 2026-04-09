"""Render a Geopol Forecaster run as an intelligence-style PDF report.

Usage:
    uv run python scripts/render_intel_report.py reports/<RUN_ID>

Produces `<RUN_ID>/intel_report.pdf` styled with:
    - cover page with classification banner, title, question, run metadata
    - BLUF page
    - body from chairman_report.md (pandoc → typst), page-broken by section
    - colophon / methodology appendix with repo and stack attribution

Requires: pandoc, typst on PATH.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

REPO_URL = "https://github.com/danielrosehill/Geopol-Forecaster"
REPO_SHORT = "github.com/danielrosehill/Geopol-Forecaster"


TEMPLATE = r"""
#set document(title: "{title}", author: "Geopol Forecaster")
#set page(
  paper: "a4",
  margin: (x: 2.2cm, top: 2.6cm, bottom: 2.4cm),
  header: context [
    #set text(7.5pt, fill: luma(120), tracking: 1pt)
    #grid(columns: (1fr, auto, 1fr),
      align: (left, center, right),
      [{classification}],
      [],
      [RUN {run_id} · {runtime}],
    )
    #v(-0.35em)
    #line(length: 100%, stroke: 0.4pt + luma(200))
  ],
  footer: context [
    #set text(7.5pt, fill: luma(120))
    #line(length: 100%, stroke: 0.4pt + luma(200))
    #v(-0.2em)
    #grid(columns: (1fr, auto, 1fr),
      align: (left, center, right),
      [Geopol Forecaster],
      [generated with #link("{repo_url}")[{repo_short}]],
      [#counter(page).display("1 / 1", both: true)],
    )
  ],
)
#set text(font: ("IBM Plex Sans", "DejaVu Sans"), size: 10.5pt, lang: "en")
#set par(justify: true, leading: 0.62em, first-line-indent: 0pt)

#let brand = rgb("#0b3d2e")
#let brand-light = rgb("#1f6b4f")
#let accent = rgb("#a43e2a")

#show heading.where(level: 1): it => {{
  pagebreak(weak: true)
  v(0.6em)
  block(below: 0.6em)[
    #set text(size: 20pt, weight: "bold", fill: brand)
    #it.body
  ]
  line(length: 100%, stroke: 0.8pt + brand)
  v(0.4em)
}}
#show heading.where(level: 2): it => {{
  v(0.8em)
  block(below: 0.3em)[
    #set text(size: 13pt, weight: "bold", fill: brand)
    #it.body
  ]
}}
#show heading.where(level: 3): it => {{
  v(0.4em)
  block(below: 0.2em)[
    #set text(size: 11pt, weight: "bold", fill: brand-light)
    #it.body
  ]
}}
#show link: set text(fill: rgb("#1e5f8b"))
#show raw: set text(font: "DejaVu Sans Mono", size: 8.8pt)
#show table: set text(size: 9.5pt)
#set table(stroke: 0.4pt + luma(180), inset: 6pt)

// ─── COVER ──────────────────────────────────────────────────────────
#page(header: none, footer: none)[
  #v(1.2fr)
  #align(center)[
    #block(width: 100%, fill: brand, inset: (x: 1em, y: 0.6em))[
      #set text(fill: white, tracking: 2pt, size: 10pt, weight: "bold")
      {classification}
    ]
  ]
  #v(1.5fr)
  #align(center)[
    #text(10pt, tracking: 3pt, fill: luma(100))[GEOPOL FORECASTER]
    #v(0.6em)
    #text(28pt, weight: "bold", fill: brand)[Assessment Report]
    #v(1.2em)
    #block(width: 80%, inset: (x: 0em))[
      #set text(15pt, weight: "semibold")
      #set par(justify: false, leading: 0.55em)
      {cover_title}
    ]
  ]
  #v(1fr)
  #align(center)[
    #block(width: 75%, stroke: (top: 0.6pt + brand, bottom: 0.6pt + brand),
           inset: (y: 0.8em))[
      #set text(10pt)
      #grid(columns: (1fr, 1fr), gutter: 1em, align: left,
        [*Run ID*\ {run_id}],
        [*Generated*\ {gen_date}],
        [*Forecast horizon*\ {horizon}],
        [*Pipeline*\ Stage A sim + Stage B council],
      )
    ]
  ]
  #v(1.2fr)
  #align(center)[
    #block(width: 100%, fill: brand, inset: (x: 1em, y: 0.6em))[
      #set text(fill: white, tracking: 2pt, size: 10pt, weight: "bold")
      {classification}
    ]
  ]
]

// ─── BLUF ────────────────────────────────────────────────────────────
#page[
  #v(0.5em)
  #block(
    width: 100%,
    fill: rgb("#f4f1ea"),
    stroke: (left: 4pt + accent),
    inset: (x: 1.2em, y: 1em),
    radius: 2pt,
  )[
    #text(9pt, tracking: 3pt, fill: accent, weight: "bold")[BOTTOM LINE UP FRONT]
    #v(0.4em)
    #set text(11pt)
    {bluf_body}
  ]
  #v(1em)
  #text(8.5pt, fill: luma(110), style: "italic")[
    The full analytical reasoning, lens-by-lens breakdown, scenario branching,
    and watch indicators follow in Sections 1–11. A colophon with the
    generating stack and reproducibility notes is appended.
  ]
]

// ─── BODY ────────────────────────────────────────────────────────────
#include "body.typ"

// ─── COLOPHON ────────────────────────────────────────────────────────
#pagebreak()
= About this report

This document was produced by *Geopol Forecaster*, an open-source two-stage
geopolitical forecasting pipeline. It is a *research artifact*, not an
official intelligence product. All judgments are probabilistic model output
conditioned on the seeded question and fresh news grounding — they should
be read as structured reasoning support, not as ground truth.

== Pipeline

- *Stage A — Actor simulation.* A persona-briefed roster of state,
  sub-state, and institutional actors independently commit to private
  assessments and concrete actions across four timesteps (now, +24h,
  +1 week, +1 month). A referee model narrates the resulting world state
  between turns, enforcing authority-precedence conflict resolution.
  Actors see only the referee-authored state and their own private memory.
- *Stage B — Council lens panel.* Six analytical lenses answer the
  question independently, cross-review each other, and a chairman
  synthesises the final forecast.

== Stack

#table(
  columns: (auto, 1fr),
  align: (left, left),
  [*Language runtime*], [Python 3.12, managed via `uv`],
  [*Models*], [`anthropic/claude-sonnet-4.5` via OpenRouter (single model for first seeded runs; per-role overrides wired for future diversification)],
  [*Grounding*], [Tavily search (answer + citations) · RSS + ISW ingestion],
  [*Orchestration*], [asyncio — actors and council lenses run in parallel per stage],
  [*Serialisation*], [Pydantic v2 structured outputs],
  [*Rendering*], [Markdown → Typst via pandoc; PDF via Typst],
  [*Fonts*], [IBM Plex Sans (body) · DejaVu Sans Mono (code)],
)

== Reproducibility

The full simulation transcript (`simulation.json`), lens answers
(`stage1_answers.md`), cross-reviews (`stage2_reviews.md`), chairman
synthesis (`chairman_report.md`), and fresh-data seed (`fresh_data.json`)
are retained under `reports/{run_id}/` in the source repository. Runs
are reproducible modulo the non-determinism of temperature-0.8 actor
sampling and live news drift in the Tavily/RSS seed.

== Source & collaboration

Source code, actor roster, prompts, and published runs are available at:

#align(center)[
  #v(0.4em)
  #box(stroke: 0.6pt + brand, inset: 0.6em, radius: 2pt)[
    #link("{repo_url}")[#text(11pt, weight: "semibold", fill: brand)[{repo_short}]]
  ]
]

== Disclaimer

This report is generated by a language-model pipeline on publicly
available news inputs. It reflects model reasoning conditioned on a
structured prompt. It does *not* represent the views of any government,
intelligence service, or official body. Figures are forecasts, not
measurements. Use at your own discretion and always triangulate against
primary sources before acting on any judgment herein.
"""


def md_to_typst_body(md_path: Path, out_path: Path) -> None:
    subprocess.run(
        ["pandoc", "-t", "typst", str(md_path), "-o", str(out_path)],
        check=True,
    )
    text = out_path.read_text(encoding="utf-8")
    # pandoc emits `#horizontalrule` which isn't a Typst builtin
    text = re.sub(
        r"^#horizontalrule\s*$",
        "#line(length: 100%, stroke: 0.4pt + luma(180))",
        text,
        flags=re.MULTILINE,
    )
    out_path.write_text(text, encoding="utf-8")


def extract_bluf(chairman_md: str) -> str:
    """Pull the HEADLINE FORECAST / BLUF content out of the chairman report."""
    # Match the first section (typically "## 1. HEADLINE FORECAST") up to the next `## `.
    m = re.search(
        r"## 1\.\s*HEADLINE FORECAST\s*\n(.*?)(?=\n##\s|\Z)",
        chairman_md,
        re.DOTALL,
    )
    if not m:
        m = re.search(r"## [^\n]+\n(.*?)(?=\n##\s|\Z)", chairman_md, re.DOTALL)
    body = m.group(1).strip() if m else chairman_md[:1200]
    # Convert minimal markdown to typst inline: **bold**, *italic*, lists.
    body = re.sub(r"\*\*(.+?)\*\*", r"*\1*", body)
    # Escape `<` / `>` literals that would break typst parsing.
    body = body.replace("<", r"\<").replace(">", r"\>")
    # Collapse multi-blank lines.
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body


def infer_cover_title(run_dir: Path, chairman_md: str) -> tuple[str, str]:
    m = re.search(r"^#\s+(.+?)$", chairman_md, re.MULTILINE)
    h1 = m.group(1).strip() if m else "Forecast assessment"
    h1 = re.sub(r"^FINAL REPORT:\s*", "", h1, flags=re.IGNORECASE)
    # Derive horizon line from any "Assessment Horizon" metadata line.
    mh = re.search(r"Assessment Horizon:\s*([^\n]+)", chairman_md)
    horizon = mh.group(1).strip().rstrip("*") if mh else "multi-window"
    return h1, horizon


def infer_runtime(run_dir: Path) -> str:
    """Estimate wall-clock runtime from file mtimes (fresh_data → chairman)."""
    start = run_dir / "fresh_data.json"
    end = run_dir / "chairman_report.md"
    if not (start.exists() and end.exists()):
        return "unknown"
    secs = int(end.stat().st_mtime - start.stat().st_mtime)
    if secs <= 0:
        return "unknown"
    m, s = divmod(secs, 60)
    if m == 0:
        return f"{s}s"
    return f"{m}m{s:02d}s"


def render(run_dir: Path) -> Path:
    chairman_md = (run_dir / "chairman_report.md").read_text(encoding="utf-8")
    body_typ = run_dir / "body.typ"
    md_to_typst_body(run_dir / "chairman_report.md", body_typ)

    cover_title, horizon = infer_cover_title(run_dir, chairman_md)
    bluf_body = extract_bluf(chairman_md)

    # Extract generation date from run ID (YYYY-MM-DD_HHMMSSZ).
    run_id = run_dir.name
    gen_date = run_id[:10] if re.match(r"\d{4}-\d{2}-\d{2}", run_id) else "unknown"
    runtime = infer_runtime(run_dir)

    source = TEMPLATE.format(
        title=cover_title.replace('"', "'"),
        classification="FOR RESEARCH USE · UNCLASSIFIED",
        run_id=run_id,
        cover_title=cover_title,
        gen_date=gen_date,
        horizon=horizon,
        runtime=runtime,
        bluf_body=bluf_body,
        repo_url=REPO_URL,
        repo_short=REPO_SHORT,
    )
    typ_path = run_dir / "intel_report.typ"
    typ_path.write_text(source, encoding="utf-8")

    pdf_path = run_dir / "intel_report.pdf"
    subprocess.run(
        ["typst", "compile", str(typ_path), str(pdf_path)],
        check=True,
    )
    return pdf_path


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: render_intel_report.py <run_dir>", file=sys.stderr)
        sys.exit(2)
    run_dir = Path(sys.argv[1]).resolve()
    if not run_dir.is_dir():
        print(f"not a directory: {run_dir}", file=sys.stderr)
        sys.exit(2)
    for tool in ("pandoc", "typst"):
        if not shutil.which(tool):
            print(f"missing required tool: {tool}", file=sys.stderr)
            sys.exit(2)
    pdf = render(run_dir)
    print(f"rendered → {pdf}")


if __name__ == "__main__":
    main()

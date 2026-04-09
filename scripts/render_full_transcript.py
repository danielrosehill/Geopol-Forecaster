"""Render the *full* Geopol Forecaster run transcript as a single archival PDF.

Unlike `render_intel_report.py` (executive briefing — cover + BLUF + chairman +
colophon, ~15 pages), this script produces a multi-hundred-page archival
artifact that includes every perspective:

  1. Cover page
  2. BLUF
  3. Chairman report
  4. Stage A — per-turn world state, every actor's action, referee narration
  5. Stage A — per-actor view across all turns
  6. Stage B — every lens answer
  7. Stage B — every cross-review
  8. Colophon / stack / repo

Usage:
    uv run python scripts/render_full_transcript.py reports/<RUN_ID>
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/danielrosehill/Geopol-Forecaster"
REPO_SHORT = "github.com/danielrosehill/Geopol-Forecaster"


PREAMBLE = r'''
#set document(title: "{title} — Full Transcript", author: "Geopol Forecaster")
#set page(
  paper: "a4",
  margin: (x: 2.0cm, top: 2.4cm, bottom: 2.2cm),
  header: context [
    #set text(7pt, fill: luma(120), tracking: 1pt)
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
    #set text(7pt, fill: luma(120))
    #line(length: 100%, stroke: 0.4pt + luma(200))
    #v(-0.2em)
    #grid(columns: (1fr, auto, 1fr),
      align: (left, center, right),
      [Geopol Forecaster · Full Transcript],
      [generated with #link("{repo_url}")[{repo_short}]],
      [#counter(page).display("1 / 1", both: true)],
    )
  ],
)
#set text(font: ("IBM Plex Sans", "DejaVu Sans"), size: 9.5pt, lang: "en")
#set par(justify: true, leading: 0.58em, first-line-indent: 0pt)

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
  v(0.7em)
  block(below: 0.3em)[
    #set text(size: 13pt, weight: "bold", fill: brand)
    #it.body
  ]
}}
#show heading.where(level: 3): it => {{
  v(0.4em)
  block(below: 0.2em)[
    #set text(size: 10.5pt, weight: "bold", fill: brand-light)
    #it.body
  ]
}}
#show heading.where(level: 4): it => {{
  v(0.3em)
  block(below: 0.15em)[
    #set text(size: 9.8pt, weight: "bold")
    #it.body
  ]
}}
#show link: set text(fill: rgb("#1e5f8b"))
#show raw: set text(font: "DejaVu Sans Mono", size: 8.2pt)
#show raw.where(block: true): set block(fill: luma(245), inset: 6pt, radius: 2pt, width: 100%)

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
    #text(10pt, tracking: 3pt, fill: luma(100))[GEOPOL FORECASTER · FULL TRANSCRIPT]
    #v(0.6em)
    #text(26pt, weight: "bold", fill: brand)[Complete Run Archive]
    #v(1.2em)
    #block(width: 82%)[
      #set text(14pt, weight: "semibold")
      #set par(justify: false, leading: 0.55em)
      {cover_title}
    ]
  ]
  #v(1fr)
  #align(center)[
    #block(width: 78%, stroke: (top: 0.6pt + brand, bottom: 0.6pt + brand),
           inset: (y: 0.8em))[
      #set text(9.5pt)
      #grid(columns: (1fr, 1fr), gutter: 1em, align: left,
        [*Run ID*\ {run_id}],
        [*Generated*\ {gen_date}],
        [*Runtime*\ {runtime}],
        [*Actors simulated*\ {n_actors}],
        [*Timesteps*\ {n_turns}],
        [*Council lenses*\ {n_lenses}],
      )
    ]
  ]
  #v(0.8fr)
  #align(center)[
    #text(9pt, fill: luma(110), style: "italic")[
      This document contains the *complete* run transcript — every actor's
      private assessment and committed action at every turn, every referee
      narration, every council lens's first-round answer, and every
      cross-review between lenses. For the executive briefing, see the
      separate `intel_report.pdf`.
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

#outline(title: [Contents], depth: 2, indent: auto)
'''


COLOPHON = r'''
#pagebreak()
= About this report

This document is the *full archival transcript* of a Geopol Forecaster run.
Every actor-level assessment, every referee narration, every council lens
answer, and every cross-review is reproduced verbatim. It is a *research
artifact*, not an official intelligence product.

== Pipeline

- *Stage A — Actor simulation.* A persona-briefed roster of state, sub-state,
  and institutional actors independently commit to private assessments and
  concrete actions across four timesteps. A referee model narrates the
  resulting world state between turns, enforcing authority-precedence conflict
  resolution. Actors see only the referee-authored state and their own
  private memory.
- *Stage B — Council lens panel.* Six analytical lenses answer the question
  independently, cross-review each other, and a chairman synthesises the
  final forecast (see `intel_report.pdf`).

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

All raw artifacts — `simulation.json` (full Stage A transcript),
`stage1_answers.md` (lens answers), `stage2_reviews.md` (cross-reviews),
`chairman_report.md` (synthesis), `fresh_data.json` (Tavily + RSS/ISW seed) —
are retained under `reports/{run_id}/` in the source repository. Runs are
reproducible modulo temperature-0.8 actor sampling and live news drift in
the Tavily/RSS seed at run time.

== Source & collaboration

#align(center)[
  #v(0.4em)
  #box(stroke: 0.6pt + brand, inset: 0.6em, radius: 2pt)[
    #link("{repo_url}")[#text(11pt, weight: "semibold", fill: brand)[{repo_short}]]
  ]
]

== Disclaimer

This report is generated by a language-model pipeline on publicly available
news inputs. It reflects model reasoning conditioned on a structured prompt.
It does *not* represent the views of any government, intelligence service,
or official body. Figures are forecasts, not measurements.
'''


def md_to_typst(md_text: str, workdir: Path, tag: str) -> str:
    """Run pandoc md→typst, fix known quirks, return body source."""
    in_path = workdir / f"_in_{tag}.md"
    out_path = workdir / f"_out_{tag}.typ"
    in_path.write_text(md_text, encoding="utf-8")
    subprocess.run(
        ["pandoc", "-t", "typst", str(in_path), "-o", str(out_path)],
        check=True,
    )
    text = out_path.read_text(encoding="utf-8")
    text = re.sub(
        r"^#horizontalrule\s*$",
        "#line(length: 100%, stroke: 0.4pt + luma(180))",
        text,
        flags=re.MULTILINE,
    )
    in_path.unlink(missing_ok=True)
    out_path.unlink(missing_ok=True)
    return text


def escape_typ(s: str) -> str:
    """Escape content that would break Typst markup when embedded verbatim."""
    return (
        s.replace("\\", "\\\\")
        .replace("<", r"\<")
        .replace(">", r"\>")
        .replace("@", r"\@")
        .replace("#", r"\#")
        .replace("$", r"\$")
        .replace("*", r"\*")
        .replace("_", r"\_")
        .replace("[", r"\[")
        .replace("]", r"\]")
    )


def extract_bluf(chairman_md: str) -> str:
    m = re.search(
        r"## 1\.\s*HEADLINE FORECAST\s*\n(.*?)(?=\n##\s|\Z)",
        chairman_md,
        re.DOTALL,
    )
    body = m.group(1).strip() if m else chairman_md[:1200]
    body = re.sub(r"\*\*(.+?)\*\*", r"*\1*", body)
    body = body.replace("<", r"\<").replace(">", r"\>")
    return re.sub(r"\n{3,}", "\n\n", body)


def infer_runtime(run_dir: Path) -> str:
    start = run_dir / "fresh_data.json"
    end = run_dir / "chairman_report.md"
    if not (start.exists() and end.exists()):
        return "unknown"
    secs = int(end.stat().st_mtime - start.stat().st_mtime)
    if secs <= 0:
        return "unknown"
    m, s = divmod(secs, 60)
    return f"{m}m{s:02d}s" if m else f"{s}s"


def infer_cover_title(chairman_md: str) -> str:
    m = re.search(r"^#\s+(.+?)$", chairman_md, re.MULTILINE)
    h1 = m.group(1).strip() if m else "Forecast assessment"
    return re.sub(r"^FINAL REPORT:\s*", "", h1, flags=re.IGNORECASE)


def build_stage_a_turns(sim: dict) -> str:
    """Per-turn sections: world state + all actions + referee narration."""
    out: list[str] = []
    out.append("= Stage A — Turn-by-turn transcript\n")
    out.append(
        "Each turn shows the world state the actors saw, every action each "
        "actor committed to that turn, and the referee's narration that "
        "became the next turn's world state.\n"
    )
    run0 = sim["runs"][0]
    for t in run0["turns"]:
        label = t["timestep_label"]
        out.append(f"\n== Turn: {label}\n")
        out.append("=== World state at start of turn\n")
        out.append("```\n" + t["world_state"].strip() + "\n```\n")
        out.append(f"=== Committed actions ({len(t['actions'])} actors)\n")
        for act in t["actions"]:
            aid = act["actor_id"]
            conf = float(act.get("confidence_in_action", 0) or 0)
            out.append(f"\n==== {aid}  (confidence: {conf:.2f})\n")
            pub = escape_typ(act.get("public_statement", "").strip() or "—")
            con = escape_typ(act.get("concrete_action", "").strip() or "—")
            priv = escape_typ(act.get("private_assessment", "").strip() or "—")
            rls = act.get("redlines_considered") or []
            out.append(f"*Public statement.* {pub}\n")
            out.append(f"*Concrete action.* {con}\n")
            out.append(f"*Private assessment.* {priv}\n")
            if rls:
                rl_txt = "; ".join(escape_typ(r) for r in rls)
                out.append(f"*Red lines considered.* {rl_txt}\n")
        out.append("\n=== Referee narration → next turn\n")
        out.append("```\n" + t["referee_narration"].strip() + "\n```\n")
    return "\n".join(out)


def build_stage_a_actors(sim: dict) -> str:
    """Per-actor sections: all turns for one actor grouped together."""
    out: list[str] = []
    out.append("= Stage A — Per-actor trajectories\n")
    out.append(
        "The same actions pivoted actor-first so each actor's four-turn "
        "trajectory is legible as a single narrative.\n"
    )
    run0 = sim["runs"][0]
    history: dict[str, list[tuple[str, dict]]] = {}
    for t in run0["turns"]:
        for a in t["actions"]:
            history.setdefault(a["actor_id"], []).append((t["timestep_label"], a))
    for aid in sorted(history.keys()):
        out.append(f"\n== Actor: {aid}\n")
        for label, act in history[aid]:
            conf = float(act.get("confidence_in_action", 0) or 0)
            out.append(f"\n=== Turn: {label}  (confidence: {conf:.2f})\n")
            pub = escape_typ(act.get("public_statement", "").strip() or "—")
            con = escape_typ(act.get("concrete_action", "").strip() or "—")
            priv = escape_typ(act.get("private_assessment", "").strip() or "—")
            out.append(f"*Public.* {pub}\n")
            out.append(f"*Action.* {con}\n")
            out.append(f"*Private.* {priv}\n")
    return "\n".join(out)


def render(run_dir: Path) -> Path:
    chairman_md = (run_dir / "chairman_report.md").read_text(encoding="utf-8")
    sim = json.loads((run_dir / "simulation.json").read_text(encoding="utf-8"))
    stage1 = (run_dir / "stage1_answers.md").read_text(encoding="utf-8")
    stage2 = (run_dir / "stage2_reviews.md").read_text(encoding="utf-8")

    cover_title = infer_cover_title(chairman_md)
    runtime = infer_runtime(run_dir)
    run_id = run_dir.name
    gen_date = run_id[:10] if re.match(r"\d{4}-\d{2}-\d{2}", run_id) else "unknown"
    n_actors = len({a["actor_id"] for a in sim["runs"][0]["turns"][0]["actions"]})
    n_turns = len(sim["runs"][0]["turns"])
    n_lenses = len(re.findall(r"^#\s+(?!#)", stage1, re.MULTILINE)) // 2 or 6

    preamble = PREAMBLE.format(
        title=cover_title.replace('"', "'"),
        classification="FOR RESEARCH USE · UNCLASSIFIED",
        run_id=run_id,
        cover_title=cover_title,
        gen_date=gen_date,
        runtime=runtime,
        n_actors=n_actors,
        n_turns=n_turns,
        n_lenses=n_lenses,
        repo_url=REPO_URL,
        repo_short=REPO_SHORT,
    )

    chairman_typ = md_to_typst(chairman_md, run_dir, "chairman")
    stage1_typ = md_to_typst(stage1, run_dir, "stage1")
    stage2_typ = md_to_typst(stage2, run_dir, "stage2")

    bluf_body = extract_bluf(chairman_md)

    bluf_section = (
        "\n#pagebreak()\n= Bottom Line Up Front\n\n"
        + "#block(width: 100%, fill: rgb(\"#f4f1ea\"),"
          " stroke: (left: 4pt + rgb(\"#a43e2a\")),"
          " inset: (x: 1.2em, y: 1em), radius: 2pt)[\n"
        + "#text(9pt, tracking: 3pt, fill: rgb(\"#a43e2a\"),"
          " weight: \"bold\")[BOTTOM LINE UP FRONT]\n#v(0.4em)\n#set text(10.5pt)\n"
        + bluf_body
        + "\n]\n"
    )

    chairman_section = "\n#pagebreak()\n= Chairman report — executive synthesis\n\n" + chairman_typ
    turns_section = "\n#pagebreak()\n" + build_stage_a_turns(sim)
    actors_section = "\n#pagebreak()\n" + build_stage_a_actors(sim)
    lenses_section = "\n#pagebreak()\n= Stage B — Council lens answers\n\n" + stage1_typ
    reviews_section = "\n#pagebreak()\n= Stage B — Council cross-reviews\n\n" + stage2_typ
    colophon = COLOPHON.format(
        run_id=run_id, repo_url=REPO_URL, repo_short=REPO_SHORT
    )

    source = (
        preamble
        + bluf_section
        + chairman_section
        + turns_section
        + actors_section
        + lenses_section
        + reviews_section
        + colophon
    )

    typ_path = run_dir / "full_transcript.typ"
    typ_path.write_text(source, encoding="utf-8")
    pdf_path = run_dir / "full_transcript.pdf"
    subprocess.run(
        ["typst", "compile", str(typ_path), str(pdf_path)], check=True
    )
    return pdf_path


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: render_full_transcript.py <run_dir>", file=sys.stderr)
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
    size_mb = pdf.stat().st_size / 1024 / 1024
    print(f"rendered → {pdf}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()

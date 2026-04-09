"""Typst source generator. Slimmed-down port of `src/lib/typst-template.ts`.

The TS template had special-case rendering for the old POC's SITREP + 6 lens
timeframe tables. This port keeps the same preamble + markdown→Typst pipeline
but targets the new report shape: cover page + chairman report (already
markdown) + appendices for sim trace + fresh-data citations.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

from ..schemas import FreshData, SimulationResult


def _escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace("#", "\\#")
        .replace("$", "\\$")
        .replace("@", "\\@")
        .replace("<", "\\<")
        .replace(">", "\\>")
    )


def _convert_inline(text: str) -> str:
    # code
    codes: list[str] = []
    def _code(m: re.Match) -> str:
        codes.append(m.group(1))
        return f"%%CODE{len(codes) - 1}%%"
    text = re.sub(r"`([^`]+)`", _code, text)

    # links
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'#link("{m.group(2)}")[{_escape(m.group(1))}]',
        text,
    )

    # bold/italic
    text = re.sub(r"\*\*([^*]+)\*\*", lambda m: f"*{_escape(m.group(1))}*", text)
    text = re.sub(r"(?<!\*)\*(?!\*)([^*]+)\*(?!\*)", lambda m: f"_{_escape(m.group(1))}_", text)

    text = _escape_remaining(text)
    for i, c in enumerate(codes):
        text = text.replace(
            f"%%CODE{i}%%", f'#raw("{c.replace(chr(34), chr(92) + chr(34))}")'
        )
    return text


def _escape_remaining(text: str) -> str:
    # Escape typst-special chars in plain runs, avoiding our own inserted
    # directives.
    out: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "#" and not re.match(r"[a-z]", text[i + 1 : i + 2] or ""):
            out.append("\\#")
        elif ch == "$":
            out.append("\\$")
        elif ch == "@":
            out.append("\\@")
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def _md_to_typst(md: str) -> str:
    lines_out: list[str] = []
    for line in md.split("\n"):
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = min(len(m.group(1)) + 1, 5)
            lines_out.append(f"{'=' * level} {_convert_inline(m.group(2))}")
            continue
        if re.match(r"^[-*]\s+", line):
            lines_out.append(f"- {_convert_inline(re.sub(r'^[-*]\s+', '', line))}")
            continue
        nm = re.match(r"^(\d+)\.\s+(.*)$", line)
        if nm:
            lines_out.append(f"+ {_convert_inline(nm.group(2))}")
            continue
        if line.strip() == "":
            lines_out.append("")
            continue
        lines_out.append(_convert_inline(line))
    return "\n".join(lines_out)


PREAMBLE = r"""
#set document(title: "Geopolitical Forecast Report", author: "Geopol Forecaster")
#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2cm, right: 2cm),
)
#set text(font: "IBM Plex Sans", size: 10.5pt)
#set par(justify: true, leading: 0.75em)
#show raw: set text(font: "IBM Plex Mono", size: 9pt)
#let accent = rgb("#1a365d")
#let muted = rgb("#718096")
#let border = rgb("#e2e8f0")
"""


def build_typst_source(
    *,
    question: str,
    session_id: str,
    created_at: str,
    fresh: FreshData,
    sim: SimulationResult,
    chairman_report_md: str,
) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sim_appendix_md = _sim_appendix(sim)
    citations_md = _citations_block(fresh)
    return f"""{PREAMBLE}

#align(center)[
  #v(3cm)
  #text(size: 10pt, fill: muted, tracking: 0.2em, weight: "medium")[GEOPOL FORECASTER]
  #v(0.5cm)
  #line(length: 40%, stroke: 1.5pt + accent)
  #v(0.5cm)
  #text(size: 24pt, weight: "bold", fill: accent)[Geopolitical Forecast Report]
  #v(0.3cm)
  #text(size: 12pt, fill: muted)[Stage A actor simulation · Stage B lens-council deliberation]
  #v(1cm)
  #block(width: 70%, inset: 14pt, stroke: 0.5pt + border, radius: 4pt)[
    #align(left)[
      *Question:* {_escape(question)} \\
      *Session:* {_escape(session_id)} \\
      *Generated:* {ts}
    ]
  ]
]

#pagebreak()

#outline(title: [Contents], depth: 2)

#pagebreak()

= Chairman's Final Report

{_md_to_typst(chairman_report_md)}

#pagebreak()

= Appendix A — Simulation Trace

{_md_to_typst(sim_appendix_md)}

#pagebreak()

= Appendix B — Fresh Data Citations

{_md_to_typst(citations_md)}
"""


def _sim_appendix(sim: SimulationResult) -> str:
    lines = ["## Summary", ""]
    s = sim.summary
    lines.append(f"**Dominant trajectory:** {s.dominant_trajectory}")
    lines.append("")
    if s.divergent_trajectories:
        lines.append("**Divergent trajectories:**")
        for d in s.divergent_trajectories:
            lines.append(f"- {d}")
        lines.append("")
    if s.empirical_probabilities:
        lines.append("**Empirical probabilities:**")
        for k, v in s.empirical_probabilities.items():
            lines.append(f"- {k}: {v:.2f}")
        lines.append("")
    if s.flags_for_council:
        lines.append("**Flags for council (sim-declared assumptions):**")
        for f in s.flags_for_council:
            lines.append(f"- {f}")
        lines.append("")
    for run in sim.runs:
        lines.append(f"## Run {run.run_idx}")
        for turn in run.turns:
            lines.append(f"### Turn {turn.timestep_label}")
            for a in turn.actions:
                lines.append(f"- **{a.actor_id}** (conf {a.confidence_in_action:.2f}): {a.concrete_action}")
            lines.append("")
            lines.append(f"_Referee:_ {turn.referee_narration[:1200]}")
            lines.append("")
    return "\n".join(lines)


def _citations_block(fresh: FreshData) -> str:
    lines = [f"*Bundle timestamp:* {fresh.timestamp_utc}", ""]
    if fresh.tavily_queries:
        lines.append("## Tavily queries")
        for q, a in zip(fresh.tavily_queries, fresh.tavily_answers):
            lines.append(f"**Q:** {q}")
            lines.append("")
            lines.append(a[:2000])
            lines.append("")
    if fresh.tavily_citations:
        lines.append("## Citations")
        for c in fresh.tavily_citations:
            title = c.title or c.url
            lines.append(f"- [{title}]({c.url})")
    return "\n".join(lines)

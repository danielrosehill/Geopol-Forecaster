"""Publish a Geopol Forecaster run to the docs/ Jekyll site.

Fans out every perspective:
  - one page per actor (all 4 turns of private assessment + action)
  - one page per turn (world state + all 40 actions + referee narration)
  - one page per council lens (extracted from stage1_answers.md)
  - one page per cross-reviewer (extracted from stage2_reviews.md)
  - a run index that links to the chairman report, the intel PDF, and
    all of the above
  - the intel PDF itself

Usage:
    uv run python scripts/publish_run.py reports/<RUN_ID>
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from textwrap import dedent

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_RUNS = REPO_ROOT / "docs" / "runs"


def _front_matter(title: str, layout: str = "default") -> str:
    safe = title.replace('"', "'")
    return f"---\nlayout: {layout}\ntitle: \"{safe}\"\n---\n\n"


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ─── Actor + turn fan-out from simulation.json ─────────────────────────

def publish_actors_and_turns(run_dir: Path, out_dir: Path) -> dict:
    sim = json.loads((run_dir / "simulation.json").read_text(encoding="utf-8"))
    run0 = sim["runs"][0]
    turns = run0["turns"]

    actors_dir = out_dir / "actors"
    turns_dir = out_dir / "turns"
    actors_dir.mkdir(parents=True, exist_ok=True)
    turns_dir.mkdir(parents=True, exist_ok=True)

    # Pivot: {actor_id: [(turn_label, action), ...]}
    actor_history: dict[str, list[tuple[str, dict]]] = {}
    for t in turns:
        label = t["timestep_label"]
        for a in t["actions"]:
            actor_history.setdefault(a["actor_id"], []).append((label, a))

    # One page per actor.
    actor_ids = sorted(actor_history.keys())
    for aid in actor_ids:
        lines = [_front_matter(f"Actor — {aid}")]
        lines.append(f"# {aid}\n")
        lines.append(
            f"All {len(actor_history[aid])} turns of private assessment, public "
            "statement, and committed action for this actor across the Stage A "
            "simulation.\n"
        )
        for label, act in actor_history[aid]:
            lines.append(f"\n## Turn: {label}\n")
            lines.append(f"**Confidence in action:** {act.get('confidence_in_action', 0):.2f}\n")
            if act.get("redlines_considered"):
                lines.append("**Red lines considered:**\n")
                for rl in act["redlines_considered"]:
                    lines.append(f"- {rl}")
                lines.append("")
            lines.append("### Private assessment\n")
            lines.append(f"> {act.get('private_assessment','').strip()}\n")
            lines.append("### Public statement\n")
            lines.append(f"> {act.get('public_statement','').strip()}\n")
            lines.append("### Concrete action\n")
            lines.append(f"> {act.get('concrete_action','').strip()}\n")
        (actors_dir / f"{aid}.md").write_text("\n".join(lines), encoding="utf-8")

    # Actor index.
    idx_lines = [_front_matter("Actors — full Stage A perspective set")]
    idx_lines.append("# Actors\n")
    idx_lines.append(
        f"Stage A simulated **{len(actor_ids)} actors** across "
        f"**{len(turns)} timesteps**. Every actor commits privately and "
        "independently; the referee narrates world-state between turns.\n"
    )
    for aid in actor_ids:
        idx_lines.append(f"- [{aid}]({aid})")
    (actors_dir / "index.md").write_text("\n".join(idx_lines), encoding="utf-8")

    # One page per turn (world state + all actions + referee narration).
    for t in turns:
        label = t["timestep_label"]
        slug = _slug(label)
        lines = [_front_matter(f"Turn — {label}")]
        lines.append(f"# Turn: {label}\n")
        lines.append("## World state at start of turn\n")
        lines.append("```\n" + t["world_state"].strip() + "\n```\n")
        lines.append(f"## Committed actions ({len(t['actions'])} actors)\n")
        for act in t["actions"]:
            aid = act["actor_id"]
            lines.append(f"### {aid}\n")
            lines.append(f"**Public:** {act.get('public_statement','').strip()}\n")
            lines.append(f"**Action:** {act.get('concrete_action','').strip()}\n")
            lines.append(
                f"*Confidence: {act.get('confidence_in_action', 0):.2f}* · "
                f"[full actor page](../actors/{aid})\n"
            )
        lines.append("## Referee narration → next turn\n")
        lines.append("```\n" + t["referee_narration"].strip() + "\n```\n")
        (turns_dir / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")

    # Turn index.
    tidx = [_front_matter("Turns — Stage A timestep sequence")]
    tidx.append("# Turns\n")
    for t in turns:
        label = t["timestep_label"]
        tidx.append(f"- [{label}]({_slug(label)})")
    (turns_dir / "index.md").write_text("\n".join(tidx), encoding="utf-8")

    return {
        "n_actors": len(actor_ids),
        "n_turns": len(turns),
        "actor_ids": actor_ids,
        "turn_labels": [t["timestep_label"] for t in turns],
    }


# ─── Council lens / review fan-out from stage markdown files ───────────

def _split_by_h1(md: str) -> list[tuple[str, str]]:
    """Return list of (title, body) split by top-level `# Heading` lines.

    Collapses consecutive H1s (e.g. stage1_answers.md has both
    `# Neutral` as a section marker immediately followed by
    `# NEUTRAL LENS FORECAST: ...` as the actual body heading). Only the
    first H1 in each consecutive run counts as a section boundary; subsequent
    consecutive H1s are folded into that section's body.
    """
    # First pass: tokenise into (is_h1, title_if_h1, original_line) tuples.
    parts: list[tuple[str, str]] = []
    current_title: str | None = None
    current: list[str] = []
    prev_was_h1 = False
    for line in md.splitlines():
        m = re.match(r"^#\s+(?!#)(.+?)\s*$", line)
        if m:
            if prev_was_h1:
                # Consecutive H1 — fold into current body as a regular H1 line.
                current.append(line)
                continue
            if current_title is not None:
                parts.append((current_title, "\n".join(current).strip()))
            current_title = m.group(1).strip()
            current = []
            prev_was_h1 = True
        else:
            if line.strip():
                prev_was_h1 = False
            current.append(line)
    if current_title is not None:
        parts.append((current_title, "\n".join(current).strip()))
    return parts


def publish_council(run_dir: Path, out_dir: Path) -> dict:
    lenses_dir = out_dir / "lenses"
    reviews_dir = out_dir / "reviews"
    lenses_dir.mkdir(parents=True, exist_ok=True)
    reviews_dir.mkdir(parents=True, exist_ok=True)

    stage1 = (run_dir / "stage1_answers.md").read_text(encoding="utf-8")
    stage2 = (run_dir / "stage2_reviews.md").read_text(encoding="utf-8")

    lens_parts = _split_by_h1(stage1)
    # Filter out degenerate heads (the first # in each part repeats the lens
    # title; keep both the short top marker and the detailed body).
    lens_meta: list[tuple[str, str]] = []
    for title, body in lens_parts:
        slug = _slug(title)
        fname = f"{slug}.md"
        page = _front_matter(f"Lens — {title}")
        page += f"# {title} lens\n\n"
        page += "*Stage B — independent first-round answer from the six-lens council panel.*\n\n"
        page += body + "\n"
        (lenses_dir / fname).write_text(page, encoding="utf-8")
        lens_meta.append((title, slug))

    idx = [_front_matter("Council lenses — Stage B first-round answers")]
    idx.append("# Council lenses\n")
    idx.append(
        "Six analytical lenses answer the forecast question independently "
        "before cross-reviewing each other.\n"
    )
    for title, slug in lens_meta:
        idx.append(f"- [{title}]({slug})")
    (lenses_dir / "index.md").write_text("\n".join(idx), encoding="utf-8")

    review_parts = _split_by_h1(stage2)
    rev_meta: list[tuple[str, str]] = []
    for title, body in review_parts:
        slug = _slug(title)
        page = _front_matter(f"Review — {title}")
        page += f"# {title}\n\n"
        page += "*Stage B — cross-review round: this lens reviewing all other lenses' answers.*\n\n"
        page += body + "\n"
        (reviews_dir / f"{slug}.md").write_text(page, encoding="utf-8")
        rev_meta.append((title, slug))

    idx = [_front_matter("Council cross-reviews")]
    idx.append("# Cross-reviews\n")
    idx.append("Every lens reviews the other five lenses' Stage 1 answers.\n")
    for title, slug in rev_meta:
        idx.append(f"- [{title}]({slug})")
    (reviews_dir / "index.md").write_text("\n".join(idx), encoding="utf-8")

    return {
        "n_lenses": len(lens_meta),
        "n_reviews": len(rev_meta),
        "lens_meta": lens_meta,
        "review_meta": rev_meta,
    }


# ─── Run-level index ────────────────────────────────────────────────────

def write_run_index(run_dir: Path, out_dir: Path, stats: dict) -> None:
    run_id = run_dir.name
    chairman = (run_dir / "chairman_report.md").read_text(encoding="utf-8")

    m = re.search(r"^#\s+(.+?)$", chairman, re.MULTILINE)
    title = m.group(1).strip() if m else f"Run {run_id}"
    title = re.sub(r"^FINAL REPORT:\s*", "", title, flags=re.IGNORECASE)

    lines = [_front_matter(f"Run {run_id}")]
    lines.append(f"# Run `{run_id}`\n")
    lines.append(f"**{title}**\n")
    lines.append(
        f"Stage A simulated **{stats['n_actors']} actors** across "
        f"**{stats['n_turns']} timesteps**. Stage B ran a "
        f"**{stats['n_lenses']}-lens council** with "
        f"**{stats['n_reviews']} cross-reviews**.\n"
    )
    lines.append("## Final report\n")
    lines.append(
        "- [Chairman report (full markdown)](chairman_report)\n"
        "- [Intel-style PDF](intel_report.pdf)\n"
        "- [Experiment notes](experiment_notes)\n"
    )
    lines.append("## Stage A — actor simulation\n")
    lines.append("- [All actors](actors/) — one page per actor, all turns")
    lines.append("- [All turns](turns/) — world state + all actions + referee narration\n")
    lines.append("## Stage B — council\n")
    lines.append("- [Lens answers (Stage 1)](lenses/) — six independent perspectives")
    lines.append("- [Cross-reviews (Stage 2)](reviews/) — lenses reviewing each other\n")
    lines.append("## Supporting material\n")
    lines.append("- [`fresh_data.json`](fresh_data.json) — Tavily + RSS/ISW seed")
    lines.append("- [`simulation.json`](simulation.json) — full Stage A transcript\n")
    lines.append("\n---\n\n## Quick actor index\n")
    for aid in stats["actor_ids"]:
        lines.append(f"- [{aid}](actors/{aid})")
    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


# ─── Supporting file copy ───────────────────────────────────────────────

COPY_FILES = [
    "chairman_report.md",
    "experiment_notes.md",
    "fresh_data.json",
    "simulation.json",
    "intel_report.pdf",
]


def copy_support(run_dir: Path, out_dir: Path) -> None:
    for name in COPY_FILES:
        src = run_dir / name
        if src.exists():
            shutil.copy2(src, out_dir / name)


def publish(run_dir: Path) -> None:
    run_id = run_dir.name
    out_dir = DOCS_RUNS / run_id
    # Clean previous publish output (leave run_dir itself alone).
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    stats = publish_actors_and_turns(run_dir, out_dir)
    council_stats = publish_council(run_dir, out_dir)
    stats.update(council_stats)
    copy_support(run_dir, out_dir)
    write_run_index(run_dir, out_dir, stats)
    print(f"published → {out_dir}")
    print(
        f"  actors: {stats['n_actors']}  turns: {stats['n_turns']}  "
        f"lenses: {stats['n_lenses']}  reviews: {stats['n_reviews']}"
    )


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: publish_run.py <run_dir>", file=sys.stderr)
        sys.exit(2)
    run_dir = Path(sys.argv[1]).resolve()
    if not run_dir.is_dir():
        print(f"not a directory: {run_dir}", file=sys.stderr)
        sys.exit(2)
    publish(run_dir)


if __name__ == "__main__":
    main()

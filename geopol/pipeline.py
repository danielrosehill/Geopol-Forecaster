"""End-to-end pipeline orchestrator.

Stage 0: gather fresh data (Tavily + RSS/ISW, frozen)
Stage A: snowglobe-style actor simulation → SimulationResult
Stage B: 6-lens council 3-stage protocol → chairman report (markdown)
Render:  Typst source → PDF → reports/<ts>/
"""
from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .config import REPORTS_DIR, require_keys
from .council import run_council
from .news.fresh_data import gather_fresh_data
from .render import build_typst_source, render_pdf
from .render.pdf import TypstNotInstalled
from .simulation import run_simulation


@dataclass
class PipelineResult:
    session_id: str
    report_dir: Path
    markdown_path: Path
    pdf_path: Path | None


async def run_pipeline(question: str, *, skip_pdf: bool = False) -> PipelineResult:
    require_keys()
    session_id = uuid.uuid4().hex
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%SZ")
    out_dir = REPORTS_DIR / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[stage 0] gathering fresh data …")
    fresh = await gather_fresh_data(question)
    (out_dir / "fresh_data.json").write_text(fresh.model_dump_json(indent=2))

    print(f"[stage A] running actor simulation …")
    news_seed = (fresh.rss_brief or "") + "\n\n" + (fresh.isw_brief or "")
    sim = await run_simulation(question, news_seed[:8000])
    (out_dir / "simulation.json").write_text(sim.model_dump_json(indent=2))

    print(f"[stage B] running 6-lens council …")
    council = await run_council(question, fresh, sim)
    (out_dir / "chairman_report.md").write_text(council.final_report_markdown)
    (out_dir / "stage1_answers.md").write_text(
        "\n\n---\n\n".join(f"# {m.lens.name}\n\n{m.answer}" for m in council.stage1)
    )
    (out_dir / "stage2_reviews.md").write_text(
        "\n\n---\n\n".join(
            f"# Reviewer: {r.reviewer_lens_id}\n\n{r.critique}" for r in council.stage2
        )
    )

    print(f"[render] building Typst source …")
    typ = build_typst_source(
        question=question,
        session_id=session_id,
        created_at=created_at,
        fresh=fresh,
        sim=sim,
        chairman_report_md=council.final_report_markdown,
    )
    (out_dir / "report.typ").write_text(typ)

    pdf_path: Path | None = None
    if not skip_pdf:
        try:
            pdf_path = render_pdf(typ, out_dir)
            print(f"[render] PDF → {pdf_path}")
        except TypstNotInstalled as e:
            print(f"[render] {e} — skipping PDF, .typ source is saved")

    return PipelineResult(
        session_id=session_id,
        report_dir=out_dir,
        markdown_path=out_dir / "chairman_report.md",
        pdf_path=pdf_path,
    )


def run_pipeline_sync(question: str, *, skip_pdf: bool = False) -> PipelineResult:
    return asyncio.run(run_pipeline(question, skip_pdf=skip_pdf))

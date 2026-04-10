"""End-to-end pipeline orchestrator.

Stage 0: gather fresh data (Tavily + RSS/ISW, frozen)
Stage A: snowglobe-style actor simulation → SimulationResult
Stage B: 6-lens council 3-stage protocol → chairman report (markdown)
Render:  Typst source → PDF → reports/<ts>/
"""
from __future__ import annotations

import asyncio
import shutil
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .config import REPO_ROOT, REPORTS_DIR, require_keys
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


async def run_pipeline(
    question: str, *, skip_pdf: bool = False, horizons: list[str] | None = None
) -> PipelineResult:
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
    sim = await run_simulation(
        question, news_seed[:8000], horizons=horizons
    )
    (out_dir / "simulation.json").write_text(sim.model_dump_json(indent=2))

    print(f"[stage B] running 6-lens council …")
    council = await run_council(question, fresh, sim, horizons=horizons)
    (out_dir / "chairman_report.md").write_text(council.final_report_markdown)
    (out_dir / "stage1_answers.md").write_text(
        "\n\n---\n\n".join(f"# {m.lens.name}\n\n{m.answer}" for m in council.stage1)
    )
    (out_dir / "stage2_reviews.md").write_text(
        "\n\n---\n\n".join(
            f"# Reviewer: {r.reviewer_lens_id}\n\n{r.critique}" for r in council.stage2
        )
    )

    pdf_path: Path | None = None
    if not skip_pdf:
        pdf_path = _render_and_publish_artifacts(out_dir)

    return PipelineResult(
        session_id=session_id,
        report_dir=out_dir,
        markdown_path=out_dir / "chairman_report.md",
        pdf_path=pdf_path,
    )


def _render_and_publish_artifacts(out_dir: Path) -> Path | None:
    """Run the three renderers + publish_run.py. Failures are non-fatal.

    Produces in order:
      - intel_report.pdf   (executive briefing)
      - full_transcript.pdf (archival — every actor, turn, lens, review)
      - combined_report.pdf (pdfunite of the two)
    Then calls scripts/publish_run.py to fan out into docs/runs/<id>/.
    """
    scripts = REPO_ROOT / "scripts"
    combined: Path | None = None

    def _run(name: str, cmd: list[str]) -> bool:
        try:
            subprocess.run(cmd, check=True)
            return True
        except FileNotFoundError as e:
            print(f"[render] {name}: missing tool — {e}")
        except subprocess.CalledProcessError as e:
            print(f"[render] {name}: failed (exit {e.returncode})")
        return False

    print(f"[render] intel_report.pdf …")
    _run(
        "intel_report",
        [sys.executable, str(scripts / "render_intel_report.py"), str(out_dir)],
    )

    print(f"[render] full_transcript.pdf …")
    _run(
        "full_transcript",
        [sys.executable, str(scripts / "render_full_transcript.py"), str(out_dir)],
    )

    intel = out_dir / "intel_report.pdf"
    full = out_dir / "full_transcript.pdf"
    if intel.exists() and full.exists() and shutil.which("pdfunite"):
        combined = out_dir / "combined_report.pdf"
        print(f"[render] combined_report.pdf …")
        _run("combined", ["pdfunite", str(intel), str(full), str(combined)])
    elif not shutil.which("pdfunite"):
        print("[render] pdfunite not installed — skipping combined PDF")

    print(f"[publish] fanning out to docs/runs/{out_dir.name}/ …")
    _run(
        "publish_run",
        [sys.executable, str(scripts / "publish_run.py"), str(out_dir)],
    )

    # Prefer the combined artifact as the canonical pdf_path, then intel, then full.
    for candidate in (combined, intel, full):
        if candidate and candidate.exists():
            return candidate
    return None


def run_pipeline_sync(
    question: str, *, skip_pdf: bool = False, horizons: list[str] | None = None
) -> PipelineResult:
    return asyncio.run(run_pipeline(question, skip_pdf=skip_pdf, horizons=horizons))

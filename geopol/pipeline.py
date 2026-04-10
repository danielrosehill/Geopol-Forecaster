"""Backward-compatibility shim. Delegates to geopol.graph.

The LangGraph-based pipeline in graph.py is the canonical implementation.
This module exists so that any external code calling run_pipeline_sync()
continues to work.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path

from .graph import run_forecast


@dataclass
class PipelineResult:
    session_id: str
    report_dir: Path
    markdown_path: Path
    pdf_path: Path | None


async def run_pipeline(
    question: str, *, skip_pdf: bool = False, horizons: list[str] | None = None
) -> PipelineResult:
    state = await run_forecast(question, skip_pdf=skip_pdf, horizons=horizons)
    report_dir = Path(state["report_dir"])
    pdf = Path(state["pdf_path"]) if state.get("pdf_path") else None
    return PipelineResult(
        session_id=state["session_id"],
        report_dir=report_dir,
        markdown_path=report_dir / "chairman_report.md",
        pdf_path=pdf,
    )


def run_pipeline_sync(
    question: str, *, skip_pdf: bool = False, horizons: list[str] | None = None
) -> PipelineResult:
    return asyncio.run(run_pipeline(question, skip_pdf=skip_pdf, horizons=horizons))

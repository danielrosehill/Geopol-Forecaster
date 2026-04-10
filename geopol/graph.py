"""LangGraph pipeline orchestrator.

Replaces the linear async chain in pipeline.py with a checkpointed StateGraph.
Nodes wrap existing functions from simulation/, council/, news/, and render/.
"""
from __future__ import annotations

import asyncio
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict

from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import END, StateGraph

from .actors import ROSTER_CORE
from .base_context import BASE_CONTEXT
from .config import (
    CHECKPOINT_DB,
    DAILY_ACTORS_COUNT,
    DAILY_HORIZONS,
    DAILY_TIMESTEPS,
    MC_RUNS,
    MODEL_COUNCIL_MEMBER,
    REPO_ROOT,
    REPORTS_DIR,
    require_keys,
)
from .council.lenses import LENSES
from .council.protocol import (
    CouncilMemberAnswer,
    CouncilPeerReview,
    _bundle,
    _stage1_member,
    _stage2_review,
    _stage3_chairman,
)
from .news.fresh_data import gather_fresh_data
from .pinecone_store import query_past_runs, upsert_run
from .schemas import FreshData, SimulationResult
from .simulation import run_simulation


# ─── State ────────────────────────────────────────────────────────────────

class ForecastState(TypedDict, total=False):
    # Inputs
    question: str
    session_id: str
    created_at: str
    horizons: list[str] | None
    mode: str  # "full" or "daily"
    skip_pdf: bool

    # Stage 0
    fresh: dict
    news_seed: str

    # Stage A
    simulation: dict

    # Pinecone retrieval
    past_runs_context: str

    # Stage B (decomposed)
    council_stage1_answers: list[dict]
    council_stage2_reviews: list[dict]
    council_report_markdown: str

    # Render
    report_dir: str
    pdf_path: str | None


# ─── Helpers ──────────────────────────────────────────────────────────────

def _out_dir(state: ForecastState) -> Path:
    return Path(state["report_dir"])


# ─── Nodes ────────────────────────────────────────────────────────────────

async def gather_news(state: ForecastState) -> dict:
    """Stage 0: Tavily + RSS news gathering."""
    print("[stage 0] gathering fresh data …")
    fresh = await gather_fresh_data(state["question"])

    out_dir = _out_dir(state)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "fresh_data.json").write_text(fresh.model_dump_json(indent=2))

    news_seed = (fresh.rss_brief or "") + "\n\n" + (fresh.isw_brief or "")
    return {
        "fresh": fresh.model_dump(),
        "news_seed": news_seed[:8000],
    }


async def run_sim(state: ForecastState) -> dict:
    """Stage A: actor simulation."""
    print("[stage A] running actor simulation …")
    is_daily = state.get("mode") == "daily"
    actors = ROSTER_CORE[:DAILY_ACTORS_COUNT] if is_daily else ROSTER_CORE
    timesteps = DAILY_TIMESTEPS if is_daily else None
    horizons = state.get("horizons")
    if is_daily and not horizons:
        horizons = DAILY_HORIZONS

    sim = await run_simulation(
        state["question"],
        state["news_seed"],
        actors=actors,
        timesteps=timesteps,
        horizons=horizons,
    )

    out_dir = _out_dir(state)
    (out_dir / "simulation.json").write_text(sim.model_dump_json(indent=2))
    return {"simulation": sim.model_dump()}


async def council_stage1(state: ForecastState) -> dict:
    """Stage B.1: parallel lens answers."""
    print("[stage B.1] running 6-lens council (stage 1) …")
    fresh = FreshData.model_validate(state["fresh"])
    sim = SimulationResult.model_validate(state["simulation"])
    horizons = state.get("horizons")
    bundle = _bundle(state["question"], fresh, sim)

    answers = await asyncio.gather(
        *[_stage1_member(lens, bundle, horizon_labels=horizons) for lens in LENSES]
    )

    out_dir = _out_dir(state)
    (out_dir / "stage1_answers.md").write_text(
        "\n\n---\n\n".join(f"# {m.lens.name}\n\n{m.answer}" for m in answers)
    )

    return {
        "council_stage1_answers": [
            {"lens_id": m.lens.id, "lens_name": m.lens.name, "answer": m.answer}
            for m in answers
        ],
    }


async def council_stage2(state: ForecastState) -> dict:
    """Stage B.2: blind peer review (skipped in daily mode)."""
    print("[stage B.2] running blind peer review …")
    fresh = FreshData.model_validate(state["fresh"])
    sim = SimulationResult.model_validate(state["simulation"])
    bundle = _bundle(state["question"], fresh, sim)

    stage1_answers = state["council_stage1_answers"]
    labels = [chr(ord("A") + i) for i in range(len(stage1_answers))]
    anonymised = [
        (f"Response {lbl}", ans["answer"])
        for lbl, ans in zip(labels, stage1_answers)
    ]

    reviews = await asyncio.gather(
        *[_stage2_review(lens, anonymised, bundle) for lens in LENSES]
    )

    out_dir = _out_dir(state)
    (out_dir / "stage2_reviews.md").write_text(
        "\n\n---\n\n".join(
            f"# Reviewer: {r.reviewer_lens_id}\n\n{r.critique}" for r in reviews
        )
    )

    return {
        "council_stage2_reviews": [
            {"reviewer_lens_id": r.reviewer_lens_id, "critique": r.critique}
            for r in reviews
        ],
    }


async def retrieve_past_runs_node(state: ForecastState) -> dict:
    """Query Pinecone for past forecasts on similar topics."""
    print("[pinecone] retrieving past runs …")
    ctx = await query_past_runs(state["question"])
    if ctx:
        print(f"[pinecone] found relevant past runs ({len(ctx)} chars)")
    else:
        print("[pinecone] no relevant past runs found")
    return {"past_runs_context": ctx}


async def council_stage3(state: ForecastState) -> dict:
    """Stage B.3: chairman synthesis."""
    print("[stage B.3] chairman writing final report …")
    fresh = FreshData.model_validate(state["fresh"])
    sim = SimulationResult.model_validate(state["simulation"])
    bundle = _bundle(state["question"], fresh, sim)
    horizons = state.get("horizons")
    past_runs = state.get("past_runs_context", "")

    # Re-hydrate stage1 answers into CouncilMemberAnswer objects
    stage1 = []
    for ans in state["council_stage1_answers"]:
        lens = next(l for l in LENSES if l.id == ans["lens_id"])
        stage1.append(CouncilMemberAnswer(lens=lens, answer=ans["answer"]))

    # Re-hydrate stage2 reviews (may be empty in daily mode)
    stage2 = [
        CouncilPeerReview(reviewer_lens_id=r["reviewer_lens_id"], critique=r["critique"])
        for r in state.get("council_stage2_reviews", [])
    ]

    report = await _stage3_chairman(
        state["question"],
        bundle,
        stage1,
        stage2,
        horizon_labels=horizons,
        past_runs_context=past_runs,
    )

    out_dir = _out_dir(state)
    (out_dir / "chairman_report.md").write_text(report)
    return {"council_report_markdown": report}


async def render_and_publish(state: ForecastState) -> dict:
    """Render PDFs and publish to docs/runs/."""
    out_dir = _out_dir(state)
    skip_pdf = state.get("skip_pdf", False)
    pdf_path: str | None = None

    if not skip_pdf:
        result = await asyncio.to_thread(_render_artifacts, out_dir)
        pdf_path = str(result) if result else None

    return {"pdf_path": pdf_path}


def _render_artifacts(out_dir: Path) -> Path | None:
    """Run the three renderers + publish_run.py (synchronous)."""
    scripts = REPO_ROOT / "scripts"

    def _run(name: str, cmd: list[str]) -> bool:
        try:
            subprocess.run(cmd, check=True)
            return True
        except FileNotFoundError as e:
            print(f"[render] {name}: missing tool — {e}")
        except subprocess.CalledProcessError as e:
            print(f"[render] {name}: failed (exit {e.returncode})")
        return False

    print("[render] intel_report.pdf …")
    _run("intel_report", [sys.executable, str(scripts / "render_intel_report.py"), str(out_dir)])

    print("[render] full_transcript.pdf …")
    _run("full_transcript", [sys.executable, str(scripts / "render_full_transcript.py"), str(out_dir)])

    intel = out_dir / "intel_report.pdf"
    full = out_dir / "full_transcript.pdf"
    combined: Path | None = None
    if intel.exists() and full.exists() and shutil.which("pdfunite"):
        combined = out_dir / "combined_report.pdf"
        print("[render] combined_report.pdf …")
        _run("combined", ["pdfunite", str(intel), str(full), str(combined)])
    elif not shutil.which("pdfunite"):
        print("[render] pdfunite not installed — skipping combined PDF")

    print(f"[publish] fanning out to docs/runs/{out_dir.name}/ …")
    _run("publish_run", [sys.executable, str(scripts / "publish_run.py"), str(out_dir)])

    for candidate in (combined, intel, full):
        if candidate and candidate.exists():
            return candidate
    return None


async def upsert_to_pinecone(state: ForecastState) -> dict:
    """Archive the run in Pinecone for future retrieval."""
    print("[pinecone] upserting run …")
    sim = SimulationResult.model_validate(state["simulation"])
    summary_text = (
        f"Dominant trajectory: {sim.summary.dominant_trajectory}\n\n"
        f"Flags for council: {', '.join(sim.summary.flags_for_council)}"
    )
    lens_digest = "\n\n---\n\n".join(
        f"# {ans['lens_name']}\n\n{ans['answer']}"
        for ans in state.get("council_stage1_answers", [])
    )

    await upsert_run(
        session_id=state["session_id"],
        question=state["question"],
        created_at=state["created_at"],
        chairman_md=state.get("council_report_markdown", ""),
        sim_summary_text=summary_text,
        lens_digest=lens_digest[:8000],
        mode=state.get("mode", "full"),
    )
    return {}


# ─── Conditional edge ────────────────────────────────────────────────────

def route_after_stage1(state: ForecastState) -> str:
    if state.get("mode") == "daily":
        return "retrieve_past_runs"
    return "council_stage2"


# ─── Graph construction ──────────────────────────────────────────────────

def build_graph() -> StateGraph:
    builder = StateGraph(ForecastState)

    builder.add_node("gather_news", gather_news)
    builder.add_node("run_sim", run_sim)
    builder.add_node("council_stage1", council_stage1)
    builder.add_node("council_stage2", council_stage2)
    builder.add_node("retrieve_past_runs", retrieve_past_runs_node)
    builder.add_node("council_stage3", council_stage3)
    builder.add_node("render_and_publish", render_and_publish)
    builder.add_node("upsert_to_pinecone", upsert_to_pinecone)

    builder.set_entry_point("gather_news")
    builder.add_edge("gather_news", "run_sim")
    builder.add_edge("run_sim", "council_stage1")
    builder.add_conditional_edges("council_stage1", route_after_stage1)
    builder.add_edge("council_stage2", "retrieve_past_runs")
    builder.add_edge("retrieve_past_runs", "council_stage3")
    builder.add_edge("council_stage3", "render_and_publish")
    builder.add_edge("render_and_publish", "upsert_to_pinecone")
    builder.add_edge("upsert_to_pinecone", END)

    return builder


async def run_forecast(
    question: str,
    *,
    mode: str = "full",
    horizons: list[str] | None = None,
    skip_pdf: bool = False,
    session_id: str | None = None,
) -> ForecastState:
    """Main entry point: run the full forecast graph."""
    require_keys()

    sid = session_id or uuid.uuid4().hex
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%SZ")
    out_dir = REPORTS_DIR / stamp
    out_dir.mkdir(parents=True, exist_ok=True)

    if mode == "daily" and skip_pdf is False:
        skip_pdf = True

    initial_state: ForecastState = {
        "question": question,
        "session_id": sid,
        "created_at": created_at,
        "horizons": horizons,
        "mode": mode,
        "skip_pdf": skip_pdf,
        "report_dir": str(out_dir),
    }

    CHECKPOINT_DB.parent.mkdir(parents=True, exist_ok=True)
    async with AsyncSqliteSaver.from_conn_string(str(CHECKPOINT_DB)) as checkpointer:
        graph = build_graph().compile(checkpointer=checkpointer)
        config = {"configurable": {"thread_id": sid}}
        final_state = await graph.ainvoke(initial_state, config)
    return final_state


async def resume_forecast(session_id: str) -> ForecastState:
    """Resume a previously interrupted forecast run."""
    CHECKPOINT_DB.parent.mkdir(parents=True, exist_ok=True)
    async with AsyncSqliteSaver.from_conn_string(str(CHECKPOINT_DB)) as checkpointer:
        graph = build_graph().compile(checkpointer=checkpointer)
        config = {"configurable": {"thread_id": session_id}}
        final_state = await graph.ainvoke(None, config)
    return final_state

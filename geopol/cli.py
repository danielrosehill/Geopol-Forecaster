"""Typer CLI. `uv run geopol forecast "Will the Iran-Israel ceasefire hold …?"`"""
from __future__ import annotations

import asyncio
from typing import Optional

import typer

from .config import HORIZON_PRESETS

app = typer.Typer(no_args_is_help=True, add_completion=False)


def _resolve_horizons(raw: Optional[str]) -> list[str] | None:
    """Parse --horizons flag: preset name or comma-separated labels."""
    if raw is None:
        return None
    if raw in HORIZON_PRESETS:
        return HORIZON_PRESETS[raw]
    return [h.strip() for h in raw.split(",") if h.strip()]


@app.command()
def forecast(
    question: str = typer.Argument(..., help="The forecast question"),
    skip_pdf: bool = typer.Option(False, help="Skip Typst PDF render; emit .typ only"),
    horizons: Optional[str] = typer.Option(
        None,
        help=(
            "Timestep horizons: a preset name (default, short, medium, long) "
            "or comma-separated labels (e.g. '+1 week,+1 month,+1 year')"
        ),
    ),
    mode: str = typer.Option(
        "full",
        help="Run mode: 'full' (default) or 'daily' (fewer actors, no peer review)",
    ),
) -> None:
    """Run the full forecast pipeline via LangGraph."""
    from .graph import run_forecast

    labels = _resolve_horizons(horizons)
    state = asyncio.run(
        run_forecast(question, mode=mode, horizons=labels, skip_pdf=skip_pdf)
    )
    typer.echo(f"\nSession:   {state['session_id']}")
    typer.echo(f"Directory: {state['report_dir']}")
    typer.echo(f"Report:    {state['report_dir']}/chairman_report.md")
    if state.get("pdf_path"):
        typer.echo(f"PDF:       {state['pdf_path']}")


@app.command()
def resume(
    session_id: str = typer.Argument(..., help="Session ID of the interrupted run"),
) -> None:
    """Resume a previously interrupted forecast run from its last checkpoint."""
    from .graph import resume_forecast

    state = asyncio.run(resume_forecast(session_id))
    typer.echo(f"\nResumed session: {state['session_id']}")
    typer.echo(f"Directory:       {state['report_dir']}")
    if state.get("pdf_path"):
        typer.echo(f"PDF:             {state['pdf_path']}")


@app.command()
def smoketest() -> None:
    """Tiny smoke test — 3 actors, 2 timesteps, 1 run, no council."""
    from .actors import ROSTER_CORE
    from .simulation import run_simulation

    async def _go() -> None:
        sim = await run_simulation(
            "Will the Iran-Israel ceasefire hold through Q3 2026?",
            news_seed="(smoke test: no fresh data)",
            actors=ROSTER_CORE[:3],
            n_runs=1,
            timesteps=2,
        )
        typer.echo(sim.summary.model_dump_json(indent=2))

    asyncio.run(_go())


if __name__ == "__main__":
    app()

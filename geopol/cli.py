"""Typer CLI. `uv run geopol forecast "Will the Iran-Israel ceasefire hold …?"`"""
from __future__ import annotations

from typing import Optional

import typer

from .config import HORIZON_PRESETS
from .pipeline import run_pipeline_sync

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
) -> None:
    """Run the full Stage-A + Stage-B pipeline and emit a report directory."""
    labels = _resolve_horizons(horizons)
    result = run_pipeline_sync(question, skip_pdf=skip_pdf, horizons=labels)
    typer.echo(f"\nSession:   {result.session_id}")
    typer.echo(f"Directory: {result.report_dir}")
    typer.echo(f"Markdown:  {result.markdown_path}")
    if result.pdf_path:
        typer.echo(f"PDF:       {result.pdf_path}")


@app.command()
def smoketest() -> None:
    """Tiny smoke test — 3 actors, 2 timesteps, 1 run, no council."""
    import asyncio

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

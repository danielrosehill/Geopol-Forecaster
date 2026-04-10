"""Typer CLI. `uv run geopol forecast "Will the Iran-Israel ceasefire hold …?"`"""
from __future__ import annotations

import typer

from .pipeline import run_pipeline_sync

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def forecast(
    question: str = typer.Argument(..., help="The forecast question"),
    skip_pdf: bool = typer.Option(False, help="Skip Typst PDF render; emit .typ only"),
) -> None:
    """Run the full Stage-A + Stage-B pipeline and emit a report directory."""
    result = run_pipeline_sync(question, skip_pdf=skip_pdf)
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
